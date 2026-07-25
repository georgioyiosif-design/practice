import pandas as pd
from pathlib import Path
from datetime import datetime


def ingest_to_bronze(source_path: str, bronze_path: str):

    print(f"📥 Διαβάζω πηγή: {source_path}")
    df = pd.read_csv(source_path)

    # --- PROFILING ---
    print(f"\n📊 PROFILING ΠΗΓΗΣ:")
    print(f"   Γραμμές:    {len(df)}")
    print(f"   Στήλες:     {list(df.columns)}")
    print(f"   Τύποι:\n{df.dtypes}")
    print(f"\n   Nulls:\n{df.isnull().sum()}")
    print(f"\n   Διπλότυπα: {df.duplicated().sum()}")

    # --- ΕΠΑΛΗΘΕΥΣΗ PRIMARY KEY ---
    print(f"\n🔑 ΕΛΕΓΧΟΣ PRIMARY KEY:")
    for col in ["order_id", "customer_id"]:
        unique = df[col].nunique()
        total  = len(df)
        nulls  = df[col].isnull().sum()
        print(f"\n   {col}:")
        print(f"      Μοναδικές τιμές: {unique} από {total}")
        print(f"      Null τιμές:      {nulls}")
        if unique == total and nulls == 0:
            print(f"      ✅ Μπορεί να είναι PRIMARY KEY")
        else:
            print(f"      ❌ ΔΕΝ μπορεί να είναι primary key")

    # --- METADATA ---
    df["_source_file"] = Path(source_path).name
    df["_ingested_at"] = datetime.now().isoformat()

    # --- ΑΠΟΘΗΚΕΥΣΗ σε Parquet ---
    output = Path(bronze_path)
    output.mkdir(parents=True, exist_ok=True)
    output_file = output / "orders.parquet"
    df.to_parquet(output_file, index=False)

    print(f"\n✅ Bronze layer έτοιμο: {output_file}")
    print(f"   Μέγεθος CSV:     "
          f"{Path(source_path).stat().st_size / 1024:.1f} KB")
    print(f"   Μέγεθος Parquet: "
          f"{output_file.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    ingest_to_bronze(
        source_path="data/source/orders.csv",
        bronze_path="data/bronze"
    )