import http.server
import socketserver
import urllib.parse
from os import curdir, sep

from page import edit_page, save_page, view_page

PORT = 8088

class Handler(http.server.SimpleHTTPRequestHandler):

    def return_html_content(self, content):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, encoding="UTF-8"))

    def do_GET(self):
        try:
            if self.path.startswith("/media") or self.path.startswith("/static"):
                super().do_GET()
            elif self.path.startswith("/pages"):
                html = view_page(self.path[len("/pages/"):])
                self.return_html_content(html)
            elif self.path.startswith("/edit"):
                html = edit_page(self.path[len("/edit/"):])
                self.return_html_content(html)
            elif self.path.startswith("/sitemap"):
                self.return_html_content("Sitemap")
            elif self.path.startswith("/uploads"):
                self.return_html_content("Uploads")
            return
        except IOError:
            self.send_error(404,"Not Found: %s" % self.path)

    def do_POST(self):
        try:
            if self.path.startswith("/save"):
                name = self.path[len("/save/"):]
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                content_urlencoded = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
                content = urllib.parse.unquote_plus(content_urlencoded)[len("content="):]
                save_page(name, content)
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", f"/pages/{name}")
                self.end_headers()
        except IOError:
            self.send_error(404,"Not Found: %s" % self.path)


def main():
    with socketserver.TCPServer(("", PORT), Handler, bind_and_activate=False) as httpd:
        print("serving at port", PORT)
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        httpd.serve_forever()

if __name__ == "__main__":
    main()
