# Importamos las librerías necesarias
import streamlit as st  # Para crear interfaces interactivas web
import yfinance as yf   # Para obtener datos financieros de Yahoo Finance
import pandas as pd     # Para manipulación de datos tabulares
import plotly.graph_objects as go  # Para gráficos personalizados
import plotly.express as px        # Para gráficos rápidos y estilizados

# Configuramos la página de Streamlit
st.set_page_config(page_title="📈 Dashboard Acciones",
                   layout="wide", initial_sidebar_state="expanded")

# Estilos personalizados para modo claro y oscuro
st.markdown("""
    <style>
    html[data-theme="light"] {
        --background-color: #f5f5f5;
        --text-color: #000;
    }
    html[data-theme="dark"] {
        --background-color: #0e1117;
        --text-color: #fafafa;
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo del dashboard
st.title("📈 Dashboard de Acciones")
st.markdown("Visualización dinámica de métricas financieras, precios históricos y dividendos 💹.")

# Diccionario con métricas clave que se quieren mostrar, con nombres más amigables
METRICAS_CLAVE = {
    'currentPrice': 'Precio Actual (ARS)',
    'marketCap': 'Capitalización de Mercado',
    'trailingPE': 'P/E Ratio (últimos 12 meses)',
    'forwardPE': 'P/E Ratio Proyectado',
    'dividendYield': 'Dividend Yield (%)',
    'regularMarketChangePercent': 'Cambio Diario (%)',
    'beta': 'Beta (volatilidad vs mercado)',
    'debtToEquity': 'Deuda/Capital (%)',
    'returnOnEquity': 'ROE (%)',
    'profitMargins': 'Márgen Neto (%)',
    'fiftyTwoWeekHigh': 'Máximo 52 semanas',
    'fiftyTwoWeekLow': 'Mínimo 52 semanas'
}

# Lista de tickers disponibles (acciones locales e internacionales)
TICKERS = ['ALUA.BA', 'BYMA.BA', 'BMA.BA','CGPA2.BA', 'EDN.BA', 'GGAL.BA',
           'METR.BA', 'MSFT', 'PAMP.BA', 'SUPV.BA', 'TGSU2.BA', 'YPFD.BA']

# Sección lateral de configuración del usuario
st.sidebar.title("⚙️ Configuración")
ticker_seleccionado = st.sidebar.multiselect(
    "Selecciona uno o más tickers:",
    options=TICKERS,
    default=['YPFD.BA']  # Por defecto se muestra YPFD
)

# Selección de periodo para datos históricos
periodo = st.sidebar.selectbox(
    "Periodo de datos históricos:",
    ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'],
    index=3  # Por defecto: 3 meses
)

# Función para obtener la info y los datos históricos de un ticker
@st.cache_data
def obtener_datos(ticker):
    datos = yf.Ticker(ticker)
    info = datos.info  # Información general de la empresa
    historico = datos.history(period=periodo)  # Datos históricos según el período elegido
    return info, historico

# Si hay tickers seleccionados, mostramos su información
if ticker_seleccionado:
    for ticker in ticker_seleccionado:
        info, historico = obtener_datos(ticker)

        st.subheader(f"📊 {ticker}")  # Subtítulo con el nombre del ticker

        # Creamos dos columnas: una para gráficos y otra para métricas
        col1, col2 = st.columns([3, 1])

        with col1:
            # Gráfico del precio de cierre
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=historico.index,
                y=historico['Close'],
                mode='lines+markers',
                name='Cierre',
                line=dict(color='royalblue', width=2)
            ))
            fig.update_layout(
                title="Evolución del Precio",
                xaxis_title="Fecha",
                yaxis_title="Precio (ARS)",
                template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de dividendos si existen datos de dividendos
            if 'Dividends' in historico.columns and historico['Dividends'].sum() > 0:
                df_div = historico[historico['Dividends'] > 0].reset_index()
                fig_div = px.bar(
                    df_div,
                    x='Date',
                    y='Dividends',
                    labels={'Dividends': 'Dividendos'},
                    title='Dividendos pagados'
                )
                fig_div.update_layout(
                    template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
                    height=300
                )
                st.plotly_chart(fig_div, use_container_width=True)
            else:
                st.info("No se registran dividendos en este periodo.")

        with col2:
            # Tabla de métricas financieras clave
            st.markdown("### 📌 Métricas Clave")
            metricas = {}
            for clave, nombre in METRICAS_CLAVE.items():
                valor = info.get(clave, 'N/A')  # Obtenemos el valor de la métrica
                if isinstance(valor, float):
                    valor = round(valor, 2)
                metricas[nombre] = valor

            df_metricas = pd.DataFrame.from_dict(
                metricas, orient='index', columns=['Valor'])
            st.dataframe(
                df_metricas.style.format("{:.2f}", subset=df_metricas.select_dtypes(include=["number"]).columns)
            )

            # Recomendación de analistas (ej: BUY, HOLD, etc.)
            recomendacion = info.get('recommendationKey', 'N/A').upper()

            # Color según la recomendación
            color_map = {
                'BUY': 'green',
                'STRONG_BUY': 'darkgreen',
                'HOLD': 'orange',
                'SELL': 'red',
                'STRONG_SELL': 'darkred'
            }
            color = color_map.get(recomendacion, 'gray')

            # Mostramos la recomendación estilizada
            st.markdown(f"""
                <div style="padding: 0.75em; background-color: {color}; color: white; text-align: center; border-radius: 8px; margin-top: 1em;">
                    <strong>Recomendación Analistas:</strong><br>{recomendacion}
                </div>
            """, unsafe_allow_html=True)

# Sección de exportación de datos (botones en la barra lateral)
st.sidebar.markdown("### 📥 Exportar Datos")

# Botón para descargar los datos históricos como CSV
if st.sidebar.button("Descargar CSV"):
    csv_total = pd.DataFrame()
    for ticker in ticker_seleccionado:
        _, historico = obtener_datos(ticker)
        historico['Ticker'] = ticker  # Agregamos columna con el nombre del ticker
        csv_total = pd.concat([csv_total, historico])  # Concatenamos todo

    csv_total.to_csv("datos_acciones.csv")
    st.sidebar.success("CSV guardado como `datos_acciones.csv` 📂")

# Información sobre exportar a HTML (no soportado directamente)
if st.sidebar.button("Descargar HTML de la App"):
    st.sidebar.info(
        "Exportar como HTML requiere usar `streamlit` export tools externas (ej: streamlit-logger o grabar manualmente la web).")
