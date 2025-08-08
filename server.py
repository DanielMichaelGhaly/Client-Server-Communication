import socket
import threading
import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client_data = {
    'client1': {'cpu': 0, 'gpu': 0, 'memory': 0},
    'client2': {'cpu': 0, 'gpu': 0, 'memory': 0}
}

thresholds = {
    'client1': {'cpu': 50, 'gpu': 50, 'memory': 50},
    'client2': {'cpu': 50, 'gpu': 50, 'memory': 50}
}

@app.route('/update_thresholds', methods=['POST'])
def update_thresholds():
    data = request.get_json()
    thresholds['client1'] = data.get('client1', thresholds['client1'])
    thresholds['client2'] = data.get('client2', thresholds['client2'])
    return jsonify({'success': True})

@app.route('/get_updated_data')
def get_updated_data():
    return jsonify({
        'client1_data': client_data['client1'],
        'client2_data': client_data['client2'],
        'thresholds': thresholds
    })

def handle_client(conn, addr, client_id):
    print(f"[{client_id}] Connected: {addr}")
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break

            array = pickle.loads(data)
            if array == ['EXIT']:
                print(f"[{client_id}] Disconnected.")
                break

            client_data[client_id] = {
                'cpu': array[0],
                'gpu': array[1],
                'memory': array[2]
            }

            print(f"[{client_id}] Updated data: {client_data[client_id]}")

            conn.send("Data received".encode('utf-8'))

        except Exception as e:
            print(f"[{client_id}] Error: {e}")
            break
    conn.close()

def socket_server():
    HOST = '0.0.0.0'
    PORT = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"[Socket Server] Listening on {HOST}:{PORT}")

    clients_connected = 0
    while clients_connected < 2:
        conn, addr = server_socket.accept()
        client_id = f'client{clients_connected + 1}'
        threading.Thread(target=handle_client, args=(conn, addr, client_id)).start()
        clients_connected += 1

if __name__ == "__main__":
    # Run socket server in a separate thread
    threading.Thread(target=socket_server, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000)
