import duckdb

# Συνδεόμαστε — χωρίς server, χωρίς εγκατάσταση
con = duckdb.connect()

print("=" * 55)
print("ΑΝΑΛΥΣΗ ΠΩΛΗΣΕΩΝ — DuckDB πάνω σε Parquet")
print("=" * 55)

# --- ΕΡΩΤΗΜΑ 1: Top 5 χώρες σε τζίρο ---
print("\n🏆 Top 5 χώρες σε συνολικό τζίρο:")
con.execute("""
    SELECT
        country,
        SUM(total_revenue)  AS total_revenue,
        SUM(total_orders)   AS total_orders,
        ROUND(AVG(avg_order), 2) AS avg_order
    FROM read_parquet('data/gold/sales_by_country.parquet')
    GROUP BY country
    ORDER BY total_revenue DESC
    LIMIT 5
""").df().pipe(print)

# --- ΕΡΩΤΗΜΑ 2: Μηνιαία εξέλιξη τζίρου ---
print("\n📅 Μηνιαίος τζίρος (όλες οι χώρες):")
con.execute("""
    SELECT
        order_year,
        order_month,
        SUM(total_revenue) AS monthly_revenue,
        SUM(total_orders)  AS monthly_orders
    FROM read_parquet('data/gold/sales_by_country.parquet')
    GROUP BY order_year, order_month
    ORDER BY order_year, order_month
""").df().pipe(print)

# --- ΕΡΩΤΗΜΑ 3: Απόδοση προϊόντων ---
print("\n📦 Απόδοση προϊόντων:")
con.execute("""
    SELECT
        product,
        total_revenue,
        units_sold,
        avg_price,
        ROUND(total_revenue / units_sold, 2) AS revenue_per_unit
    FROM read_parquet('data/gold/sales_by_product.parquet')
    ORDER BY total_revenue DESC
""").df().pipe(print)

# --- ΕΡΩΤΗΜΑ 4: Top 10 πελάτες ---
print("\n👤 Top 10 πελάτες σε τζίρο:")
con.execute("""
    SELECT
        customer_id,
        total_orders,
        total_spent,
        avg_order,
        favourite_product
    FROM read_parquet('data/gold/customer_summary.parquet')
    ORDER BY total_spent DESC
    LIMIT 10
""").df().pipe(print)

# --- ΕΡΩΤΗΜΑ 5: Window function ---
print("\n📊 Κατάταξη προϊόντων ανά χώρα (window function):")
con.execute("""
    SELECT
        country,
        order_year,
        order_month,
        total_revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY total_revenue DESC
        ) AS rank_in_country
    FROM read_parquet('data/gold/sales_by_country.parquet')
    QUALIFY rank_in_country <= 2
    ORDER BY country, rank_in_country
""").df().pipe(print)

con.close()
print("\n✅ Ανάλυση ολοκληρώθηκε")