import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def load_data():
    orders_df = pd.read_csv('output/orders_per_minute_last_hour.csv')
    budgets_df = pd.read_csv('output/budgets_per_minute_last_hour.csv')
    store_info_df = pd.read_csv('output/store_info.csv')
    products_out_of_stock_df = pd.read_csv('output/products_out_of_stock_last_hour.csv')
    regions_most_orders_df = pd.read_csv('output/regions_most_orders_last_hour.csv')
    return orders_df, budgets_df, store_info_df, products_out_of_stock_df, regions_most_orders_df

def calculate_orders_per_minute_last_hour(orders_df):
    return orders_df.groupby('minute')['order_count'].sum()

def calculate_budgets_per_minute_last_hour(budgets_df):
    return budgets_df.groupby(['minute', 'state'])['budget_count'].sum().reset_index()

def display_store_info(store_info_df):
    st.subheader('Informações das Lojas')
    st.dataframe(store_info_df)
    
def display_products_out_of_stock(products_out_of_stock_df):
    st.subheader('Produtos Mais Frequentemente em Falta')
    st.dataframe(products_out_of_stock_df)

def display_regions_most_orders(regions_most_orders_df):
    st.subheader('Regiões com Maior Número de Pedidos')
    st.dataframe(regions_most_orders_df)

def main():
    st.title('Dashboard - FastDelivery Analysis')
    st.sidebar.title('Menu')
    selected_page = st.sidebar.selectbox('Selecione uma página', ['Visão Geral', 'Informações das Lojas', 'Produtos em Falta', 'Regiões com Mais Pedidos'])

    orders_df, budgets_df, store_info_df, products_out_of_stock_df, regions_most_orders_df = load_data()

    if selected_page == 'Visão Geral':
        st.subheader('Visão Geral das Últimas Análises')

        # Number of orders per minute in the last hour
        st.subheader('Número de Pedidos por Minuto na Última Hora')
        orders_per_minute = calculate_orders_per_minute_last_hour(orders_df)
        st.line_chart(orders_per_minute)

        # Number of budgets per minute in the last hour, segmented by state
        st.subheader('Número de Orçamentos por Minuto na Última Hora (Segmentado por Estado)')
        budgets_per_minute = calculate_budgets_per_minute_last_hour(budgets_df)
        st.line_chart(budgets_per_minute)

    elif selected_page == 'Informações das Lojas':
        display_store_info(store_info_df)

    elif selected_page == 'Produtos em Falta':
        display_products_out_of_stock(products_out_of_stock_df)

    elif selected_page == 'Regiões com Mais Pedidos':
        display_regions_most_orders(regions_most_orders_df)

if __name__ == '__main__':
    main()
