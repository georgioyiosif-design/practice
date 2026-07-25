import pandas as pd
from pathlib import Path


def transform_to_gold(silver_path: str, gold_path: str):

    print(f"📥 Διαβάζω silver: {silver_path}")
    df = pd.read_parquet(silver_path)
    print(f"   Γραμμές εισόδου: {len(df)}")

    output = Path(gold_path)
    output.mkdir(parents=True, exist_ok=True)

    # --- GOLD 1: Πωλήσεις ανά χώρα και μήνα ---
    print(f"\n📊 GOLD 1 - Πωλήσεις ανά χώρα και μήνα:")
    sales_by_country = (
        df.groupby(["country", "order_year", "order_month"])
        .agg(
            total_revenue=("total_amount", "sum"),
            total_orders =("order_id",     "count"),
            avg_order    =("total_amount", "mean")
        )
        .round(2)
        .reset_index()
    )
    sales_by_country.to_parquet(output / "sales_by_country.parquet", index=False)
    print(f"   Γραμμές: {len(sales_by_country)}")
    print(sales_by_country.head())

    # --- GOLD 2: Απόδοση ανά προϊόν ---
    print(f"\n📊 GOLD 2 - Απόδοση ανά προϊόν:")
    sales_by_product = (
        df.groupby("product")
        .agg(
            total_revenue=("total_amount", "sum"),
            units_sold   =("quantity",     "sum"),
            avg_price    =("unit_price",   "mean"),
            total_orders =("order_id",     "count")
        )
        .round(2)
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    sales_by_product.to_parquet(output / "sales_by_product.parquet", index=False)
    print(f"   Γραμμές: {len(sales_by_product)}")
    print(sales_by_product)

    # --- GOLD 3: Σύνοψη ανά πελάτη ---
    print(f"\n📊 GOLD 3 - Σύνοψη ανά πελάτη:")
    customer_summary = (
        df.groupby("customer_id")
        .agg(
            total_orders     =("order_id",     "count"),
            total_spent      =("total_amount", "sum"),
            avg_order        =("total_amount", "mean"),
            favourite_product=("product",      lambda x: x.value_counts().index[0])
        )
        .round(2)
        .reset_index()
        .sort_values("total_spent", ascending=False)
    )
    customer_summary.to_parquet(output / "customer_summary.parquet", index=False)
    print(f"   Γραμμές: {len(customer_summary)}")
    print(customer_summary.head())

    print(f"\n✅ Gold layer έτοιμο στο: {gold_path}")


if __name__ == "__main__":
    transform_to_gold(
        silver_path="data/silver/orders.parquet",
        gold_path="data/gold"
    )