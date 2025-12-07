import streamlit as st
import pandas as pd
from ai_analyzer import analyze_transactions
from visualization import generate_donut_chart, generate_ratios
from pdf_generator import generate_pdf_report
from io import BytesIO

# LOAD ENV (GROQ) 
############################################# 
load_dotenv() 
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
if GROQ_API_KEY: 
from groq import Groq 
client = Groq(api_key=GROQ_API_KEY) 
else: 
client = None 
#############################################

st.set_page_config(page_title="Prioritas Keuangan", layout="wide")

st.title("📊 Aplikasi Prioritas Keuangan - T-K-K-K")

uploaded_file = st.file_uploader("Unggah File Excel Laporan Bank", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.subheader("🧾 Data Mentah")
    st.dataframe(df.head())

    st.info("🔍 Menganalisis dan mengklasifikasikan transaksi dengan AI... (mock)")
    df_analyzed = analyze_transactions(df)

    st.subheader("📌 Hasil Klasifikasi T-K-K-K")
    st.dataframe(df_analyzed)

    # Visualisasi Donut
    st.subheader("📈 Alokasi Pengeluaran (Donut Chart)")
    donut_fig = generate_donut_chart(df_analyzed)
    st.plotly_chart(donut_fig, use_container_width=True)

    # Rasio Finansial
    st.subheader("📊 Rasio Keuangan")
    ratios = generate_ratios(df_analyzed)
    st.json(ratios)

    # Export PDF
    st.subheader("📤 Ekspor Laporan PDF")
    if st.button("Generate Laporan PDF"):
        pdf_bytes = generate_pdf_report(df_analyzed, ratios)
        st.success("✅ Laporan berhasil dibuat.")
        st.download_button("📥 Unduh PDF", data=pdf_bytes, file_name="laporan_keuangan.pdf")

import pandas as pd

def classify_transaction(text):
    text = text.lower()
    if any(word in text for word in ['cicilan', 'angsuran', 'kredit']):
        return "Kewajiban"
    elif any(word in text for word in ['listrik', 'air', 'makan', 'transport']):
        return "Kebutuhan"
    elif any(word in text for word in ['tabungan', 'investasi', 'dana']):
        return "Tujuan"
    else:
        return "Keinginan"

def analyze_transactions(df):
    df = df.rename(columns=str.lower)

    # Normalisasi kolom
    if 'jumlah' in df.columns:
        df['jumlah'] = df['jumlah'].astype(float)
    elif 'debit' in df.columns and 'kredit' in df.columns:
        df['jumlah'] = df['debit'].fillna(0) - df['kredit'].fillna(0)

    if 'transaksi' in df.columns:
        df['kategori'] = df['transaksi'].apply(classify_transaction)
    elif 'deskripsi' in df.columns:
        df['kategori'] = df['deskripsi'].apply(classify_transaction)
    else:
        df['kategori'] = 'Lainnya'

    return df[['transaksi', 'jumlah', 'kategori']] if 'transaksi' in df.columns else df[['deskripsi', 'jumlah', 'kategori']]

import plotly.express as px

def generate_donut_chart(df):
    summary = df.groupby('kategori')['jumlah'].sum().abs().reset_index()
    fig = px.pie(summary, names='kategori', values='jumlah', hole=0.4, title="Distribusi T-K-K-K")
    return fig

def generate_ratios(df):
    total = df['jumlah'].abs().sum()
    ratios = {}
    for kategori in ['Kewajiban', 'Kebutuhan', 'Tujuan', 'Keinginan']:
        subset = df[df['kategori'] == kategori]
        amount = subset['jumlah'].abs().sum()
        ratios[f"{kategori}/Total"] = f"{(amount/total*100):.2f}%"
    return ratios

from jinja2 import Template
from weasyprint import HTML
from io import BytesIO

def generate_pdf_report(df, ratios):
    html_template = """
    <html>
    <head><style>
        body { font-family: Arial; padding: 20px; }
        h1 { color: #2C3E50; }
        table, th, td { border: 1px solid #ddd; border-collapse: collapse; padding: 8px; }
    </style></head>
    <body>
        <h1>Laporan Keuangan</h1>
        <h2>Rasio T-K-K-K</h2>
        <ul>
            {% for key, value in ratios.items() %}
                <li><b>{{ key }}</b>: {{ value }}</li>
            {% endfor %}
        </ul>
        <h2>Transaksi Terklasifikasi</h2>
        <table>
            <tr>
                {% for col in df.columns %}
                <th>{{ col }}</th>
                {% endfor %}
            </tr>
            {% for row in df.itertuples() %}
            <tr>
                {% for cell in row[1:] %}
                <td>{{ cell }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    template = Template(html_template)
    rendered_html = template.render(df=df, ratios=ratios)
    pdf_file = BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    return pdf_file.getvalue()
