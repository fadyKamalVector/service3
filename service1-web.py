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
    host="127.0.0.1",   # or "localhost"
    user="root",        # change if needed
    password="@dm1n",        # add your MySQL password
    database="classicmodels"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)


# ---------------- CSV + Excel files ----------------
CSV_FILE = CSV_FILE = r"E:\PythonProject\insurance.csv"     # put your CSV file here
XLS_FILE = "data.xlsx"    # put your Excel file here


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


# ---------------- HTTP Handler ----------------
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- MongoDB ---
        mongo_users = list(mongo_collection.find({}, {"_id": 0}))

        # --- MySQL ---
        mysql_cursor.execute("SHOW TABLES")
        tables = [row[f"Tables_in_{mysql_conn.database}"] for row in mysql_cursor.fetchall()]

        ## print("tables ", tables)
        mysql_data = {}
        for table in tables:
            mysql_cursor.execute(f"SELECT * FROM {table}")
            rows = mysql_cursor.fetchall()
            mysql_data[table] = rows
            ## print("sql data ", mysql_data[table])

        # --- CSV + XLS ---
        csv_data = read_csv_data()
        xls_data = read_xls_data()

        # --- Determine status ---
        has_mongo = bool(mongo_users)
        has_mysql = any(mysql_data.values())
        has_csv = bool(csv_data)
        has_xls = bool(xls_data)

        sources = []
        if has_mongo: sources.append("MongoDB")
        if has_mysql: sources.append("MySQL")
        if has_csv: sources.append("CSV")
        if has_xls: sources.append("Excel")

        if not sources:
            status = "No data found in any source"
        else:
            status = "Data found in: " + ", ".join(sources)

        # --- Build response ---
        response = {
            "status": status,
            "mongo_data": mongo_users,
            "mysql_data": mysql_data,
            "csv_data": csv_data,
            "xls_data": xls_data
        }

        # --- Send response ---
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))
        self.wfile.write(json.dumps(response, indent=2, default=str).encode("utf-8"))


# ---------------- Server ----------------
class MyServer:
    def __init__(self, host="127.0.0.1", port=8000):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, MyHandler)

    def start(self):
        print(f"Server running on http://{self.server_address[0]}:{self.server_address[1]}")
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        print("Server stopped.")


if __name__ == "__main__":
    server = MyServer(port=9090)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
