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
