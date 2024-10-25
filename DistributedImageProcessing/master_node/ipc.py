import socket
import pickle

def send_to_worker(worker_ip, data):
    """Send data to a worker node."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((worker_ip, 5001))
        s.sendall(pickle.dumps(data))

def receive_from_worker(worker_ip):
    """Receive processed data from a worker node."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((worker_ip, 5001))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = pickle.loads(conn.recv(1024*1024))  # Receiving processed image chunk
            return data

def receive_from_master(worker_host):
    """Receive image data from the master node."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((worker_host, 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = pickle.loads(conn.recv(1024*1024))  # Receiving image chunk
            return data

def send_to_master(worker_host, data):
    """Send processed image data back to the master."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((worker_host, 5000))
        s.sendall(pickle.dumps(data))
