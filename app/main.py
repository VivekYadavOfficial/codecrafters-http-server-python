# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    address = ("localhost", 4221)
    server_socket = socket.create_server(address=address, reuse_port=True)
    # start a infinite loop to keep receiving requests/connections
    while True:
        conn, addr = server_socket.accept()
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n", socket.MSG_WAITALL)
    conn, addr = server_socket.accept() # wait for client
    request = conn.recv(1024)
    conn.sendall(b"HTTP/1.1")
    request_line = request.decode('utf-8').split("\r\n")[0]
    path = request_line.split(" ")[1]
    print(path)
    # check if path is user-agent
    if path == "/user-agent":
        # extract header from request
        headers = request.decode('utf-8').split("\r\n\r\n")[0].split("\r\n")[1:]
        # loop through and find which header is user-agent
        for header in headers:
            if header.split(":")[0].lower() == 'user-agent':
                user_agent = header.split(":")[1]
                user_agent = user_agent.strip()
                content_length = len(user_agent)
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + user_agent.encode() + b"\r\n", socket.MSG_WAITALL)

    if path == "/":
        r_str = "/"
        content_length = len(r_str)
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
    elif path.split("/")[1] != "echo":
        r_str = ""
        content_length = len(r_str)
        conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
    else:
        r_str = path.split("/")[2]
        print(r_str)
        content_length = len(r_str)
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)

if __name__ == "__main__":
    main()
