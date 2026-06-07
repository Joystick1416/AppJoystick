import streamlit as st
from pymongo import MongoClient

def connect_to_mongodb():
    connection_string = st.secrets["MONGODB_CONNECTION_STRING"]
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Error conectando a MongoDB: {e}")
        return None

def query_sales_by_method(payment_method):
    try:
        client = connect_to_mongodb()
        if not client:
            return None, 0

        db = client.sample_supplies
        collection = db.sales

        query = {"purchaseMethod": payment_method}
        sales = list(collection.find(query).limit(5))
        total = collection.count_documents(query)

        client.close()
        return sales, total

    except Exception as e:
        st.error(f"Error al consultar MongoDB: {e}")
        return None, 0

st.set_page_config(page_title="Buscador de Ventas", page_icon="🛒")
st.title("🛒 Buscador de Ventas por Método de Pago")

method = st.selectbox("Método de pago:", ["In store", "Online", "Phone"])

if st.button("Buscar"):
    with st.spinner(f"Buscando ventas con {method}..."):
        sales, total = query_sales_by_method(method)

        if sales:
            st.success(f"Se encontraron {total} ventas con método '{method}'")
            st.write("Mostrando los primeros 5 resultados:")

            for i, sale in enumerate(sales, 1):
                with st.expander(f"Venta #{i}"):
                    st.write(f"**ID:** {sale.get('_id')}")
                    st.write(f"**Método de pago:** {sale.get('purchaseMethod')}")
                    st.write(f"**Items:** {len(sale.get('items', []))} productos")
                    st.write(f"**Cliente:** {sale.get('customer', {}).get('email', 'N/A')}")
        else:
            st.warning("No se encontraron ventas.")

st.divider()
st.caption("App conectada a MongoDB Atlas - sample_supplies")
