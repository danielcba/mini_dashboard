# Importamos las librerías necesarias
import streamlit as st  # Para crear interfaces interactivas web
import yfinance as yf   # Para obtener datos financieros de Yahoo Finance
from yfinance.exceptions import YFRateLimitError  # Manejo de límite de peticiones
import time  # Para pausas entre reintentos
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
    
    /* Mejora de estilo para las métricas */
    .metric-row {
        padding: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo del dashboard
st.title("📈 Dashboard de Acciones")
st.markdown("Visualización dinámica de métricas financieras, precios históricos y dividendos 💹.")

# Diccionario con métricas clave que se quieren mostrar, con nombres más amigables
METRICAS_CLAVE = {
    'currentPrice': 'Precio Actual',
    'marketCap': 'Capitalización de Mercado',
    'trailingPE': 'P/E Ratio (últimos 12 meses)',
    'forwardPE': 'P/E Ratio Proyectado',
    'dividendYield': 'Dividend Yield (%)',
    'dividendRate': 'Precio de Pago de Dividendo',
    'regularMarketChangePercent': 'Cambio Diario (%)',
    'beta': 'Beta (volatilidad vs mercado)',
    'debtToEquity': 'Deuda/Capital (%)',
    'returnOnEquity': 'ROE (%)',
    'profitMargins': 'Margen Neto (%)',
    'fiftyTwoWeekHigh': 'Máximo 52 semanas',
    'fiftyTwoWeekLow': 'Mínimo 52 semanas'
}

# Lista de tickers disponibles (acciones locales e internacionales)
# TICKERS = ['AAPL', 'ADBE', 'AMCR', 'AMZN', 'AVGO', 'BEN', 'CDUAF', 'CVX', 'FDX', 'FIZZ', 'FRT', '^GSPC', 'GOOG', 'GOOGL', 'IBM', 'INTC', 'JNJ', 'KAI', 'KO', 'LNVGY', 'NWN', 'MELI', 'META', 'MKTX', 'MSFT', 'NVDA', 'PEP', 'PM', 'SWK', 'TROW', 'TSLA', 'UNH', 'XOM']
# Fabi --> TICKERS = ['AAPL', 'BEN', 'FIZZ', 'FXAIX', 'JPM', 'QQQ', 'RSP', 'SCHD', 'SPAXX', 'SPY', 'TLT', 'TSLA', 'VOO', 'XLK']
TICKERS = ['A3.BA', 'BHIP.BA', 'BPAT.BA', 'BYMA.BA', 'CRES.BA', 'ECOG.BA', 'IRSA.BA', 'MOLA.BA', 'MOLI.BA', 'TRAN.BA', 'YPF']

# Sección lateral de configuración del usuario
st.sidebar.title("⚙️ Configuración")
ticker_seleccionado = st.sidebar.multiselect(
    "Selecciona uno o más tickers:",
    options=TICKERS,
    default=['LMT']  # Por defecto se muestra AAPL
)

# Selección de periodo para datos históricos
periodo = st.sidebar.selectbox(
    "Periodo de datos históricos:",
    ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'],
    index=3  # Por defecto: 1y
)

# Función para obtener la info y los datos históricos de un ticker
@st.cache_data
def obtener_datos(ticker, periodo, reintentos: int = 3, pausa_inicial: int = 2):
    """Descarga información y precios históricos del ticker.

    Realiza varios reintentos con back-off exponencial para evitar errores
    `YFRateLimitError` cuando se excede el límite de Yahoo Finance (frecuente
    en Streamlit Cloud donde muchas apps comparten IP).
    """
    for intento in range(reintentos):
        try:
            datos = yf.Ticker(ticker)
            info = datos.info  # Información general de la empresa
            historico = datos.history(period=periodo)
            return info, historico
        except YFRateLimitError:
            # Si no es el último intento, esperar y reintentar
            if intento < reintentos - 1:
                time.sleep(pausa_inicial * (2 ** intento))  # back-off exponencial
            else:
                st.warning(f"⚠️ Límite de peticiones alcanzado para {ticker}. Intenta más tarde.")
                # Devolver estructuras vacías para evitar que la app se caiga
                return {}, pd.DataFrame()

# Función para formatear números grandes (millones y billones)
def format_number(val):
    if not isinstance(val, (int, float)) or pd.isna(val):
        return val
    if abs(val) >= 1e12:  # Trillones
        return f"{val/1e12:.2f}T"
    elif abs(val) >= 1e9:  # Billones
        return f"{val/1e9:.2f}B"
    elif abs(val) >= 1e6:  # Millones
        return f"{val/1e6:.2f}M"
    return f"{val:,.2f}"

# Si hay tickers seleccionados, mostramos su información
if ticker_seleccionado:
    for ticker in ticker_seleccionado:
        info, historico = obtener_datos(ticker, periodo)

        # Obtener el nombre de la empresa (shortName o longName)
        company_name = info.get('shortName', info.get('longName', '')) or 'Empresa desconocida'
        st.subheader(f"📊 {ticker} - {company_name}")  # Subtítulo con el nombre del ticker y la empresa

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
            
            # Añadir bandas de máximo y mínimo de 52 semanas si están disponibles
            if 'fiftyTwoWeekHigh' in info and 'fiftyTwoWeekLow' in info:
                max_52 = info['fiftyTwoWeekHigh']
                min_52 = info['fiftyTwoWeekLow']
                fig.add_hline(y=max_52, line_dash="dash", line_color="green", 
                              annotation_text=f"Máx 52s: {max_52:.2f}", 
                              annotation_position="bottom right")
                fig.add_hline(y=min_52, line_dash="dash", line_color="red", 
                              annotation_text=f"Mín 52s: {min_52:.2f}", 
                              annotation_position="bottom right")
            
            fig.update_layout(
                title="Evolución del Precio",
                xaxis_title="Fecha",
                yaxis_title="Precio",
                yaxis=dict(tickformat=".2f"),
                template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True, key=f"{ticker}_price")

            # Gráfico de dividendos si existen datos de dividendos
            if 'Dividends' in historico.columns and historico['Dividends'].sum() > 0:
                df_div = historico[historico['Dividends'] > 0].reset_index()
                fig_div = px.bar(
                    df_div,
                    x='Date',
                    y='Dividends',
                    labels={'Dividends': 'Dividendos'},
                    title='Dividendos pagados',
                    color='Dividends',
                    color_continuous_scale='greens'
                )
                fig_div.update_layout(
                    template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
                    height=300
                )
                st.plotly_chart(fig_div, use_container_width=True, key=f"{ticker}_div")
            else:
                st.info("No se registran dividendos en este periodo.")

        with col2:
            # Tabla de métricas financieras clave
            st.markdown("### 📌 Métricas Clave")
            metricas = {}
            for clave, nombre in METRICAS_CLAVE.items():
                valor = info.get(clave, 'N/A')  # Obtenemos el valor de la métrica
                if isinstance(valor, (int, float)) and not pd.isna(valor):
                    if 'Capitalización' in nombre:  # Aplicar formato especial a capitalización
                        metricas[nombre] = format_number(valor)
                    else:
                        # Formatear a string con exactamente 2 decimales
                        metricas[nombre] = valor
                else:
                    metricas[nombre] = valor

            df_metricas = pd.DataFrame.from_dict(
                metricas, orient='index', columns=['Valor'])
            
            # Función para aplicar estilos condicionales por fila
            def style_row(row):
                metric_name = row.name  # Nombre de la métrica (índice)
                valor = row['Valor']
                style = ''
                
                # Solo aplicar color a 'Cambio Diario (%)'
                if metric_name == 'Cambio Diario (%)':
                    if isinstance(valor, (int, float)) and not pd.isna(valor):
                        if valor < 0:
                            style = 'color: #FF5252; font-weight: bold'  # Rojo
                        elif valor > 0:
                            style = 'color: #4CAF50; font-weight: bold'  # Verde
                return [style]  # Devuelve una lista con un estilo por celda
            
            # Aplicar estilos y formato
            styled_df = (
                df_metricas.style
                .apply(style_row, axis=1)
                .format(
                    formatter={
                        'Valor': lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) and not pd.isna(x) else x
                    }
                )
            )
            
            st.dataframe(styled_df, height=500)

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
st.sidebar.markdown("### 📥 Exportar Datos Históricos")

# Botón para descargar los datos históricos como CSV
if ticker_seleccionado:
    csv_total = pd.DataFrame()
    for ticker in ticker_seleccionado:
        _, historico = obtener_datos(ticker, periodo)
        historico['Ticker'] = ticker  # Agregamos columna con el nombre del ticker
        csv_total = pd.concat([csv_total, historico])  # Concatenamos todo

    # Convertir DataFrame a CSV
    csv = csv_total.to_csv(index=False).encode('utf-8')

    # Botón de descarga
    st.sidebar.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="datos_historicos_acciones.csv",
        mime="text/csv",
        help="Haz clic para descargar los datos en formato CSV"
    )
else:
    st.sidebar.warning("Selecciona al menos un ticker para exportar datos")
