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
