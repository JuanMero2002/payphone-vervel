"""
NODE/// — Función serverless: entrega token y storeId al frontend
Equivalente a la ruta /api/config de server.py.
"""

from http.server import BaseHTTPRequestHandler
import json

PAYPHONE_TOKEN = "wvi2hPp-_QMdJlVgNKIt5NNEo1vMCJFIGbtmGgCrZbeCCPHynVY4IKOjGTzO96QGegaOmPIffkxW_STXUhHNw6H1YAgkTU6oSYUTlgTXUvhSsTUQoA7YfWHexVMZ-r_YljOYcVqox5PZUviyM48Kjmv75ER2f9SJ33X1kwxi3xXVZ8rMbK1AnoRdpXZnhdulO8-deZEGIpCGUVu4vMApmD1jKctoDI9mHEJEBYZwbQH3mOfdVOnMBbd7WDowdDefRQtLv2Ee4PIJq18xa2Kb9d-Ob2Vj7ETihI10NPMhBp48blS_1DYH_wGbetB_yVj4PkXPsjMfINqBWqXno4k90eX4Av0"
PAYPHONE_STORE_ID = "b6ee8df2-d7dd-4e64-9539-3c92cbcfa046"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"token": PAYPHONE_TOKEN, "storeId": PAYPHONE_STORE_ID}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
