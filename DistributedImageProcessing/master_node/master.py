import socket
import os
from image_splitter import split_image, merge_image
import ipc

# Master node config
MASTER_HOST = '192.168.1.1'  # Example IP
PORT = 5000
NUM_WORKERS = 4  # Number of worker nodes

def distribute_and_process(image_path):
    """Distribute the image chunks to worker nodes and gather results."""
    # 1. Split image into chunks for multiprocessing
    chunks = split_image(image_path, NUM_WORKERS)
    
    # 2. Distribute chunks to worker nodes
    worker_results = []
    for i, chunk in enumerate(chunks):
        worker_ip = f"192.168.1.{i+2}"  # Worker IPs in sequence
        ipc.send_to_worker(worker_ip, chunk)
        processed_chunk = ipc.receive_from_worker(worker_ip)
        worker_results.append(processed_chunk)

    # 3. Merge results into final processed image
    final_image = merge_image(worker_results)
    return final_image

if __name__ == "__main__":
    final_image = distribute_and_process("input_image.png")
    final_image.save("output_image.png")
    print("Processing complete. Saved to output_image.png.")
