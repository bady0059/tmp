# modules
import socket
import os

# constants
IP = "0.0.0.0"
PORT = 80

DEFAULT_PATH = r'/root/school/html/'
DEFAULT_FILE = r'main.html'
DEFAULT_URL = DEFAULT_PATH + DEFAULT_FILE

def get_file_data(filename):
    """ Get data from file in binary"""
    with open(filename, 'rb') as f:
        file_read = f.read()
        return file_read


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    if not os.path.exists(url):
        http_response = "HTTP/1.1 404 Not Found\r\n"
        http_response += "\n"
        client_socket.send(http_response.encode())
        return
    else:
        http_header = "HTTP/1.1 200 OK\r\n"
        if url == DEFAULT_URL:
            http_header += "Content-Type: text/html; charset=utf-8\r\n"
        else:
            if "." in url:
                file_type = url[url.rindex(".") + 1:]
                if file_type == 'html':
                    http_header += "Content-Type: text/html; charset=utf-8\r\n"
                elif file_type == 'jpg':
                    http_header += "Content-Type: image/jpeg\r\n"
                elif file_type == 'js':
                    http_header += "Content-Type: application/x-javascript; charset=UTF-8\r\n"
                elif file_type == 'css':
                    http_header += "Content-Type: text/css\r\n"
                elif file_type == 'mp3':
                    http_header += "Content-Type: audio/mpeg\r\n"

        data = get_file_data(url)
        http_header += "\n"
        http_response = http_header.encode() + data
        client_socket.sendall(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """

    regex = request.split()
    requset_type = regex[0]
    if requset_type != 'GET':
        return False, None
    url_path = regex[1]

    if url_path == r'/':
        requested_url = ''
    else:
        requested_url = DEFAULT_PATH
        src_of = url_path.replace(r"/", "")
        requested_url += src_of
    print(requested_url)
    return True, requested_url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print("client data: ", client_socket)
    while True:
        client_request = client_socket.recv(2048).decode()
        if client_request == "":
            break

        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            handle_client_request(resource, client_socket)
            break
        else:
            print("bad HTTP request")
            print("Closing connection")
            break
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print("New connection received")
        client_socket.settimeout(1000)
        handle_client(client_socket)



