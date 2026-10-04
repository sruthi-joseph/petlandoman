import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8080

REW_RITES = {}
if os.path.exists("vercel.json"):
    with open("vercel.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for r in data.get("rewrites", []):
            if not r["source"].endswith("(.*)"):
                REW_RITES[r["source"]] = r["destination"]

class VercelLocalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        if not path:
            path = "/"
        
        # Match rewrites
        if path in REW_RITES:
            self.path = REW_RITES[path]
            if parsed.query:
                self.path += "?" + parsed.query
        elif not os.path.splitext(path)[1] and path != "/":
            # If requesting something like /about without extension, check if /pages/about.html exists
            page_path = os.path.join(os.getcwd(), "pages", path.lstrip('/') + ".html")
            if os.path.exists(page_path):
                self.path = "/pages" + path + ".html"
                if parsed.query:
                    self.path += "?" + parsed.query
                    
        return super().do_GET()

if __name__ == '__main__':
    # Ensure address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VercelLocalHandler) as httpd:
        print(f"Serving local Vercel site on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
