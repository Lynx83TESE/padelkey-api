import os
from flask import Flask, jsonify
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)

# Ottieni i dati dal file .env
SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
API_TOKEN = os.getenv("SHOPIFY_API_KEY")

headers = {
    "X-Shopify-Access-Token": API_TOKEN,
    "Content-Type": "application/json"
}

# Rotta che restituisce tutti gli ordini
@app.route('/get_orders', methods=['GET'])
def get_orders():
    # URL per ottenere gli ordini
    orders_url = f"https://{SHOP_URL}/admin/api/2023-01/orders.json"
    
    # Fai la richiesta GET per ottenere gli ordini da Shopify
    response = requests.get(orders_url, headers=headers)
    
    # Se la risposta è valida (status code 200), restituisce gli ordini
    if response.status_code == 200:
        orders = response.json()  # Converte la risposta in formato JSON
        return jsonify(orders)  # Restituisce gli ordini al cliente
    else:
        return jsonify({"error": "Impossibile recuperare gli ordini"}), 500

# Rotta che restituisce i dettagli di un singolo ordine (passando l'ID dell'ordine)
@app.route('/get_order/<order_id>', methods=['GET'])
def get_order(order_id):
    order_url = f"https://{SHOP_URL}/admin/api/2023-01/orders/{order_id}.json"
    
    # Fai la richiesta GET per ottenere un singolo ordine
    response = requests.get(order_url, headers=headers)
    
    if response.status_code == 200:
        order = response.json()  # Converte la risposta in formato JSON
        return jsonify(order)  # Restituisce i dettagli dell'ordine
    else:
        return jsonify({"error": f"Impossibile recuperare l'ordine {order_id}"}), 500

# Rotta che permette di creare un nuovo ordine (si utilizza POST)
@app.route('/create_order', methods=['POST'])
def create_order():
    order_data = {
        "order": {
            "line_items": [
                {
                    "variant_id": 123456789,  # ID variante prodotto (modifica con l'ID reale)
                    "quantity": 1
                }
            ],
            "customer": {
                "id": 123456789,  # ID cliente (modifica con l'ID reale)
            },
            "shipping_address": {
                "first_name": "John",
                "last_name": "Doe",
                "address1": "123 Street",
                "city": "City",
                "province": "State",
                "country": "Country",
                "zip": "12345"
            }
        }
    }
    
    # Fai la richiesta POST per creare un nuovo ordine
    response = requests.post(f"https://{SHOP_URL}/admin/api/2023-01/orders.json", json=order_data, headers=headers)
    
    if response.status_code == 201:
        return jsonify({"message": "Ordine creato con successo"}), 201
    else:
        return jsonify({"error": "Impossibile creare l'ordine"}), 500

# Funzione principale per eseguire Flask su Replit o altri ambienti
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
