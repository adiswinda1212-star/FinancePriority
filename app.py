import streamlit as st
import pandas as pd
from ai_analyzer import analyze_transactions
from visualization import generate_donut_chart, generate_ratios
from pdf_generator import generate_pdf_report
from io import BytesIO



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

import os
import pandas as pd
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # Groq endpoint

def classify_transaction_groq(text):
    prompt = f"Klasifikasikan transaksi ini ke salah satu kategori: Kewajiban, Kebutuhan, Tujuan, Keinginan.\nTransaksi: '{text}'\nJawaban:"
    
    try:
        response = openai.ChatCompletion.create(
            model="mixtral-8x7b-32768",  # atau "llama3-70b-8192" jika tersedia
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "Tidak Terkategori"

def analyze_transactions(df):
    df = df.rename(columns=str.lower)

    if 'jumlah' in df.columns:
        df['jumlah'] = df['jumlah'].astype(float)

    transaksi_col = 'transaksi' if 'transaksi' in df.columns else 'deskripsi'
    df['kategori'] = df[transaksi_col].apply(classify_transaction_groq)
    return df[[transaksi_col, 'jumlah', 'kategori']]


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

# Hapus atau komentar bagian ini
# pdf_bytes = generate_pdf_report(...)
# st.download_button(...)

