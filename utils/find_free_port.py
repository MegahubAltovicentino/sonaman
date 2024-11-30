import socket

def find_free_port(start_port=1024, end_port=65535, host='127.0.0.1'):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return port  # Port is available
            except OSError:
                continue  # Port is already in use, try the next one
    return None 


if __name__=="__main__":
    available_port = find_free_port()
    if available_port:
        print(f"Found an available port: {available_port}")
    else:
        print("No available ports found.")  