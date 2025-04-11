
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
