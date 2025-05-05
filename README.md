# 📈 Dashboard de Acciones Argentina - PRO

Una aplicación web interactiva construida con [Streamlit](https://streamlit.io/) que permite visualizar de forma clara y dinámica **métricas financieras**, **precios históricos** y **dividendos** de acciones locales e internacionales. Ideal para seguimiento de inversiones y análisis bursátil 📊.

---

## 🧰 Funcionalidades

✅ Selección múltiple de **tickers** (acciones)  
✅ Visualización de **precios históricos** con gráficas interactivas  
✅ Gráfico de **dividendos** pagados por período  
✅ Panel de **métricas clave** (P/E, ROE, Beta, etc.)  
✅ Recomendación de **analistas** con color contextual  
✅ Opción de **exportar datos a CSV**  
✅ Interfaz adaptable a **modo claro/oscuro**

---

## 🖼️ Captura de Pantalla
![image](https://github.com/user-attachments/assets/6be4678d-11c5-4270-b84e-c06d5091756e)



```bash
🚀 Instalación

    Clona este repositorio:

git clone https://github.com/danielcba/mini_dashboard/
cd mini_dashboard

    Crea un entorno virtual (opcional pero recomendado):

python -m venv env
source env/bin/activate  # En Linux/macOS
env\Scripts\activate     # En Windows

    Instala las dependencias:

pip install -r requirements.txt

    Requisitos principales:

        streamlit

        yfinance

        plotly

        pandas

▶️ Uso

Lanza la aplicación ejecutando:

streamlit run app.py

Luego abre tu navegador en http://localhost:8501
🧠 ¿Cómo Funciona?

El código:

    Usa yfinance para descargar información financiera y precios históricos de cada ticker.

    Muestra métricas clave (P/E, dividendos, ROE, etc.) junto a gráficos dinámicos de precios y dividendos.

    Ofrece herramientas de exportación para análisis posterior.

📁 Exportación de Datos

    Puedes guardar los datos históricos en un archivo CSV desde la barra lateral.

    También se incluye información sobre exportar la vista HTML (requiere herramientas externas).

📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información.

¡Espero que este dashboard te ayude a tomar mejores decisiones financieras! 💰📊
