import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Precios por unidad y docena
PRECIO_TATIN_U, PRECIO_TATIN_D = 500, 5200
PRECIO_SHOT_U, PRECIO_SHOT_D = 900, 9500
PRECIO_FULBITO_U, PRECIO_FULBITO_D = 400, 4200
PRECIO_RASTA_U, PRECIO_RASTA_D = 1100, 11500
PRECIO_JORGITO_U, PRECIO_JORGITO_D = 800, 8500

# Inicialización de la sesión
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "nombre" not in st.session_state:
    st.session_state.nombre = ""

# PANTALLA 1: Pedir nombre
if not st.session_state.logueado:
    st.title("Tienda de Alfajores")
    
    nombre = st.text_input("Ingresa tu nombre:")
    
    if st.button("Acceder"):
        if nombre != "":
            st.session_state.nombre = nombre
            st.session_state.logueado = True
        else:
            st.write("Por favor, escribe un nombre para continuar.")

# PANTALLA 2: Compra y generación del PDF adaptado
if st.session_state.logueado:
    st.title("Bienvenido/a " + st.session_state.nombre)
    
    st.write("---")
    st.title("Lista de alfajores y precios")
    st.write("• **Tatín** - Unidad: $", PRECIO_TATIN_U, " | Docena: $", PRECIO_TATIN_D)
    st.write("• **Shot** - Unidad: $", PRECIO_SHOT_U, " | Docena: $", PRECIO_SHOT_D)
    st.write("• **Fulbito** - Unidad: $", PRECIO_FULBITO_U, " | Docena: $", PRECIO_FULBITO_D)
    st.write("• **Rasta** - Unidad: $", PRECIO_RASTA_U, " | Docena: $", PRECIO_RASTA_D)
    st.write("• **Jorgito** - Unidad: $", PRECIO_JORGITO_U, " | Docena: $", PRECIO_JORGITO_D)
    
    st.write("---")
    st.title("Selecciona las cantidades")
    
    # Tatín
    st.write("**Alfajor Tatín**")
    tatin_u = st.selectbox("Unidades de Tatín:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    tatin_d = st.selectbox("Docenas de Tatín:", [0, 1, 2, 3, 4, 5])
    
    # Shot
    st.write("**Alfajor Shot**")
    shot_u = st.selectbox("Unidades de Shot:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    shot_d = st.selectbox("Docenas de Shot:", [0, 1, 2, 3, 4, 5])

    # Fulbito
    st.write("**Alfajor Fulbito**")
    fulbito_u = st.selectbox("Unidades de Fulbito:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    fulbito_d = st.selectbox("Docenas de Fulbito:", [0, 1, 2, 3, 4, 5])

    # Rasta
    st.write("**Alfajor Rasta**")
    rasta_u = st.selectbox("Unidades de Rasta:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    rasta_d = st.selectbox("Docenas de Rasta:", [0, 1, 2, 3, 4, 5])

    # Jorgito
    st.write("**Alfajor Jorgito**")
    jorgito_u = st.selectbox("Unidades de Jorgito:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    jorgito_d = st.selectbox("Docenas de Jorgito:", [0, 1, 2, 3, 4, 5])

    # Selección del método de pago
    metodo_pago = st.selectbox("¿Con qué vas a pagar?", ["Efectivo", "Transferencia"])

    # -------------------------------------------------------------
    # CÁLCULOS SIGUIENDO TU SECUENCIA
    # -------------------------------------------------------------
    # 1. Subtotal: Suma de la lista
    subtotal = (
        (tatin_u * PRECIO_TATIN_U) + (tatin_d * PRECIO_TATIN_D) +
        (shot_u * PRECIO_SHOT_U) + (shot_d * PRECIO_SHOT_D) +
        (fulbito_u * PRECIO_FULBITO_U) + (fulbito_d * PRECIO_FULBITO_D) +
        (rasta_u * PRECIO_RASTA_U) + (rasta_d * PRECIO_RASTA_D) +
        (jorgito_u * PRECIO_JORGITO_U) + (jorgito_d * PRECIO_JORGITO_D)
    )

    # 2. Descuento: Subtotal * 0.10 (solo si es efectivo)
    descuento = 0.0
    if metodo_pago == "Efectivo":
        descuento = subtotal * 0.10

    # 3. Base: Subtotal - Descuento
    base = subtotal - descuento

    # 4. IVA: Base * 0.21
    iva = base * 0.21

    # 5. Total: Base + IVA
    total_final = base + iva

    # -------------------------------------------------------------
    # MUESTRA DEL RESUMEN EN PANTALLA
    # -------------------------------------------------------------
    st.write("---")
    st.title("Resumen")
    st.write("1. Subtotal: $", round(subtotal, 2))
    st.write("2. Descuento (10% Efectivo): -$", round(descuento, 2))
    st.write("3. Base Imponible: $", round(base, 2))
    st.write("4. IVA (21%): $", round(iva, 2))
    st.write(f"### 5. Total: ${total_final:.2f}")

    if st.button("Confirmar compra"):
        if subtotal > 0:
            st.write("¡Gracias por tu compra, " + st.session_state.nombre + "!")
            st.write("Elegiste pagar mediante ", metodo_pago)

            # -------------------------------------------------------------
            # CONSTRUCCIÓN DEL PDF CON LA SECUENCIA DE LA HOJA
            # -------------------------------------------------------------
            pdf = FPDF()
            pdf.add_page()

            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            # Encabezado
            pdf.set_font("Arial", "B", 18)
            pdf.cell(0, 8, "Kiosco Carlos Paz", ln=True, align="R")
            
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 6, "Presupuesto N° 1", ln=True, align="R")
            pdf.cell(0, 6, f"Fecha: {fecha_actual}", ln=True, align="R")
            pdf.ln(15)

            # Cliente
            pdf.set_font("Arial", "", 12)
            pdf.cell(90, 8, "Cliente", align="L")
            pdf.cell(90, 8, st.session_state.nombre, align="R", ln=True)
            pdf.ln(8)

            # Detalle de los productos
            pdf.set_font("Arial", "", 11)
            
            if tatin_u > 0:
                costo = tatin_u * PRECIO_TATIN_U
                pdf.cell(120, 7, f"{tatin_u} x Alfajor Tatin", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)
            if tatin_d > 0:
                costo = tatin_d * PRECIO_TATIN_D
                pdf.cell(120, 7, f"{tatin_d} x Docena Tatin", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)

            if shot_u > 0:
                costo = shot_u * PRECIO_SHOT_U
                pdf.cell(120, 7, f"{shot_u} x Alfajor Shot", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)
            if shot_d > 0:
                costo = shot_d * PRECIO_SHOT_D
                pdf.cell(120, 7, f"{shot_d} x Docena Shot", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)

            if fulbito_u > 0:
                costo = fulbito_u * PRECIO_FULBITO_U
                pdf.cell(120, 7, f"{fulbito_u} x Alfajor Fulbito", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)
            if fulbito_d > 0:
                costo = fulbito_d * PRECIO_FULBITO_D
                pdf.cell(120, 7, f"{fulbito_d} x Docena Fulbito", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)

            if rasta_u > 0:
                costo = rasta_u * PRECIO_RASTA_U
                pdf.cell(120, 7, f"{rasta_u} x Alfajor Rasta", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)
            if rasta_d > 0:
                costo = rasta_d * PRECIO_RASTA_D
                pdf.cell(120, 7, f"{rasta_d} x Docena Rasta", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)

            if jorgito_u > 0:
                costo = jorgito_u * PRECIO_JORGITO_U
                pdf.cell(120, 7, f"{jorgito_u} x Alfajor Jorgito", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)
            if jorgito_d > 0:
                costo = jorgito_d * PRECIO_JORGITO_D
                pdf.cell(120, 7, f"{jorgito_d} x Docena Jorgito", align="L")
                pdf.cell(60, 7, f"${costo:.2f}", align="R", ln=True)

            pdf.ln(10)

            # BLOQUE DE TOTALES SEGÚN TU SECUENCIA
            pdf.cell(120, 7, "1. Subtotal", align="L")
            pdf.cell(60, 7, f"${subtotal:.2f}", align="R", ln=True)

            pdf.cell(120, 7, "2. Descuento (10% Efectivo)", align="L")
            pdf.cell(60, 7, f"-${descuento:.2f}", align="R", ln=True)

            pdf.cell(120, 7, "3. Base", align="L")
            pdf.cell(60, 7, f"${base:.2f}", align="R", ln=True)

            pdf.cell(120, 7, "4. IVA (21%)", align="L")
            pdf.cell(60, 7, f"${iva:.2f}", align="R", ln=True)

            pdf.set_font("Arial", "B", 13)
            pdf.cell(120, 8, "5. TOTAL", align="L")
            pdf.cell(60, 8, f"${total_final:.2f}", align="R", ln=True)

            pdf.ln(15)

            # Pie de página
            pdf.set_font("Arial", "I", 9)
            pdf.cell(0, 6, "Presupuesto valido por 7 dias.", align="L", ln=True)

            pdf_bytes = bytes(pdf.output())

            st.download_button(
                label="📄 Descargar recibo en PDF",
                data=pdf_bytes,
                file_name=f"presupuesto_{st.session_state.nombre}.pdf",
                mime="application/pdf"
            )
        else:
            st.write("No has seleccionado ningún producto.")