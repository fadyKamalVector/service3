from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

# قراءة الإكسل
file_path = r"E:\MyWorkspace\project\python.project\ReadData\Second Dashboard.xlsx"
df = pd.read_excel(file_path, sheet_name="Data")

# إضافة عمود "Index" بالترقيم العام
df.insert(0, "Index", range(1, len(df) + 1))

# --- دالة لإيجاد العمود الأنسب للتجميع ---
def best_text_column(df):
    text_cols = df.select_dtypes(include='object').columns.tolist()
    if not text_cols:
        return None
    return max(text_cols, key=lambda col: df[col].value_counts().max())

# --- دالة لعمل التجميع المتداخل ---
def recursive_group(df, level=0):
    col = best_text_column(df)
    if not col:
        # لو مفيش أعمدة نصية متبقية، ارجع الداتا كجدول
        return df.to_html(index=False)
    
    grouped = df.groupby(col)
    html = ""
    for name, group in grouped:
        indent = "&nbsp;" * 4 * level  # مسافة للتعشيش
        html += f"<h{level+3}>{indent}{col}: {name}</h{level+3}>"
        # استدعاء دالة التجميع recursively على المجموعة
        html += recursive_group(group.drop(columns=[col]), level=level+1)
    return html

# إنشاء HTML كامل
tables_html = recursive_group(df)

# قالب HTML مباشر
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>عرض الداتا مجمعة تلقائي</title>
    <style>
        table, th, td { border: 1px solid black; border-collapse: collapse; padding: 5px; }
        th { background-color: #f2f2f2; }
        h3,h4,h5,h6 { margin: 5px 0 0 0; }
    </style>
</head>
<body>
    <h2>بيانات الإكسل مجمعة تلقائيًا</h2>
    {{ table|safe }}
</body>
</html>
"""

@app.route("/")
def show_data():
    return render_template_string(html_template, table=tables_html)

if __name__ == "__main__":
    app.run(debug=True)
