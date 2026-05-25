from flask import Flask, render_template_string
from markupsafe import Markup
import pandas as pd
import html
import plotly.express as px

app = Flask(__name__)

# قراءة الإكسل
file_path = r"E:\MyWorkspace\project\python.project\ReadData\Second Dashboard.xlsx"
df = pd.read_excel(file_path, sheet_name="Data").copy()

# دالة تنظيف وتحديد Primary Key
def clean_and_identify(df):
    df = df.copy()
    potential_pks = [col for col in df.columns if df[col].is_unique and df[col].notnull().all()]

    if "Index" in potential_pks:
        pk = "Index"
    elif "id" in potential_pks:
        pk = "id"
    elif "code" in potential_pks:
        pk = "code"
    elif potential_pks:
        pk = potential_pks[0]
    else:
        pk = "Index"
        df.insert(0, "Index", range(1, len(df) + 1))

    for col in df.columns:
        if col == pk:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
        elif pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].where(df[col].notna(), None)

    return df, pk

df, primary_key = clean_and_identify(df)

# دالة اختيار أفضل عمود نصي للتجميع
def best_text_column(df):
    text_cols = df.select_dtypes(include='object').columns.tolist()
    valid_cols = [c for c in text_cols if c != primary_key]
    if not valid_cols:
        return None
    return max(valid_cols, key=lambda col: df[col].fillna("").value_counts().max())

# دالة التجميع المتداخل مع شارت لكل جروب
def recursive_group(df, level=0):
    col = best_text_column(df)

    # ✅ لو مفيش أعمدة نصية: ده آخر مستوى → جدول فقط
    if not col:
        return df.to_html(index=False, escape=True)

    html_out = ""

    for name, group in df.groupby(col, sort=False):
        html_out += f"<h{min(level+3,6)}>{html.escape(col)}: {html.escape(str(name))}</h{min(level+3,6)}>"

        # الأعمدة الرقمية
        numeric_cols = group.select_dtypes(include='number').columns.tolist()

        # الشارت
        chart_html = ""
        if numeric_cols:
            fig = px.bar(
                group,
                x=group.columns[0],
                y=numeric_cols,
                title=f"{col}: {name}"
            )
            chart_html = fig.to_html(full_html=False)

        # 👈 هنا بس نلف الجدول النهائي + الشارت
        inner_html = recursive_group(group.drop(columns=[col]), level+1)

        html_out += f"""
        <div class="row">
            <div class="table-box">
                {inner_html}
            </div>
            <div class="chart-box">
                {chart_html}
            </div>
        </div>
        """

    return html_out


# قالب HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>عرض البيانات مع شارت</title>
    <style>
        body { font-family: Arial; }
        table, th, td {
            border:1px solid #333;
            border-collapse:collapse;
            padding:6px;
            font-size:12px;
        }
        th { background:#eee; }

        .row {
            display: flex;
            gap: 20px;
            margin-bottom: 40px;
            align-items: flex-start;
        }

        .table-box {
            width: 55%;
            overflow-x: auto;
        }

        .chart-box {
            width: 45%;
            border: 2px solid #000;
            padding: 10px;
        }

        h3,h4,h5,h6 {
            margin-top: 30px;
        }
    </style>

</head>
<body>
    <h2>بيانات الإكسل مجمعة مع شارت</h2>
    {{ table | safe }}
</body>
</html>
"""

@app.route("/")
def show_data():
    table_html = recursive_group(df)
    return render_template_string(HTML_TEMPLATE, table=table_html)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
