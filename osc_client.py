from pythonosc.udp_client import SimpleUDPClient
import time

UDP_IP = "127.0.0.1"  
UDP_PORT = 8000

def send_osc(client, msg, data):
    client.send_message(msg, data)   
    time.sleep(1)

def run(client):
    while True:
        send_osc(client, "/note", [41, 40])   
        time.sleep(2)

if __name__=="__main__":
    client = SimpleUDPClient(UDP_IP, UDP_PORT)
    run(client)