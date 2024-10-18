import os
from flask import Flask, jsonify, request, send_from_directory
import subprocess
import threading

app = Flask(__name__, static_url_path='', static_folder='static')

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
    return send_from_directory(app.static_folder, "final.html")

if __name__ == '__main__':
    # Use the port provided by Railway, or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
