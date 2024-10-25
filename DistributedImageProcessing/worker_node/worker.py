import socket
import ipc
from image_processing import apply_filter

WORKER_HOST = '192.168.1.2'  # IP of this worker
PORT = 5001

def worker_process():
    """Worker node listens for image chunks, processes them, and sends back results."""
    while True:
        image_chunk = ipc.receive_from_master(WORKER_HOST)
        processed_chunk = apply_filter(image_chunk)
        ipc.send_to_master(WORKER_HOST, processed_chunk)

if __name__ == "__main__":
    worker_process()
