import cv2
import socket
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("0.0.0.0", 5000))

try: 
    while True:
        data, addr = client_socket.recvfrom(65536)
        np_data = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        cv2.imshow('Video Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print(" Exiting...")