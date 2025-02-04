# Basic MVP for Environmental Data Visualization
# Flask Backend (backend.py)

from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

def load_data(filename):
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

@app.route('/api/air_pollution', methods=['GET'])
def get_air_pollution():
    df = load_data('air_pollution.csv')
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({'error': 'Data not found'}), 404

@app.route('/api/farming', methods=['GET'])
def get_farming_data():
    df = load_data('farming.csv')
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)