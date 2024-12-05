import socket
import ssl

class URL:
    def __init__(self, url):
        # "http://example.com:8080/index.html"
        # host = "http"
        # hostname = "example.com"
        # port = 8080
        # path = "/index.html"
        # print(url.split("://", 1)) ['http', 'www.example.com']
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https", "file"]

        if self.scheme in ["http", "https"]:
            if self.scheme == "https":
                self.port = 443
            elif self.scheme == "http":
                self.port = 80
                        
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url

            if ":" in self.host and self.host != "file":
                self.host, port = self.host.split(":", 1)
                self.port = int(port)

        elif self.scheme == "file":
            self.path = url
            self.host = None
            self.port = None

    def request(self):
        if self.scheme == "file":
            with open(self.path, "r") as f:
                return f.read()
        
        # socket connection
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

        # send request
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "Connection: close\r\n"
        request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\r\n"
        request += "\r\n"
        # encode converts text into bytes
        s.send(request.encode("utf8"))

        # response
        # makefile returns a file object
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        verion, status, explanation = statusline.split(" ", 2)

        # response headers
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.lower()] = value.strip()

        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding
        assert "transfer-encoding" not in response_headers
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content
    
def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request()
    show(body)

# run only when executing script from command line
# To open browser: python3 browser.py https://karenaragon.com
# To open file: python3 browser.py file:///path/to/example_file.htm
if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))