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
