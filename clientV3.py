import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        # Create a TCP/IP socket and connect to the server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            
            while True:
                # Wait to receive data from the server.
                data = client_socket.recv(4096)
                if not data:
                    print("No data received. Closing connection.")
                    break

                # Decode the received bytes into a string.
                received_message = data.decode('utf-8')
                print(f"Received message: {received_message}")

                # Reverse the received string.
                reversed_message = received_message[::-1]
                print(f"Sending reversed message: {reversed_message}")

                # Send the reversed string back to the server.
                client_socket.sendall(reversed_message.encode('utf-8'))

if __name__ == '__main__':
    # Update the host and port if needed.
    client = Client('192.168.141.175', 65432)
    client.run()
