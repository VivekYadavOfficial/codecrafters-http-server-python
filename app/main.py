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
    conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n\r\n", socket.MSG_WAITALL)

if __name__ == "__main__":
    main()
