import sys
import os
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000

class GodotWebRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 加入跨來源隔離標頭 (COOP & COEP)，保證 WebAssembly 與 Web Audio 正常運作
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def guess_type(self, path):
        # 確保 WASM 與 JS MIME 類型正確
        if path.endswith(".wasm"):
            return "application/wasm"
        elif path.endswith(".pck"):
            return "application/octet-stream"
        elif path.endswith(".js"):
            return "application/javascript"
        return super().guess_type(path)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    mimetypes.add_type("application/wasm", ".wasm")
    mimetypes.add_type("application/octet-stream", ".pck")

    server_address = ("localhost", PORT)
    httpd = HTTPServer(server_address, GodotWebRequestHandler)
    print("=" * 60)
    print(f"🚀 Godot 4 Web 本地伺服器已啟動！")
    print(f"👉 請在瀏覽器開啟： http://localhost:{PORT}/TestWeb.html")
    print(f"   (已啟用 COOP/COEP 標頭與 Web Audio 安全上下文)")
    print("   按 Ctrl + C 可停止伺服器")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止。")
