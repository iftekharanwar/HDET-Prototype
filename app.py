from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import xml.etree.ElementTree as ET
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('hdet.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hardware_data (
            id INTEGER PRIMARY KEY,
            ip_address TEXT,
            dhcp_options TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route to import data
@app.route('/import', methods=['POST'])
def import_data():
    file = request.files['file']
    if file:
        filename = file.filename
        if filename.endswith('.xlsx'):
            df = pd.read_excel(file)
            conn = sqlite3.connect('hdet.db')
            cursor = conn.cursor()
            for index, row in df.iterrows():
                cursor.execute('INSERT INTO hardware_data (ip_address, dhcp_options) VALUES (?, ?)', (row['ip_address'], row['dhcp_options']))
            conn.commit()
            conn.close()
        elif filename.endswith('.xml'):
            tree = ET.parse(file)
            root = tree.getroot()
            conn = sqlite3.connect('hdet.db')
            cursor = conn.cursor()
            for hardware in root.findall('hardware'):
                ip_address = hardware.find('ip_address').text
                dhcp_options = hardware.find('dhcp_options').text
                cursor.execute('INSERT INTO hardware_data (ip_address, dhcp_options) VALUES (?, ?)', (ip_address, dhcp_options))
            conn.commit()
            conn.close()
        else:
            return jsonify({"error": "Unsupported file format"}), 400
        return jsonify({"message": "Data imported successfully"})
    return jsonify({"error": "No file provided"}), 400

# Route to export data
@app.route('/export', methods=['GET'])
def export_data():
    conn = sqlite3.connect('hdet.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hardware_data')
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'ip_address': row[1],
            'dhcp_options': row[2]
        })

    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
