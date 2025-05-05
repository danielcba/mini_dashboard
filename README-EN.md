# 📈 Stock Dashboard (ticker)

An interactive web app built with [Streamlit](https://streamlit.io/) that allows users to dynamically explore **financial metrics**, **historical prices**, and **dividends** for both local and international stocks. Perfect for investment tracking and stock analysis 📊.

---

## 🧰 Features

✅ Multi-select support for **stock tickers**  
✅ Interactive charts for **historical price trends**  
✅ **Dividends chart** per period  
✅ Panel of **key financial metrics** (P/E, ROE, Beta, etc.)  
✅ Analyst **recommendation** with color indicators  
✅ **CSV export** functionality  
✅ Responsive interface with **dark/light mode**

---

## 🖼️ Screenshot

![image](https://github.com/user-attachments/assets/3b6bec4a-5537-4fcd-b923-ebaeb5ee8f53)


```bash
🚀 Installation

    Clone this repository:

git clone https://github.com/danielcba/mini_dashboard.git
cd /danielcba/mini_dashboard

    (Optional) Create a virtual environment:

python -m venv env
source env/bin/activate  # On Linux/macOS
env\Scripts\activate     # On Windows

    Install dependencies:

pip install -r requirements.txt

    Main packages:

        streamlit

        yfinance

        plotly

        pandas

▶️ Usage

Run the app locally with:

streamlit run app.py

Then open your browser at http://localhost:8501
🧠 How It Works

The app:

    Uses yfinance to fetch financial data and historical prices for each selected ticker.

    Displays a set of key metrics (P/E, dividends, ROE, etc.) along with dynamic price and dividend charts.

    Includes export options for offline analysis.

📁 Data Export

    You can export historical stock data as a CSV file via the sidebar.

    Exporting the app as HTML is mentioned (requires external tools like streamlit-logger).

📝 License

This project is licensed under the MIT License. See the LICENSE file for more details.

