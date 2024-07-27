# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    address = ("localhost", 4221)
    server_socket = socket.create_server(address=address, reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    # server_socket.bind(address)
    request = conn.recv(1024)
    request_line = request.decode('utf-8').split("\r\n")[0]
    path = request_line.split(" ")[1]
    if path == "/":
        not_found = False
    else:
        not_found = True
    print(path)
    if not_found:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n", socket.MSG_WAITALL)
    else:
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n\r\n", socket.MSG_WAITALL)

if __name__ == "__main__":
    main()
