import streamlit as st
from calculos_N4_2 import *

productos = ["Alfajor", "Gaseosa", "Chicle", "Agua"]
precios = [1500, 2800, 500, 1800]

st.title("Kiosco Carlos Paz")

if "ingresado" not in st.session_state:
    st.session_state["ingresado"] = False

nombre = st.text_input("Nombre del cliente")

if st.button("Ingresar"):
    if nombre:
        st.session_state["ingresado"] = True

if st.session_state["ingresado"]:
    producto = st.selectbox("Producto", productos)
    cantidad = st.number_input("Cantidad", value=0)
    pago = st.radio("Forma de pago", [EFECTIVO, TRANSFERENCIA])

    pos = buscar_posicion(productos, producto)
    precio = precios[pos]

    subtotal = cantidad * precio
    con_desc = aplicar_descuento(subtotal, pago)
    descuento = subtotal - con_desc
    iva = calcular_iva(con_desc)
    total = con_desc + iva

    st.write(f"Pedido de {nombre}")
    st.write(f"Subtotal: ${subtotal}")
    st.write(f"Descuento: -${descuento}")
    st.write(f"IVA: +${iva}")
    st.metric("TOTAL", f"${total}")
