import os
from flask import Flask, jsonify, request, send_from_directory
import subprocess
import threading
import csv
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='static')


cors = CORS(app, origins="*")


# Function to run the script in a separate thread
def run_script():
    try:
        print("Running server_script.py...")  # Debug message
        subprocess.run(['python', 'server_script.py'], check=True)
        print("Data updated successfully.")  # Debug message
    except Exception as e:
        print(f"Error updating data: {e}")


@app.route('/update_data', methods=['POST'])
def update_data():
    print("Update data request received.")  # Debug message
    # Run the script in a separate thread to avoid blocking
    thread = threading.Thread(target=run_script)
    thread.start()
    return jsonify({"status": "Data update initiated."}), 200


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route('/get_processor_data', methods=['POST'])
def get_processor_data():
    jsonArray = []
    with open(app.static_folder + "\\processor_data.csv", encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            jsonArray.append(row)


    return jsonArray, 200


if __name__ == '__main__':
    # Use the port provided by Railway, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
