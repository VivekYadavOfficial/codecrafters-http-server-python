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
    print(path)
    if path.split("/")[1] != "echo":
        r_str = ""
    else:
        r_str = path.split("/")[2]
        print(r_str)
    content_length = len(r_str)
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)

if __name__ == "__main__":
    main()
