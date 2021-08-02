import argparse
import cgi
import http.server
import socketserver
import urllib.parse

from constants import PAGES_URL_ROOT
from page import edit_page, save_page, view_page
from search import search
from sitemap import site_map
from uploads import file_upload, view_uploads

PORT_DEFAULT = 7713

EDIT_URL_ROOT = "/edit"
HOME_PAGE_URL = f"{PAGES_URL_ROOT}/Home"
MEDIA_URL_ROOT = "/media"
SAVE_URL_ROOT = "/save"
SEARCH_URL_ROOT = "/search"
SITEMAP_URL_ROOT = "/sitemap"
STATIC_URL_ROOT = "/static"
UPLOAD_URL_ROOT = "/uploads"


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
        if self.path.startswith(MEDIA_URL_ROOT) or self.path.startswith(
            STATIC_URL_ROOT
        ):
            super().do_GET()
        elif self.path.startswith(PAGES_URL_ROOT):
            name = urllib.parse.unquote(self.path[len(PAGES_URL_ROOT) + 1 :])
            self.return_html_content(view_page(name))
        elif self.path.startswith(EDIT_URL_ROOT):
            name = urllib.parse.unquote(self.path[len(EDIT_URL_ROOT) + 1 :])
            self.return_html_content(edit_page(name))
        elif self.path.startswith(SITEMAP_URL_ROOT):
            self.return_html_content(site_map())
        elif self.path.startswith(UPLOAD_URL_ROOT):
            self.return_html_content(view_uploads())
        else:
            self.redirect(HOME_PAGE_URL)
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )

        try:
            if self.path.startswith(SAVE_URL_ROOT):
                name = urllib.parse.unquote(self.path[len(SAVE_URL_ROOT) + 1 :])
                content = form["content"].value
                save_page(name, content)
                self.redirect(f"{PAGES_URL_ROOT}/{name}")
            elif self.path.startswith(UPLOAD_URL_ROOT):
                directory = form["dir"].value
                filename = form["newFile"].filename
                uploaded_data = form["newFile"].file.read()
                file_upload(directory, filename, uploaded_data)
                self.redirect(UPLOAD_URL_ROOT)
            elif self.path.startswith(SEARCH_URL_ROOT):
                search_term = form["search"].value
                self.return_html_content(search(search_term))
        except IOError:
            self.send_error(404, "Not Found: %s" % self.path)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main(port):
    with ThreadedTCPServer(("", port), Handler, bind_and_activate=False) as httpd:
        print("serving at port", port)
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", help="port to listen on", type=int, default=PORT_DEFAULT
    )
    args = parser.parse_args()
    main(args.port)
