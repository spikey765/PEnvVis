from flask import Flask, jsonify, request
import pandas as pd
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

DATA_DIR = 'data'
CACHE = {}  # Cache for loaded datasets

def load_data(filename):
    """Load data from a CSV or JSON file with caching."""
    filepath = os.path.join(DATA_DIR, filename)
    
    if filename in CACHE:
        logging.info(f"Loading {filename} from cache")
        return CACHE[filename]

    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}")
        return None

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            logging.warning(f"Unsupported file format: {filename}")
            return None

        CACHE[filename] = df  # Store in cache
        return df

    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return None

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """List all available datasets in the data directory."""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') or f.endswith('.json')]
    return jsonify({'datasets': files}) if files else jsonify({'error': 'No datasets found'}), 404

@app.route('/api/air_pollution', methods=['GET'])
def get_air_pollution():
    """Fetch air pollution data, optionally filtered by year."""
    df = load_data('air_pollution.csv')
    if df is None:
        return jsonify({'error': 'Air pollution data not found'}), 404
    
    year = request.args.get('year')
    if year:
        df = df[df['year'] == int(year)]
    
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/farming', methods=['GET'])
def get_farming_data():
    """Fetch farming data, optionally filtered by year."""
    df = load_data('farming.csv')
    if df is None:
        return jsonify({'error': 'Farming data not found'}), 404

    year = request.args.get('year')
    if year:
        df = df[df['year'] == int(year)]
    
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/summary/<dataset>', methods=['GET'])
def get_dataset_summary(dataset):
    """Return summary statistics for a given dataset."""
    filename = f"{dataset}.csv"
    df = load_data(filename)
    if df is None:
        return jsonify({'error': f'{dataset} data not found'}), 404
    
    summary = df.describe().to_dict()
    return jsonify(summary)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
