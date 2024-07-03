from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import time
import datetime as dt

def run_analysis_pipeline(spark: SparkSession):
    # Carregar dados
    orders_df = spark.read.csv("src/data/orders.csv", header=False, inferSchema=True, mode="DROPMALFORMED")
    budgets_df = spark.read.csv("src/data/budgets.csv", header=False, inferSchema=True, mode="DROPMALFORMED")

    # Registrar tabelas temporárias para SQL
    orders_df.createOrReplaceTempView("orders")
    budgets_df.createOrReplaceTempView("budgets")

    # 1. Número de pedidos por minuto na última hora
    orders_per_minute_last_hour = spark.sql("""
        SELECT
            date_format(timestamp, 'yyyy-MM-dd HH:mm') as minute,
            count(*) as order_count
        FROM
            orders
        WHERE
            timestamp > date_sub(current_timestamp(), 60)
        GROUP BY
            minute
        ORDER BY
            minute
    """)

    # 2. Número de orçamentos por minuto na última hora, segmentados por estado
    budgets_per_minute_last_hour = spark.sql("""
        SELECT
            date_format(timestamp, 'yyyy-MM-dd HH:mm') as minute,
            state,
            count(*) as budget_count
        FROM
            budgets
        WHERE
            timestamp > date_sub(current_timestamp(), 60)
        GROUP BY
            minute, state
        ORDER BY
            minute, state
    """)

    # 3. Tabela com informações de cada loja
    store_info = spark.sql("""
        SELECT
            store_id,
            count(*) as total_budgets,
            sum(case when state = 'approved' then 1 else 0 end) as approved_budgets,
            sum(case when state = 'rejected' or state = 'cancelled' then 1 else 0 end) as rejected_cancelled_budgets,
            sum(case when state = 'approved' then price else 0 end) as total_revenue,
            avg(timestamp - lag(timestamp) over (partition by store_id order by timestamp)) as avg_time_between_orders,
            max(distance) as max_distance,
            avg(distance) as avg_distance,
            min(distance) as min_distance
        FROM
            budgets
        GROUP BY
            store_id
    """)

    # 4. Os 10 produtos mais frequentemente em falta na última hora
    products_out_of_stock_last_hour = spark.sql("""
        SELECT
            product_id,
            count(*) as out_of_stock_count
        FROM
            budgets
        WHERE
            state = 'rejected'
        GROUP BY
            product_id
        ORDER BY
            out_of_stock_count DESC
        LIMIT 10
    """)

    # 5. As 5 regiões que mais solicitaram pedidos na última hora
    regions_most_orders_last_hour = spark.sql("""
        SELECT
            consumer_neighborhood as region,
            count(*) as order_count
        FROM
            orders
        GROUP BY
            consumer_neighborhood
        ORDER BY
            order_count DESC
        LIMIT 5
    """)

    # Salvar os resultados em arquivos de saída ou persistir em algum armazenamento
    # Exemplo: salvar em CSV ou em um banco de dados
    
    # Exemplo de salvamento em CSV (você pode ajustar conforme necessário)
    orders_per_minute_last_hour.write.csv("output/orders_per_minute_last_hour.csv", mode="overwrite", header=True)
    budgets_per_minute_last_hour.write.csv("output/budgets_per_minute_last_hour.csv", mode="overwrite", header=True)
    store_info.write.csv("output/store_info.csv", mode="overwrite", header=True)
    products_out_of_stock_last_hour.write.csv("output/products_out_of_stock_last_hour.csv", mode="overwrite", header=True)
    regions_most_orders_last_hour.write.csv("output/regions_most_orders_last_hour.csv", mode="overwrite", header=True)

    # Pode ser útil retornar alguns resultados se necessário
    return {
        "orders_per_minute_last_hour": orders_per_minute_last_hour,
        "budgets_per_minute_last_hour": budgets_per_minute_last_hour,
        "store_info": store_info,
        "products_out_of_stock_last_hour": products_out_of_stock_last_hour,
        "regions_most_orders_last_hour": regions_most_orders_last_hour
    }

if __name__ == "__main__":
    spark = SparkSession.builder.appName("FastDeliveryAnalysis").getOrCreate()
    result = run_analysis_pipeline(spark)
    spark.stop()
