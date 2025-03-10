import socket
import threading
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS-Import hinzufügen

# -------------------------------
# Configure Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# TCP Client Manager
# -------------------------------
class TCPClientManager:
    """
    Manages the TCP server that waits for a single client connection.
    Provides a method to send a message to the client and wait for a response.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Create and configure the TCP server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.connection = None  # Holds the accepted client socket
        self.conn_lock = threading.Lock()  # For thread-safe access
        self.logger = logging.getLogger("TCPClientManager")
        self.logger.info(f"TCP Server listening on {self.host}:{self.port}")

    def start(self):
        """Start the background thread to accept TCP client connections."""
        accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        accept_thread.start()

    def accept_connections(self):
        """
        Waits for a client connection. If a client is already connected, new connections are rejected.
        """
        while True:
            try:
                conn, addr = self.sock.accept()
                self.logger.info(f"Incoming connection from {addr}")
                with self.conn_lock:
                    if self.connection is not None:
                        self.logger.warning("A client is already connected. Rejecting additional connection.")
                        conn.close()  # TEMP: Only one client is allowed.
                    else:
                        self.connection = conn
                        self.logger.info(f"TCP client connected from {addr}")
            except Exception as e:
                self.logger.error(f"Error accepting connections: {e}")

    def send_message(self, message, timeout=10):
        """
        Sends a message (string) to the connected TCP client and waits for a response.
        Raises an Exception if no client is connected or if an error occurs.
        """
        with self.conn_lock:
            if self.connection is None:
                raise Exception("No TCP client connected.")
            try:
                self.logger.info(f"Sending message to TCP client: {message}")
                # Send the message encoded as bytes.
                self.connection.sendall(message.encode())
                # Set a timeout for receiving a response.
                self.connection.settimeout(timeout)
                response = self.connection.recv(4096).decode()
                self.connection.settimeout(None)
                self.logger.info(f"Received response from TCP client: {response}")
                return response
            except socket.timeout:
                self.logger.error("TCP client response timed out")
                raise Exception("TCP client response timed out")
            except Exception as e:
                self.logger.error(f"Error during send/receive: {e}")
                try:
                    self.connection.close()
                except Exception:
                    pass
                self.connection = None
                raise e

# -------------------------------
# Configuration for TCP and REST API
# -------------------------------
TCP_HOST = '192.168.141.175'  # Passe ggf. an
TCP_PORT = 65432            # TCP server port
REST_API_PORT = 5000        # Port für die Flask API

# Create and start the TCP client manager
tcp_manager = TCPClientManager(TCP_HOST, TCP_PORT)
tcp_manager.start()

# -------------------------------
# Flask REST API Setup
# -------------------------------
app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Ursprünge

@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        # Check if a TCP client is connected
        if tcp_manager.connection is None:
            return jsonify({"error": "No TCP client connected."}), 503

        # Parse and validate the JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload."}), 400

        required_keys = ["user_id", "session_id", "message"]
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing keys in payload: {missing_keys}"}), 400

        user_id = data["user_id"]
        session_id = data["session_id"]
        message = data["message"]

        # Debug log before sending to TCP
        app.logger.info(f"Sending message to TCP client: {message}")

        # Send the message over the TCP connection and get the response
        tcp_response = tcp_manager.send_message(message)

        # Debug log after receiving from TCP
        app.logger.info(f"Received response from TCP client: {tcp_response}")

        # Build the response payload
        response_payload = {
            "user_id": user_id,
            "session_id": session_id,
            "response": tcp_response,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return jsonify(response_payload), 200

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Run the Flask App
# -------------------------------
if __name__ == '__main__':
    # Für den Produktionseinsatz sollte ein WSGI-Server verwendet werden.
    app.run(host='0.0.0.0', port=REST_API_PORT)
