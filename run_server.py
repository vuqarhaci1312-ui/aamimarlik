import http.server
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8081
ROOT = Path(__file__).parent

# Clean URL -> HTML file
ROUTES = {
    "/": "index.html",
    "/ana-sehife": "index.html",
    "/haqqimizda": "about.html",
    "/xidmetlerimiz": "service-11.html",
    "/interyer-eksteryer": "service-details-interyer.html",
    "/memarliq-layiheleri": "service-details-memarliq.html",
    "/sergi-stendleri": "service-details-sergi.html",
    "/layihe-idareetmesi": "service-details-idareetme.html",
    "/faq": "faq.html",
    "/elaqe": "contact.html",
    "/premium-showroom": "portfolio-details-showroom.html",
    "/ferdi-yasayis-evi": "portfolio-details-ferdiyasayis.html",
    "/muasir-ofis": "portfolio-details-ofis.html",
    "/sergi-stendi-layihe": "portfolio-details-sergistendleri.html",
}

# Old .html URLs -> clean URLs (301 redirect)
REDIRECTS = {
    "/index.html": "/",
    "/about.html": "/haqqimizda",
    "/service-11.html": "/xidmetlerimiz",
    "/service-details-interyer.html": "/interyer-eksteryer",
    "/service-details-memarliq.html": "/memarliq-layiheleri",
    "/service-details-sergi.html": "/sergi-stendleri",
    "/service-details-idareetme.html": "/layihe-idareetmesi",
    "/service-details.html": "/interyer-eksteryer",
    "/faq.html": "/faq",
    "/contact.html": "/elaqe",
    "/portfolio-details-showroom.html": "/premium-showroom",
    "/portfolio-details-ferdiyasayis.html": "/ferdi-yasayis-evi",
    "/portfolio-details-ofis.html": "/muasir-ofis",
    "/portfolio-details-sergistendleri.html": "/sergi-stendi-layihe",
}


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        if path in REDIRECTS:
            target = REDIRECTS[path]
            if parsed.query:
                target = f"{target}?{parsed.query}"
            self.send_response(301)
            self.send_header("Location", target)
            self.end_headers()
            return

        if path in ROUTES:
            self.path = "/" + ROUTES[path]
            if parsed.query:
                self.path += "?" + parsed.query

        return super().do_GET()


Handler = CleanURLHandler
Handler.extensions_map.update({
    ".css": "text/css",
    ".js": "application/javascript",
    ".svg": "image/svg+xml",
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
