#!/usr/bin/env python3
"""Universal Video Downloader — one-file web UI over yt-dlp.

Educational use only: download only content you have the right to download,
and respect each platform's Terms of Service.
"""
import json
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOWNLOADS = ROOT / "downloads"

FORMATS = {
    "best": ["-f", "bv*+ba/b"],
    "1080": ["-f", "bv*[height<=1080]+ba/b[height<=1080]/b"],
    "720": ["-f", "bv*[height<=720]+ba/b[height<=720]/b"],
    "480": ["-f", "bv*[height<=480]+ba/b[height<=480]/b"],
    "mp3": ["-x", "--audio-format", "mp3", "--audio-quality", "192K"],
}
BROWSERS = {"chrome", "firefox", "edge", "brave", "safari", "chromium", "opera"}
# YouTube needs a JS runtime for full extraction; only deno is on by default
JS_RUNTIME = next((r for r in ("deno", "node", "bun") if shutil.which(r)), None)


def command(o):
    url = o.get("url", "").strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")
    quality = o.get("quality", "best")
    if quality not in FORMATS:
        raise ValueError("Unknown quality")
    cmd = ["yt-dlp", "--newline", "--no-colors", *FORMATS[quality]]
    if JS_RUNTIME:
        cmd += ["--js-runtimes", JS_RUNTIME]
    if quality != "mp3":
        cmd += ["--merge-output-format", "mp4"]
    if o.get("mode") == "batch":  # whole channel / playlist / shorts tab / reels feed
        out = "%(playlist_title,channel,uploader|batch)s/%(playlist_autonumber)03d - %(title).150B [%(id)s].%(ext)s"
        cmd += ["--ignore-errors"]
        if o.get("limit"):
            cmd += ["--playlist-items", f"1:{int(o['limit'])}"]
    else:
        out = "%(title).150B [%(id)s].%(ext)s"
        cmd += ["--no-playlist"]
    if o.get("cookies") in BROWSERS:  # private/login-gated content
        cmd += ["--cookies-from-browser", o["cookies"]]
    cmd += ["-o", str(DOWNLOADS / out), "--", url]
    return cmd


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/download":
            self.send_error(404)
            return
        try:
            opts = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            cmd = command(opts)
        except (ValueError, KeyError) as e:
            self.send_error(400, str(e))
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        try:
            for line in proc.stdout:
                self.wfile.write(line.encode())
                self.wfile.flush()
            proc.wait()
            done = "finished" if proc.returncode == 0 else f"exited with code {proc.returncode}"
            self.wfile.write(f"\n== {done} — files are in {DOWNLOADS} ==\n".encode())
        except BrokenPipeError:  # cancel button / tab closed
            proc.terminate()

    def log_message(self, *args):  # ponytail: yt-dlp's output is the log
        pass


if __name__ == "__main__":
    if "--check" in sys.argv:
        c = command({"url": "https://e.com/v", "mode": "batch", "quality": "720",
                     "limit": 5, "cookies": "firefox"})
        assert c[-1] == "https://e.com/v" and c[-2] == "--"
        assert "--playlist-items" in c and "--cookies-from-browser" in c
        assert "--no-playlist" in command({"url": "https://e.com/v", "quality": "mp3"})
        for bad in [{"url": "file:///etc/passwd"}, {"url": "https://e.com/v", "quality": "x"}]:
            try:
                command(bad)
                raise AssertionError(bad)
            except ValueError:
                pass
        print("ok")
        sys.exit()
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp not found. Install it first: pipx install yt-dlp  (or: pip install yt-dlp)")
    if not shutil.which("ffmpeg"):
        print("warning: ffmpeg not found — needed for MP3 and best-quality merging")
    DOWNLOADS.mkdir(exist_ok=True)
    print("Universal Video Downloader → http://127.0.0.1:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
