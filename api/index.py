"""
NODE/// — Backend Payphone
Único punto de entrada Python que Vercel reconoce (api/index.py con
una app Flask). Reemplaza a los archivos separados config.py / confirm.py
que usaban el formato antiguo de funciones Python.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# ─── CONFIGURACIÓN ──────────────────────────────────────────────────────────
PAYPHONE_TOKEN = "wvi2hPp-_QMdJlVgNKIt5NNEo1vMCJFIGbtmGgCrZbeCCPHynVY4IKOjGTzO96QGegaOmPIffkxW_STXUhHNw6H1YAgkTU6oSYUTlgTXUvhSsTUQoA7YfWHexVMZ-r_YljOYcVqox5PZUviyM48Kjmv75ER2f9SJ33X1kwxi3xXVZ8rMbK1AnoRdpXZnhdulO8-deZEGIpCGUVu4vMApmD1jKctoDI9mHEJEBYZwbQH3mOfdVOnMBbd7WDowdDefRQtLv2Ee4PIJq18xa2Kb9d-Ob2Vj7ETihI10NPMhBp48blS_1DYH_wGbetB_yVj4PkXPsjMfINqBWqXno4k90eX4Av0"
PAYPHONE_STORE_ID = "b6ee8df2-d7dd-4e64-9539-3c92cbcfa046"
CONFIRM_URL = "https://paymentbox.payphonetodoesposible.com/api/confirm"

HEADERS = {
    "Authorization": f"Bearer {PAYPHONE_TOKEN}",
    "Content-Type": "application/json",
}


# ─── API: CONFIRMAR TRANSACCIÓN ─────────────────────────────────────────────
@app.route("/api/confirm", methods=["POST"])
def confirm_transaction():
    data = request.get_json(silent=True) or {}
    transaction_id = data.get("id")
    client_tx_id = data.get("clientTxId")

    if not transaction_id or not client_tx_id:
        return jsonify({"error": "Faltan 'id' o 'clientTxId'"}), 400

    payload = {"id": int(transaction_id), "clientTxId": client_tx_id}

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Confirmando transacción:", payload)

    try:
        resp = requests.post(CONFIRM_URL, headers=HEADERS, json=payload, timeout=15)
        result = resp.json()
        return jsonify({
            "ok": resp.status_code == 200,
            "httpStatus": resp.status_code,
            "data": result,
        }), resp.status_code
    except requests.exceptions.Timeout:
        return jsonify({"ok": False, "error": "Timeout con Payphone"}), 504
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ─── API: CREDENCIALES PARA EL FRONTEND ─────────────────────────────────────
@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({
        "token": PAYPHONE_TOKEN,
        "storeId": PAYPHONE_STORE_ID,
    })
