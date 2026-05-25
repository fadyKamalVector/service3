from flask import Flask, render_template_string
import pandas as pd
import html

app = Flask(__name__)

file_path = r"E:\MyWorkspace\project\python.project\ReadData\Second Dashboard.xlsx"
df = pd.read_excel(file_path, sheet_name="Data")

df.insert(0, "Index", range(1, len(df) + 1))

def clean_and_identify(df):
    # 1. تحديد الـ Primary Key (العمود الذي لا يتكرر وقيمه فريدة)
    potential_pks = [col for col in df.columns if df[col].is_unique and df[col].notnull().all()]
    pk = potential_pks[0] if potential_pks else "Index"

    # 2. تنظيف البيانات "العادية" (مثل الأعمار أو الأسماء)
    # لا نريد عمل تنظيف للـ Primary Key لأنه معرف فريد
    for col in df.columns:
        if col == pk:
            continue  # اترك المفتاح الأساسي كما هو
            
        # إذا كان العمود رقمي (مثل العمر)
        if pd.api.types.is_numeric_dtype(df[col]):
            # ملء القيم الفارغة بمتوسط العمر مثلاً
            df[col] = df[col].fillna(df[col].mean())
            
        # إذا كان العمود نصي (وصف)
        elif pd.api.types.is_object_dtype(df[col]):
            # إزالة المسافات الزائدة وتوحيد حالة الأحرف
            df[col] = df[col].astype(str).str.strip()
            
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
    return max(valid_cols, key=lambda col: df[col].value_counts().max())

# def best_text_column(df):
#     text_cols = df.select_dtypes(include='object').columns.tolist()
#     if not text_cols:
#         return None
#     return max(text_cols, key=lambda col: df[col].value_counts().max())

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
