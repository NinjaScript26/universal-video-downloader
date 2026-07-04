# Universal Video Downloader

A tiny, open-source web UI over [yt-dlp](https://github.com/yt-dlp/yt-dlp).
Downloads from **YouTube, Facebook, Instagram, LinkedIn** and [1800+ other sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

- **Two modes** — a single video / short / reel, or an **entire channel, playlist, shorts tab or reels feed** (with an optional "max videos" limit)
- Quality picker: best / 1080p / 720p / 480p / MP3 (audio only)
- Private or login-gated content: reuses the logged-in session of your own browser (`--cookies-from-browser`) — no cookie files to export
- Live progress streamed straight from yt-dlp, with cancel
- **Zero Python dependencies** — one file of stdlib, plus the yt-dlp CLI

## Requirements

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pipx install yt-dlp`, or the standalone binary:
  `curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp && chmod a+rx ~/.local/bin/yt-dlp`
- [ffmpeg](https://ffmpeg.org) (for MP3 and merging best quality): `sudo apt install ffmpeg` / `brew install ffmpeg` / `winget install ffmpeg`
- For YouTube: a JavaScript runtime — [deno](https://deno.com) or [node](https://nodejs.org) (auto-detected)

## Run

```bash
python3 app.py
```

Open <http://127.0.0.1:8000>, paste a link, pick a mode and quality, hit Download.
Files land in the `downloads/` folder (batch downloads get one subfolder per channel/playlist).

## Link examples

| What | Example link | Mode |
|---|---|---|
| YouTube video / Short | `youtube.com/watch?v=…`, `youtube.com/shorts/…` | Single |
| Whole channel | `youtube.com/@name/videos` | Batch |
| Channel's Shorts only | `youtube.com/@name/shorts` | Batch |
| Playlist | `youtube.com/playlist?list=…` | Batch |
| Instagram post / reel | `instagram.com/reel/…` | Single |
| Instagram profile reels | `instagram.com/username/reels/` | Batch |
| Facebook video / reel | `facebook.com/watch?v=…`, `fb.watch/…` | Single |
| LinkedIn post video | `linkedin.com/posts/…` | Single |

**Instagram, Facebook and LinkedIn usually require login**: pick your browser
under *Login cookies* so yt-dlp can reuse your existing session. Close Chrome
first on Windows if the cookie database is locked.

## Troubleshooting

Most download errors are fixed by updating yt-dlp (platforms change constantly):

```bash
pipx upgrade yt-dlp   # or: pip install -U yt-dlp
```

## Legal / educational notice

This tool is for **personal and educational use only**. Download only content
you own, that is freely licensed, or that you otherwise have the right to
download. Respect copyright law and each platform's Terms of Service. The
authors take no responsibility for misuse.

## License

[MIT](LICENSE)
