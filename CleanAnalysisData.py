"""
CleanAnalysisData.py
====================
A Flask web application that allows users to upload Excel files,
visualize data grouped by text columns, and switch between chart types
(Bar, Line, Pie) interactively using Plotly.

Author  : Fady Kamal
Project : service3 — Excel Dashboard
"""

from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px
import html
import re


app = Flask(__name__)


# ─────────────────────────────────────────────
# Global State
# ─────────────────────────────────────────────
all_sheets: dict = {}       # Stores all sheets loaded from the uploaded Excel file
primary_key: str = None     # The column used as a unique identifier per sheet
current_sheet: str = None   # The sheet currently being displayed


# ─────────────────────────────────────────────
# Helper: Detect Primary Key
# ─────────────────────────────────────────────
def detect_primary_key(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Identifies a suitable primary key column in the DataFrame.

    Looks for a column where all values are unique and non-null.
    If none is found, inserts a sequential 'Index' column as a fallback.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        tuple: (modified DataFrame, primary key column name)
    """
    for col in df.columns:
        if df[col].is_unique and df[col].notnull().all():
            return df, col

    # Fallback: add an auto-increment index column
    df.insert(0, "Index", range(1, len(df) + 1))
    return df, "Index"


# ─────────────────────────────────────────────
# Helper: Select Best Text Column for Grouping
# ─────────────────────────────────────────────
def best_text_column(df: pd.DataFrame) -> str | None:
    """
    Selects the most suitable text column to group data by.

    Considers all object/string columns except the primary key,
    and returns the one with the highest frequency of repeated values
    (most meaningful for grouping).

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        str | None: Column name, or None if no text columns exist.
    """
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    text_cols = [c for c in text_cols if c != primary_key]

    if not text_cols:
        return None

    return max(text_cols, key=lambda c: df[c].value_counts().max())


# ─────────────────────────────────────────────
# Core: Recursive Grouping + Chart Generation
# ─────────────────────────────────────────────
def recursive_group(df: pd.DataFrame, chart_type: str = "bar", level: int = 0) -> str:
    """
    Recursively groups the DataFrame by text columns and generates
    an HTML section with a table and an interactive Plotly chart
    for each group.

    Groups are nested: each level removes the grouped column and
    passes the remaining data deeper. Numeric columns are plotted.

    Args:
        df (pd.DataFrame): The data to group and visualize.
        chart_type (str): Chart type — 'bar', 'line', or 'pie'. Default: 'bar'.
        level (int): Current recursion depth (controls heading size h3–h6).

    Returns:
        str: HTML string containing grouped tables and charts.
    """
    col = best_text_column(df)

    # Base case: no more text columns to group by — render as a plain table
    if not col:
        return df.to_html(index=False, escape=True)

    html_output = ""

    for val, group in df.groupby(col, sort=False):
        heading = min(level + 3, 6)
        html_output += f"<h{heading}>{col}: {html.escape(str(val))}</h{heading}>"

        # Recurse into the sub-group (without the current grouping column)
        inner_html = recursive_group(group.drop(columns=[col]), chart_type, level + 1)

        # Build Plotly chart for numeric columns
        numeric_cols = group.select_dtypes(include="number").columns.tolist()
        chart_html = ""

        if numeric_cols:
            x_col = primary_key if primary_key in group.columns else group.columns[0]

            # Select chart type
            if chart_type == "line":
                fig = px.line(group, x=x_col, y=numeric_cols)
            elif chart_type == "pie":
                fig = px.pie(group, names=x_col, values=numeric_cols[0])
            else:
                fig = px.bar(group, x=x_col, y=numeric_cols)

            # Embed chart JSON for client-side re-rendering on type change
            chart_json = fig.to_json()
            chart_id = f"chart-{level}-{re.sub(r'[^a-zA-Z0-9]', '_', str(val))}"
            chart_html = (
                f'<div id="{chart_id}" data-plotly=\'{chart_json}\'>'
                f'{fig.to_html(full_html=False, include_plotlyjs=False)}</div>'
            )

        # Layout: table on the left, chart on the right
        html_output += f"""
        <div style="display:flex; gap:20px; margin-bottom:40px;">
            <div style="width:55%">{inner_html}</div>
            <div style="width:45%">
                <label>نوع الشارت:</label>
                <select class="chart-type-select" data-chart-id="{chart_id}">
                    <option value="bar"  {'selected' if chart_type == 'bar'  else ''}>Bar</option>
                    <option value="line" {'selected' if chart_type == 'line' else ''}>Line</option>
                    <option value="pie"  {'selected' if chart_type == 'pie'  else ''}>Pie</option>
                </select>
                {chart_html}
            </div>
        </div>
        """

    return html_output


# ─────────────────────────────────────────────
# Route: Home — File Upload & Sheet Selection
# ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def home():
    """
    Main route handling two POST stages:
      1. File upload → parses Excel and shows a sheet selector dropdown.
      2. Sheet selection → loads the chosen sheet and renders the dashboard.

    Returns:
        str: Rendered HTML page.
    """
    global all_sheets, primary_key, current_sheet
    content = ""

    if request.method == "POST":

        # ── Stage 1: Handle Excel file upload ──
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
                        # Build a dropdown for sheet selection
                        sheet_options = "".join(
                            f"<option value='{s}'>{s}</option>"
                            for s in all_sheets.keys()
                        )
                        content = f"""
                        <form method='POST'>
                            اختر الشيت:
                            <select name='sheet_name' required>
                                {sheet_options}
                            </select>
                            <button type='submit'>عرض البيانات</button>
                        </form>
                        """
                        return render_template_string(HTML_TEMPLATE, content=content)

                except Exception as e:
                    content = f"<h3 style='color:red;'>Error: {e}</h3>"

        # ── Stage 2: Handle sheet selection & render dashboard ──
        if "sheet_name" in request.form:
            current_sheet = request.form["sheet_name"]

            if current_sheet in all_sheets:
                df = all_sheets[current_sheet]
                df, primary_key = detect_primary_key(df)
                content = recursive_group(df)

    return render_template_string(HTML_TEMPLATE, content=content)


# ─────────────────────────────────────────────
# HTML Template
# ─────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Excel Dashboard</title>
    <!-- Plotly for interactive charts -->
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
/**
 * Chart Type Switcher
 * -------------------
 * Listens for changes on any chart-type dropdown.
 * Re-renders the associated Plotly chart using the stored JSON data
 * without making a server request.
 */
document.querySelectorAll('.chart-type-select').forEach(sel => {
    sel.addEventListener('change', function () {
        const chartDivId = this.dataset.chartId;
        const type       = this.value;
        const chartDiv   = document.getElementById(chartDivId);
        const data       = JSON.parse(chartDiv.dataset.plotly);

        if (type === 'bar') {
            Plotly.react(chartDiv, data.data, data.layout);

        } else if (type === 'line') {
            const newData = data.data.map(d => ({
                ...d,
                type: 'scatter',
                mode: 'lines+markers'
            }));
            Plotly.react(chartDiv, newData, data.layout);

        } else if (type === 'pie') {
            if (data.data.length >= 1) {
                const pieData = data.data.map(d => ({ ...d, type: 'pie' }));
                Plotly.react(chartDiv, pieData, data.layout);
            }
        }
    });
});
</script>

</body>
</html>
"""


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)