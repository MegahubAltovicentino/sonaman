import os

message = "/test hi"
server_address = ("127.0.0.1", 8000)

os.system("echo '" + message + "' | timeout 0.01 nc -u 127.0.0.1 8000")

print(f"Sent: {message} to {server_address}")