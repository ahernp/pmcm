import cgi
import http.server
import socketserver
import urllib.parse
from os import curdir, sep

from page import edit_page, save_page, view_page
from sitemap import site_map
from uploads import file_upload, view_uploads

PORT = 8088

class Handler(http.server.SimpleHTTPRequestHandler):

    def return_html_content(self, content):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, encoding="UTF-8"))

    def redirect(self, location):
        self.send_response(301)
        self.send_header("Content-type", "text/html")
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/media") or self.path.startswith("/static"):
            super().do_GET()
        elif self.path.startswith("/pages"):
            name = urllib.parse.unquote(self.path[len("/pages/"):])
            self.return_html_content(view_page(name))
        elif self.path.startswith("/edit"):
            name = urllib.parse.unquote(self.path[len("/edit/"):])
            self.return_html_content(edit_page(name))
        elif self.path.startswith("/sitemap"):
            self.return_html_content(site_map())
        elif self.path.startswith("/uploads"):
            self.return_html_content(view_uploads())
        else:
            print("Redirect to Home page")
            self.redirect("/pages/Home")
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST",
                     "CONTENT_TYPE":self.headers["Content-Type"],
            })
        print(f"form {form.keys()}")
        try:
            if self.path.startswith("/save"):
                name = urllib.parse.unquote(self.path[len("/save/"):])
                content = form["content"].value
                save_page(name, content)
                self.redirect(f"/pages/{name}")
            elif self.path.startswith("/uploads"):
                directory = form["dir"].value
                filename = form["newFile"].filename
                uploaded_data = form["newFile"].file.read()
                file_upload(directory, filename, uploaded_data)
                self.redirect(f"/uploads")
            # elif self.path.startswith("/search"):
            #     searchterm = form["search"].value
            #     self.return_html_content(search(searchterm))
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
