# Uncomment this to pass the first stage
import socket
import threading
import gzip

# function to extract method from request
def get_method_from_request(request):
    method = request.decode('utf-8').split("\r\n")[0].split(" ")[0]
    return method

# function to extract headers from request
def get_headers_from_request(request):
    headers = request.decode('utf-8').split("\r\n\r\n")[0].split("\r\n")[1:]
    header_dict = {}
    for header in headers:
        header_data = header.split(": ")
        header_dict[header_data[0]] = header_data[1]
    return header_dict

# function to extract path from request
def get_path_from_request(request):
    path = request.decode("utf-8").split("\r\n")[0].split(" ")[1]
    return path


# extract request body from request
def get_request_body_from_request(request):
    request_body = request.decode("utf-8").split("\r\n\r\n")[1]
    return request_body

# read from file with given path and return true or false
def read_from_file(file_dir):
    try:
        with open('/tmp/data/codecrafters.io/http-server-tester/' + file_dir, 'rb') as f:
            file_data = f.read()
            response_body = file_data
            content_length = len(response_body)
            return response_body, content_length, True
    except FileNotFoundError as e:
        response_body = ""
        content_length = len(response_body)
        return response_body, content_length, False


# create file at give path with request body
def create_file_from_request_body(filename, request_body):
    try:
        with open('/tmp/data/codecrafters.io/http-server-tester/' + filename, 'w') as f:
            f.write(request_body)
            f.close()
            return True
    except Exception as e:
        return False

# using thread to handle multiple connections concurrently
def process_conn_on_thread(conn):
    request = conn.recv(1024)
    method = get_method_from_request(request)
    headers = get_headers_from_request(request)
    is_gzip_enabled = headers.get('Accept-Encoding', '').lower().find("gzip") != -1
    path = get_path_from_request(request)
    file_path = path.split("http://localhost:4221")
    if len(file_path) > 1:
        file_dir = file_path[1]
    else:
        file_dir = file_path[0]
    if file_dir.startswith("/files"):
        file_dir = file_dir.replace("/files", "")
        if method.lower() == 'get':
            response_body, content_length, status = read_from_file(file_dir)
            if status:
                if is_gzip_enabled:
                    compressed_response_body = gzip.compress(response_body)
                    compressed_response_length = len(compressed_response_body)
                    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: application/octet-stream\r\nContent-Length: " + str(compressed_response_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
                else:
                    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + response_body + b"\r\n", socket.MSG_WAITALL)
            else:
                if is_gzip_enabled:
                    compressed_response_body = gzip.compress(response_body.encode())
                    compressed_response_length = len(compressed_response_body)
                    conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(compressed_response_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
                else:
                    conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + response_body.encode() + b"\r\n", socket.MSG_WAITALL)
        if method.lower() == 'post':
            request_body = get_request_body_from_request(request)
            status = create_file_from_request_body(file_dir, request_body)
            if status:
                if is_gzip_enabled:
                    conn.sendall(b"HTTP/1.1 201 Created\r\nContent-Encoding: gzip\r\n\r\n", socket.MSG_WAITALL)
                else:
                    conn.sendall(b"HTTP/1.1 201 Created\r\n\r\n", socket.MSG_WAITALL)
            else:
                if is_gzip_enabled:
                    conn.sendall(b"HTTP/1.1 500 Internal Server Error\r\nContent-Encoding: gzip\r\n\r\n", socket.MSG_WAITALL)
                else:
                    conn.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n", socket.MSG_WAITALL)
    if path == "/user-agent":
            # loop through and find which header is user-agent
            for header, value in headers.items():
                if header.lower() == 'user-agent':
                    content_length = len(value)
                    if is_gzip_enabled:
                        compressed_response_body = gzip.compress(value.encode())
                        compressed_content_length = len(compressed_response_body)
                        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(compressed_content_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
                    else:
                        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + value.encode() + b"\r\n", socket.MSG_WAITALL)
                    break
    if path == "/":
        r_str = "/"
        content_length = len(r_str)
        if is_gzip_enabled:
            compressed_response_body = gzip.compress(r_str.encode())
            compressed_content_length = len(compressed_response_body)
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(compressed_content_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
        else:
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
    elif path.split("/")[1] != "echo":
        r_str = ""
        content_length = len(r_str)
        if is_gzip_enabled:
            compressed_response_body = gzip.compress(r_str.encode())
            compressed_content_length = len(compressed_response_body)
            conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(compressed_content_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
    else:
        r_str = path.split("/")[2]
        print(r_str)
        content_length = len(r_str)
        if is_gzip_enabled:
            compressed_response_body = gzip.compress(r_str.encode())
            compressed_content_length = len(compressed_response_body)
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(compressed_content_length).encode() + b"\r\n\r\n" + compressed_response_body + b"\r\n", socket.MSG_WAITALL)
        else:
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
    # response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 27\r\n\r\n"
    # conn.sendall(response.encode(), socket.MSG_WAITALL)
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    address = ("localhost", 4221)
    server_socket = socket.create_server(address=address, reuse_port=True)
    # start a infinite loop to keep receiving requests/connections
    
    while True:
        conn, addr = server_socket.accept() # wait for client
        # request = conn.recv(1024) # receive data
        client = threading.Thread(target=process_conn_on_thread, args=(conn,))
        client.start()
        # conn.sendall(response.encode(), socket.MSG_WAITALL)
        # conn.close()
        # print(path)
        # # check if path is user-agent
        # if path == "/user-agent":
        #     # extract header from request
        #     headers = request.decode('utf-8').split("\r\n\r\n")[0].split("\r\n")[1:]
        #     # loop through and find which header is user-agent
        #     for header in headers:
        #         if header.split(":")[0].lower() == 'user-agent':
        #             user_agent = header.split(":")[1]
        #             user_agent = user_agent.strip()
        #             content_length = len(user_agent)
        #             conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + user_agent.encode() + b"\r\n", socket.MSG_WAITALL)

        # if path == "/":
        #     r_str = "/"
        #     content_length = len(r_str)
        #     conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
        # elif path.split("/")[1] != "echo":
        #     r_str = ""
        #     content_length = len(r_str)
        #     conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)
        # else:
        #     r_str = path.split("/")[2]
        #     print(r_str)
        #     content_length = len(r_str)
        #     conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(content_length).encode() + b"\r\n\r\n" + r_str.encode() + b"\r\n", socket.MSG_WAITALL)

if __name__ == "__main__":
    main()