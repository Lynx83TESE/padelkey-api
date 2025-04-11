
import os
from flask import Flask, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
API_TOKEN = os.getenv("SHOPIFY_API_KEY")

headers = {
    "X-Shopify-Access-Token": API_TOKEN,
    "Content-Type": "application/json"
}

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify({"message": "API attiva e funzionante!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
@app.route('/get_orders', methods=['GET'])
def get_orders():
    # URL per ottenere gli ordini
    orders_url = f"https://{SHOP_URL}/admin/api/2023-01/orders.json"
    
    # Fai la richiesta a Shopify
    response = requests.get(orders_url, headers=headers)
    
    # Se la richiesta va a buon fine
    if response.status_code == 200:
        orders = response.json()  # Ottieni gli ordini in formato JSON
        return jsonify(orders)  # Ritorna gli ordini al cliente
    else:
        return jsonify({"error": "Impossibile recuperare gli ordini"}), 500
