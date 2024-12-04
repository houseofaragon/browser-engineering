import socket

class URL:
    def __init__(self, url):
        # "http://example.com/index.html"
        # host = "http"
        # hostname = "example.com"
        # path = "/index.html"
        # hello = url.split("://", 1) ['http', 'www.example.com']
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        # encode converts text into bytes
        s.send(request.encode("utf8"))

        # makefile returns a file object
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        verion, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.lower()] = value.strip()