# Basic MVP for Environmental Data Visualization
# Flask Backend (backend.py)

from flask import Flask, jsonify
import pandas as pd
import os
import logging

app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

DATA_DIR = 'data'

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}")
        return None
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filename.endswith('.json'):
            return pd.read_json(filepath)
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return None
    
    logging.warning(f"Unsupported file format: {filename}")
    return None

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List all available datasets in the data directory."""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') or f.endswith('.json')]
    if files:
        return jsonify({'datasets': files})
    return jsonify({'error': 'No datasets found'}), 404    

@app.route('/api/air_pollution', methods=['GET'])
def get_air_pollution():
    df = load_data('air_pollution.csv')
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({'error': 'Air pollution data not found'}), 404

@app.route('/api/farming', methods=['GET'])
def get_farming_data():
    df = load_data('farming.csv')
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({'error': 'Farming data not found'}), 404

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)  # Create data directory if it doesn't exist
    app.run(debug=True)
