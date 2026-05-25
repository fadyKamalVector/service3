import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import mysql.connector
import pandas as pd


# ---------------- MongoDB connection ----------------
uri = "mongodb+srv://my_data_db_user:6uXb04zphXibtPVD@cluster0.3affxhs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = mongo_client["test_n8n_data"]
mongo_collection = mongo_db["user"]


# ---------------- MySQL connection ----------------
mysql_conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="@dm1n",
    database="classicmodels"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)


# ---------------- CSV + Excel files ----------------
CSV_FILE = r"E:\PythonProject\insurance.csv"
XLS_FILE = "data.xlsx"


def read_csv_data():
    try:
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"CSV read error: {e}")
        return []


def read_xls_data():
    try:
        df = pd.read_excel(XLS_FILE)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"XLS read error: {e}")
        return []


def add_source_first(source, row):
    """Put _source as the first key"""
    return {"_source": source, **row}


# ---------------- HTTP Handler ----------------
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        all_data = []

        # ---------- MongoDB ----------
        mongo_users = list(mongo_collection.find({}, {"_id": 0}))
        for row in mongo_users:
            all_data.append(add_source_first("MongoDB", row))

        # ---------- MySQL ----------
        mysql_cursor.execute("SHOW TABLES")
        tables = [row[f"Tables_in_{mysql_conn.database}"] for row in mysql_cursor.fetchall()]

        for table in tables:
            mysql_cursor.execute(f"SELECT * FROM {table}")
            rows = mysql_cursor.fetchall()
            for row in rows:
                all_data.append(add_source_first(f"MySQL:{table}", row))

        # ---------- CSV ----------
        csv_data = read_csv_data()
        for row in csv_data:
            all_data.append(add_source_first("CSV", row))

        # ---------- Excel ----------
        xls_data = read_xls_data()
        for row in xls_data:
            all_data.append(add_source_first("Excel", row))

        # ---------- Response ----------
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(all_data, default=str).encode("utf-8"))


# ---------------- Server ----------------
class MyServer:
    def __init__(self, host="127.0.0.1", port=8080):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, MyHandler)

    def start(self):
        print(f"Server running on http://{self.server_address[0]}:{self.server_address[1]}")
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        print("Server stopped.")


if __name__ == "__main__":
    server = MyServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
