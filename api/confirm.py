"""
NODE/// — Función serverless: confirmar transacción con Payphone
Equivalente a la ruta /api/confirm de server.py, adaptada al formato
de funciones Python de Vercel (BaseHTTPRequestHandler).
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import requests

PAYPHONE_TOKEN = "wvi2hPp-_QMdJlVgNKIt5NNEo1vMCJFIGbtmGgCrZbeCCPHynVY4IKOjGTzO96QGegaOmPIffkxW_STXUhHNw6H1YAgkTU6oSYUTlgTXUvhSsTUQoA7YfWHexVMZ-r_YljOYcVqox5PZUviyM48Kjmv75ER2f9SJ33X1kwxi3xXVZ8rMbK1AnoRdpXZnhdulO8-deZEGIpCGUVu4vMApmD1jKctoDI9mHEJEBYZwbQH3mOfdVOnMBbd7WDowdDefRQtLv2Ee4PIJq18xa2Kb9d-Ob2Vj7ETihI10NPMhBp48blS_1DYH_wGbetB_yVj4PkXPsjMfINqBWqXno4k90eX4Av0"
CONFIRM_URL = "https://paymentbox.payphonetodoesposible.com/api/confirm"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length else b""

        try:
            data = json.loads(raw_body or b"{}")
        except json.JSONDecodeError:
            self._send_json({"error": "JSON inválido"}, 400)
            return

        transaction_id = data.get("id")
        client_tx_id = data.get("clientTxId")

        if not transaction_id or not client_tx_id:
            self._send_json({"error": "Faltan 'id' o 'clientTxId'"}, 400)
            return

        payload = {"id": int(transaction_id), "clientTxId": client_tx_id}
        headers = {
            "Authorization": f"Bearer {PAYPHONE_TOKEN}",
            "Content-Type": "application/json",
        }

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Confirmando transacción:")
        print(json.dumps(payload, indent=2))

        try:
            resp = requests.post(CONFIRM_URL, headers=headers, json=payload, timeout=15)
            result = resp.json()
            print(f"[Payphone Confirm] Status HTTP: {resp.status_code}")
            print(json.dumps(result, indent=2))

            self._send_json(
                {
                    "ok": resp.status_code == 200,
                    "httpStatus": resp.status_code,
                    "data": result,
                },
                resp.status_code,
            )
        except requests.exceptions.Timeout:
            self._send_json({"ok": False, "error": "Timeout con Payphone"}, 504)
        except Exception as e:
            print(f"[ERROR] {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
