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
