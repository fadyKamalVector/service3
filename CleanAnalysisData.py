from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px
import html
import re

app = Flask(__name__)

# ===========================
# المتغيرات العامة
# ===========================
all_sheets = {}  # كل شيت مخزن هنا
primary_key = None
current_sheet = None

# ===========================
# دالة لتحديد Primary Key
# ===========================
def detect_primary_key(df):
    for col in df.columns:
        if df[col].is_unique and df[col].notnull().all():
            return df, col
    # لو مفيش عمود مناسب، نضيف عمود Index
    df.insert(0, "Index", range(1, len(df) + 1))
    return df, "Index"

# ===========================
# دالة لاختيار أفضل عمود نصي للتجميع
# ===========================
def best_text_column(df):
    # text_cols = df.select_dtypes(include="object").columns.tolist()
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    text_cols = [c for c in text_cols if c != primary_key]
    if not text_cols:
        return None
    # العمود اللي عنده أكتر تكرار لقيمه
    return max(text_cols, key=lambda c: df[c].value_counts().max())

# ===========================
# دالة التجميع recursive
# ===========================
def recursive_group(df, chart_type="bar", level=0):
    col = best_text_column(df)
    if not col:
        return df.to_html(index=False, escape=True)

    html_output = ""

    for val, group in df.groupby(col, sort=False):
        heading = min(level+3, 6)
        html_output += f"<h{heading}>{col}: {html.escape(str(val))}</h{heading}>"

        # تجميع داخلي
        inner_html = recursive_group(group.drop(columns=[col]), chart_type, level+1)

        # الأعمدة الرقمية
        numeric_cols = group.select_dtypes(include="number").columns.tolist()
        chart_html = ""
        if numeric_cols:
            x_col = primary_key if primary_key in group.columns else group.columns[0]

            # اختيار نوع الشارت
            if chart_type == "line":
                fig = px.line(group, x=x_col, y=numeric_cols)
            elif chart_type == "pie":
                fig = px.pie(group, names=x_col, values=numeric_cols[0])
            else:
                fig = px.bar(group, x=x_col, y=numeric_cols)

            chart_json = fig.to_json()
            chart_id = f"chart-{level}-{re.sub(r'[^a-zA-Z0-9]', '_', str(val))}"
            chart_html = f'<div id="{chart_id}" data-plotly=\'{chart_json}\'>{fig.to_html(full_html=False, include_plotlyjs=False)}</div>'

        html_output += f"""
        <div style="display:flex; gap:20px; margin-bottom:40px;">
            <div style="width:55%">{inner_html}</div>
            <div style="width:45%">
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
    return html_output

# ===========================
# الصفحة الرئيسية
# ===========================
@app.route("/", methods=["GET", "POST"])
def home():
    global all_sheets, primary_key, current_sheet
    content = ""
    sheet_dropdown = ""

    # رفع الملف
    if request.method == "POST":
        if "excel_file" in request.files:
            file = request.files["excel_file"]
            if file.filename != "":
                try:
                    xls = pd.ExcelFile(file)
                    all_sheets = {}
                    for sheet in xls.sheet_names:
                        df_temp = pd.read_excel(xls, sheet_name=sheet)
                        if not df_temp.empty:
                            all_sheets[sheet] = df_temp

                    if not all_sheets:
                        content = "<h3 style='color:red;'>الملف لا يحتوي على بيانات</h3>"
                    else:
                        # dropdown لاختيار الشيت
                        sheet_dropdown = "<select name='sheet_name' required>"
                        for s in all_sheets.keys():
                            sheet_dropdown += f"<option value='{s}'>{s}</option>"
                        sheet_dropdown += "</select>"
                        content = f"""
                        <form method='POST'>
                            اختر الشيت: {sheet_dropdown}
                            <button type='submit'>عرض البيانات</button>
                        </form>
                        """
                        return render_template_string(HTML_TEMPLATE, content=content)

                except Exception as e:
                    content = f"<h3 style='color:red;'>Error: {e}</h3>"

    # بعد اختيار الشيت
    if request.method == "POST" and "sheet_name" in request.form:
        current_sheet = request.form["sheet_name"]
        if current_sheet in all_sheets:
            df = all_sheets[current_sheet]
            df, primary_key = detect_primary_key(df)
            content = recursive_group(df)

    return render_template_string(HTML_TEMPLATE, content=content)

# ===========================
# قالب HTML
# ===========================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Excel Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
</head>
<body>
<h2>ارفع ملف Excel</h2>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="excel_file" accept=".xlsx,.xls" required>
    <button type="submit">Upload</button>
</form>
<hr>
{{ content|safe }}

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

if __name__ == "__main__":
    app.run(debug=True)