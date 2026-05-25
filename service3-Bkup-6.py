from flask import Flask, render_template_string, request
import pandas as pd
import html
import plotly.express as px
import re

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
def recursive_group(df, chart_type="bar", level=0):
    col = best_text_column(df)

    if not col:
        return df.to_html(index=False, escape=True)

    html_out = ""
    for name, group in df.groupby(col, sort=False):
        html_out += f"<h{min(level+3,6)}>{html.escape(col)}: {html.escape(str(name))}</h{min(level+3,6)}>"

        numeric_cols = group.select_dtypes(include='number').columns.tolist()
        inner_html = recursive_group(group.drop(columns=[col]), chart_type, level+1)

        chart_html = ""
        chart_id = f"chart-{level}-{re.sub(r'[^a-zA-Z0-9]', '_', str(name))}"
        x_col = primary_key if primary_key in group.columns else group.columns[0]

        if numeric_cols:
            # Pie chart special handling: aggregate values per group
            if chart_type == "pie":
                pie_data = group.groupby(col)[numeric_cols[0]].sum().reset_index()
                fig = px.pie(pie_data, names=col, values=numeric_cols[0], title=f"{col}: {name}")
            elif chart_type == "bar":
                fig = px.bar(group, x=x_col, y=numeric_cols, title=f"{col}: {name}")
            elif chart_type == "line":
                fig = px.line(group, x=x_col, y=numeric_cols, title=f"{col}: {name}")
            else:
                fig = px.bar(group, x=x_col, y=numeric_cols, title=f"{col}: {name}")

            chart_json = fig.to_json()
            chart_html = f'<div id="{chart_id}" data-plotly=\'{chart_json}\'>{fig.to_html(full_html=False, include_plotlyjs=False)}</div>'

        html_out += f"""
        <div class="row">
            <div class="table-box">{inner_html}</div>
            <div class="chart-box">
                <label>نوع الشارت:</label>
                <select class="chart-type-select" data-chart-id="{chart_id}">
                    <option value="bar" {'selected' if chart_type=='bar' else ''}>Bar</option>
                    <option value="line" {'selected' if chart_type=='line' else ''}>Line</option>
                    <option value="pie" {'selected' if chart_type=='pie' else ''}>Pie</option>
                </select>
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
        table, th, td { border:1px solid #333; border-collapse:collapse; padding:6px; font-size:12px; }
        th { background:#eee; }

        .row { display:flex; gap:20px; margin-bottom:40px; align-items:flex-start; }
        .table-box { width:55%; overflow-x:auto; }
        .chart-box { width:45%; border:2px solid #000; padding:10px; }
        h3,h4,h5,h6 { margin-top:30px; }
    </style>

    <!-- أحدث نسخة Plotly -->
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
</head>
<body>

<h2>بيانات الإكسل مجمعة مع شارت</h2>

{{ table | safe }}

<script>
document.querySelectorAll('.chart-type-select').forEach(sel => {
    sel.addEventListener('change', function() {
        const chartDivId = this.dataset.chartId;
        const type = this.value;
        const chartDiv = document.getElementById(chartDivId);
        const data = JSON.parse(chartDiv.dataset.plotly);

        if (type === 'bar') {
            Plotly.react(chartDiv, data.data, data.layout);
        } else if (type === 'line') {
            const newData = data.data.map(d => ({...d, type:'scatter', mode:'lines+markers'}));
            Plotly.react(chartDiv, newData, data.layout);
        } else if (type === 'pie') {
            if (data.data.length >= 1) {
                const pieData = data.data.map(d => ({...d, type:'pie'}));
                Plotly.react(chartDiv, pieData, data.layout);
            }
        }
    });
});
</script>

</body>
</html>
"""

@app.route("/")
def show_data():
    chart_type = request.args.get("chart_type", "bar")
    table_html = recursive_group(df, chart_type)
    return render_template_string(
        HTML_TEMPLATE,
        table=table_html,
        selected_chart=chart_type
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)