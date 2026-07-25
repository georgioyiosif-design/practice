import pandas as pd
from pathlib import Path


def transform_to_silver(bronze_path: str, silver_path: str):

    print(f"📥 Διαβάζω bronze: {bronze_path}")
    df = pd.read_parquet(bronze_path)
    print(f"   Γραμμές εισόδου: {len(df)}")

    # --- ΒΗΜΑ 1: ΤΥΠΟΙ ---
    print(f"\n🔧 ΒΗΜΑ 1 - Διόρθωση τύπων:")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["unit_price"] = df["unit_price"].astype(float)
    print(f"   order_date: string → datetime ✅")
    print(f"   unit_price: float ✅")

    # --- ΒΗΜΑ 2: NULLS ---
    print(f"\n🔧 ΒΗΜΑ 2 - Χειρισμός nulls:")
    null_country = df["country"].isnull().sum()
    null_status  = df["status"].isnull().sum()
    df["country"] = df["country"].fillna("Unknown")
    df["status"]  = df["status"].fillna("unknown")
    print(f"   country: {null_country} nulls → 'Unknown' ✅")
    print(f"   status:  {null_status} nulls → 'unknown' ✅")

    # --- ΒΗΜΑ 3: ΕΓΚΥΡΟΤΗΤΑ ---
    print(f"\n🔧 ΒΗΜΑ 3 - Έλεγχοι εγκυρότητας:")
    invalid_price = (df["unit_price"] <= 0).sum()
    invalid_qty   = (df["quantity"] <= 0).sum()
    print(f"   Αρνητικές τιμές unit_price: {invalid_price}")
    print(f"   Αρνητικές τιμές quantity:   {invalid_qty}")
    df = df[df["unit_price"] > 0]
    df = df[df["quantity"] > 0]

    # --- ΒΗΜΑ 4: ΝΕΕΣ ΣΤΗΛΕΣ ---
    print(f"\n🔧 ΒΗΜΑ 4 - Νέες στήλες:")
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_year"]   = df["order_date"].dt.year
    df["order_month"]  = df["order_date"].dt.month
    print(f"   total_amount = quantity × unit_price ✅")
    print(f"   order_year, order_month ✅")

    # --- ΒΗΜΑ 5: ΠΟΙΟΤΙΚΟΙ ΕΛΕΓΧΟΙ ---
    print(f"\n✔️  ΒΗΜΑ 5 - Ποιοτικοί έλεγχοι:")

    checks = {
        "Μοναδικότητα order_id":     df["order_id"].nunique() == len(df),
        "Καμία αρνητική unit_price": df["unit_price"].min() > 0,
        "Κανένα null total_amount":  df["total_amount"].isnull().sum() == 0,
        "Κανένα null country":       df["country"].isnull().sum() == 0,
        "Κανένα null status":        df["status"].isnull().sum() == 0,
    }

    all_passed = True
    for check_name, result in checks.items():
        icon = "✅" if result else "❌"
        print(f"   {icon} {check_name}: {'PASS' if result else 'FAIL'}")
        if not result:
            all_passed = False

    if all_passed:
        print(f"\n   Όλοι οι έλεγχοι πέρασαν ✅")
    else:
        raise Exception("❌ Αποτυχία ποιοτικών ελέγχων")

    # --- ΑΠΟΘΗΚΕΥΣΗ ---
    output = Path(silver_path)
    output.mkdir(parents=True, exist_ok=True)
    output_file = output / "orders.parquet"
    df.to_parquet(output_file, index=False)

    print(f"\n✅ Silver layer έτοιμο: {output_file}")
    print(f"   Γραμμές εξόδου: {len(df)}")
    print(f"\n   Δείγμα:")
    print(df[["order_id", "order_date", "status",
              "country", "total_amount"]].head())


if __name__ == "__main__":
    transform_to_silver(
        bronze_path="data/bronze/orders.parquet",
        silver_path="data/silver"
    )