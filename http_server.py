from socket import *
from urlparse import urlparse
import sys, os, select

if len(sys.argv) == 2:
    param = sys.argv[1]
    serverPort = int(param)
else:
    serverPort = 2000

files = os.listdir(".")
web_file_extensions = [".htm", ".html"]
http_status_code_to_phrase = {200: "OK", 403: "Forbidden", 404: "Not Found"}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

open_connections = []
while True:
    read_list = list(open_connections)
    read_list.append(serverSocket)
    readable, writable, exceptional = select.select(read_list, read_list, read_list)
    for s in readable:
        if s == serverSocket:
            connectionSocket, addr = s.accept()
            open_connections.append(connectionSocket)
        else:
            Buff = 4096
            request = ""
            while True:
                data = s.recv(Buff)
                request += data
                if len(data) < Buff:
                    break
            requested_file_start = request.find('/') + 1        
            requested_file_end = request.find(' ', requested_file_start)
            requested_file = request[requested_file_start : requested_file_end]
            requested_file_extension_start = requested_file.rfind('.')
            requested_file_extension = requested_file[requested_file_extension_start:]
            if requested_file in files:
                if requested_file_extension in web_file_extensions:
                    status_code = 200
                    filepath = "./" + requested_file
                    with open(filepath, 'r') as myfile:
                        response_body = myfile.read()
                else:
                    status_code = 403
                    response_body = "<html>403 Forbidden</html>"
            else:
                status_code = 404
                response_body = "<html>404 Not Found</html>"
            status_phrase = http_status_code_to_phrase[status_code]
            status_line = "HTTP/1.0 " + str(status_code) + ' ' + status_phrase
            content_type_line = "Content-Type: text/html"
            response = status_line + '\r\n' + content_type_line + '\r\n\r\n'
            response += response_body
            s.sendall(response)
            s.close()
            open_connections.remove(s)
