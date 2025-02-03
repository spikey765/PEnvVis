# Basic MVP for Environmental Data Visualization
# Flask Backend (backend.py)

from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    # Load air pollution data (Replace 'air_pollution.csv' with actual dataset)
    df = pd.read_csv('air_pollution.csv')
    return df

@app.route('/api/air_pollution', methods=['GET'])
def get_air_pollution():
    df = load_data()
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


