from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px
import html
import re

app = Flask(__name__)

# تخزين البيانات بعد الرفع
df_dict = {}      # كل شيت كـ DataFrame
PRIMARY_KEY = None
selected_sheet = None

# =============================
# تحديد Primary Key تلقائي
# =============================
def detect_primary_key(dataframe):
    for col in dataframe.columns:
        if dataframe[col].is_unique and dataframe[col].notnull().all():
            return dataframe, col
    dataframe.insert(0, "Index", range(1, len(dataframe) + 1))
    return dataframe, "Index"

# =============================
# اختيار أفضل عمود نصي
# =============================
def get_best_text_column(dataframe):
    text_cols = dataframe.select_dtypes(include="object").columns.tolist()
    text_cols = [c for c in text_cols if c != PRIMARY_KEY]
    if not text_cols:
        return None
    return max(text_cols, key=lambda c: dataframe[c].value_counts().max())

# =============================
# Recursive Grouping + Charts
# =============================
def recursive_group(dataframe, chart_type="bar", level=0):
    group_column = get_best_text_column(dataframe)
    if not group_column:
        return dataframe.to_html(index=False, escape=True)

    final_html = ""
    for value, group in dataframe.groupby(group_column, sort=False):
        heading_size = min(level + 3, 6)
        final_html += f"<h{heading_size}>{group_column}: {html.escape(str(value))}</h{heading_size}>"

        inner_html = recursive_group(group.drop(columns=[group_column]), chart_type, level + 1)

        numeric_cols = group.select_dtypes(include="number").columns.tolist()
        chart_html = ""
        if numeric_cols:
            x_column = PRIMARY_KEY if PRIMARY_KEY in group.columns else group.columns[0]
            if chart_type == "line":
                fig = px.line(group, x=x_column, y=numeric_cols)
            elif chart_type == "pie":
                fig = px.pie(group, names=x_column, values=numeric_cols[0])
            else:
                fig = px.bar(group, x=x_column, y=numeric_cols)

            chart_json = fig.to_json()
            chart_id = f"chart-{level}-{re.sub(r'[^a-zA-Z0-9]', '_', str(value))}"
            chart_html = f'<div id="{chart_id}" data-plotly=\'{chart_json}\'>{fig.to_html(full_html=False, include_plotlyjs=False)}</div>'

        final_html += f"""
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
    return final_html

# =============================
# الصفحة الرئيسية
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    global df_dict, PRIMARY_KEY, selected_sheet
    content = ""
    sheet_options_html = ""

    # رفع الملف
    if request.method == "POST":
        if 'excel_file' in request.files:
            file = request.files['excel_file']
            if file.filename != "":
                try:
                    excel_file = pd.ExcelFile(file)
                    df_dict = {}
                    for sheet in excel_file.sheet_names:
                        temp_df = pd.read_excel(excel_file, sheet_name=sheet)
                        if not temp_df.empty:
                            df_dict[sheet] = temp_df

                    if not df_dict:
                        content = "<h3 style='color:red;'>الملف لا يحتوي على بيانات</h3>"
                    else:
                        # عرض dropdown لاختيار الشيت
                        sheet_options_html = "<select name='sheet_name' required>"
                        for s in df_dict.keys():
                            sheet_options_html += f"<option value='{s}'>{s}</option>"
                        sheet_options_html += "</select>"
                        content = f"""
                        <form method="POST">
                            اختر الشيت: {sheet_options_html}
                            <button type="submit">عرض البيانات</button>
                        </form>
                        """
                        return render_template_string(HTML_TEMPLATE, content=content)

                except Exception as e:
                    content = f"<h3 style='color:red;'>Error: {e}</h3>"
                    print("ERROR:", e)

    # بعد اختيار الشيت
    if request.method == "POST" and 'sheet_name' in request.form:
        selected_sheet = request.form['sheet_name']
        if selected_sheet in df_dict:
            df = df_dict[selected_sheet]
            df, PRIMARY_KEY = detect_primary_key(df)
            content = recursive_group(df)

    return render_template_string(HTML_TEMPLATE, content=content)

# =============================
# قالب HTML
# =============================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Upload Excel Dashboard</title>
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