import json
import numpy as np
import pandas as pd
from scipy import stats
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector

# --- إعدادات قاعدة البيانات ---
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "@dm1n",
    "database": "classicmodels"
}

class DataProcessor:
    @staticmethod
    def clean_and_export(df):
        if df.empty:
            return []

        for col in df.columns:
            null_count = df[col].isnull().sum()
            
            if null_count > 0:
                # منطق تحديد هل العمود هو مفتاح (PK/FK)
                # أي عمود يحتوي على 'id' أو 'code' أو 'number' أو ينتهي بـ 'no'
                is_key = any(x in col.lower() for x in ["id", "code", "number", "pk", "fk"])

                # 1. إذا كان العمود رقمي (Numeric)
                if pd.api.types.is_numeric_dtype(df[col]):
                    # إذا كان مفتاح PK أو FK -> نضع 0 ولا نحسب المتوسط
                    if is_key:
                        df[col] = df[col].fillna(0)
                    
                    # إذا كان كمية (Quantity/Qty) -> إخفاء (Hidden)
                    elif any(x in col.lower() for x in ["qty", "quantity"]):
                        df[col] = "Hidden"
                    
                    # إذا كان قيمة مالية أو غير ذلك (Float) -> نحسب المتوسط أو الوسيط
                    elif pd.api.types.is_float_dtype(df[col]):
                        non_null = df[col].dropna()
                        if len(non_null) > 1:
                            z = np.abs(stats.zscore(non_null.astype(float)))
                            if len(non_null[z > 3]) > 0:
                                df[col] = df[col].fillna(df[col].median())
                            else:
                                df[col] = df[col].fillna(df[col].mean())

                # 2. إذا كان العمود نصي (String/Object)
                elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                    # إذا كان مفتاح نصي -> unavailable
                    if is_key:
                        df[col] = df[col].fillna("unavailable")
                    # إذا كان وصف أو تعليق -> None
                    elif any(x in col.lower() for x in ["desc", "comment"]):
                        df[col] = df[col].fillna("None")
                    else:
                        df[col] = df[col].fillna("N/A")
                
                # 3. التاريخ -> إخفاء
                elif "date" in col.lower() or pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = "Date Hidden"

        # تصدير الملفات لعام 2026
        df.to_csv("clean_analysis_data.csv", index=False, encoding='utf-8-sig')
        df.to_excel("clean_analysis_data.xlsx", index=False, engine='openpyxl')
        
        return df.to_dict(orient="records")

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        conn = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True, buffered=True)
            
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]

            all_dfs = []
            for table in tables:
                cursor.execute(f"SELECT * FROM `{table}`")
                rows = cursor.fetchall()
                if rows:
                    temp_df = pd.DataFrame(rows)
                    temp_df.insert(0, "ORIGIN_TABLE", table)
                    all_dfs.append(temp_df)

            if not all_dfs:
                raise ValueError("No data found")

            # دمج الجداول (Full Merge)
            combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)
            
            # التنظيف والتصدير
            cleaned_data = DataProcessor.clean_and_export(combined_df)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(cleaned_data, default=str).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode("utf-8"))
        finally:
            if conn and conn.is_connected():
                conn.close()

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8081), MyHandler)
    print("Server : 127.0.0.1:8081")
    server.serve_forever()
