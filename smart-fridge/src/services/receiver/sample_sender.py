import socket

def main() -> None:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("<YOUR_IP>", 12444))

    for i in range(10):
        clientSocket.send("<SENSOR=movement1;TYPE=sensor;>Hello from esp32!<END>".encode())

if __name__ == "__main__":
    main()
