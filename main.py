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

@app.route('/get_orders', methods=['GET'])
def get_orders():
    # URL per ottenere gli ordini
    orders_url = f"https://{SHOP_URL}/admin/api/2023-01/orders.json"
    
    # Fai la richiesta GET per ottenere gli ordini
    response = requests.get(orders_url, headers=headers)
    
    # Log per verificare la risposta completa
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    # Controlla lo status code della risposta
    if response.status_code == 200:
        # Se la risposta è OK, restituisce gli ordini
        orders = response.json()  # Converte la risposta in formato JSON
        return jsonify(orders)  # Restituisce gli ordini in formato JSON
    else:
        # Se c'è un errore, ritorna un errore con codice 500
        return jsonify({
            "error": "Impossibile recuperare gli ordini", 
            "status_code": response.status_code,
            "response": response.text
        }), 500

@app.route('/get_order/<order_id>', methods=['GET'])
def get_order(order_id):
    # URL per ottenere un ordine specifico tramite l'ID
    order_url = f"https://{SHOP_URL}/admin/api/2023-01/orders/{order_id}.json"
    
    # Fai la richiesta GET per ottenere i dettagli di un singolo ordine
    response = requests.get(order_url, headers=headers)
    
    # Log per verificare la risposta completa
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    # Se la risposta è OK (200), restituisce l'ordine
    if response.status_code == 200:
        order = response.json()  # Converte la risposta in formato JSON
        return jsonify(order)  # Restituisce i dettagli dell'ordine
    else:
        # Se c'è un errore, ritorna un errore con codice 500
        return jsonify({
            "error": f"Impossibile recuperare l'ordine {order_id}",
            "status_code": response.status_code,
            "response": response.text
        }), 500

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
    
    # Log per verificare la risposta completa
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    # Se l'ordine è creato con successo (status 201), restituisce un messaggio di successo
    if response.status_code == 201:
        return jsonify({"message": "Ordine creato con successo"}), 201
    else:
        # Se c'è un errore nella creazione dell'ordine, ritorna un errore con codice 500
        return jsonify({
            "error": "Impossibile creare l'ordine",
            "status_code": response.status_code,
            "response": response.text
        }), 500

# Funzione principale per eseguire Flask su Replit o altri ambienti
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
