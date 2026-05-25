from flask import Flask, render_template_string
import pandas as pd
import html

app = Flask(__name__)

file_path = r"E:\MyWorkspace\project\python.project\ReadData\Second Dashboard.xlsx"
df = pd.read_excel(file_path, sheet_name="Data")

def clean_and_identify(df):
    df = df.copy()  # نسخ الداتا الأصلية لتجنب تعديلها
    # 1. تحديد الأعمدة الفريدة الممكنة للـ Primary Key
    potential_pks = [col for col in df.columns if df[col].is_unique and df[col].notnull().all()]

    # 2. اختيار الأفضل:
    if "Index" in potential_pks:
        pk = "Index"
    elif "id" in potential_pks:
        pk = "id"
    elif "code" in potential_pks:
        pk = "code"
    elif potential_pks:
        pk = potential_pks[0]  # أي عمود فريد آخر
    else:
        pk = None  # لو مفيش أعمدة فريدة
        df.insert(0, "Index", range(1, len(df) + 1))
        pk = "Index"

    # 3. تنظيف باقي الأعمدة
    for col in df.columns:
        if col == pk:
            continue  # اترك المفتاح الأساسي كما هو
        
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())

        elif pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].where(df[col].notna(), None)


    return df, pk

# تطبيق التنظيف قبل التشغيل
df, primary_key = clean_and_identify(df)

def best_text_column(df):
    # نعدل الدالة بحيث لا تختار الـ Primary Key لعمل GroupBy عليه
    text_cols = df.select_dtypes(include='object').columns.tolist()
    # استبعاد الـ Primary Key من التجميع لأنه فريد ولن يجمع شيئاً
    valid_cols = [c for c in text_cols if c != primary_key]
    
    if not valid_cols:
        return None
    # نختار العمود الذي يحتوي على أكثر قيم متكررة (Foreign Key محتمل أو تصنيف)
    return max(valid_cols, key=lambda col: df[col].fillna("").value_counts().max())

def recursive_group(df, level=0):
    col = best_text_column(df)
    if not col:
        return df.to_html(index=False, escape=True)

    html_out = ""
    for name, group in df.groupby(col, sort=False):
        html_out += f"<h{min(level+3,6)}>{html.escape(col)}: {html.escape(str(name))}</h{min(level+3,6)}>"
        html_out += recursive_group(group.drop(columns=[col]), level+1)

    return html_out


# 👈 لازم يكون هنا قبل أي route
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>عرض البيانات</title>
    <style>
        table, th, td { border:1px solid #333; border-collapse:collapse; padding:6px; }
        th { background:#eee; }
    </style>
</head>
<body>
    <h2>بيانات الإكسل مجمعة</h2>
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
