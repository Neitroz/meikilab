import os, re, glob, shutil, tempfile, base64, hmac, urllib.request
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_file, send_from_directory
import yt_dlp

app = Flask(__name__, static_folder="static", static_url_path="")
KEY = os.environ.get("APP_KEY", "")          # mot de passe d'accès (recommandé)
HOSTS = ("tiktok.com", "instagram.com")      # seuls ces sites sont acceptés


def host_ok(u):
    p = urlparse(u)
    h = p.hostname or ""
    return p.scheme in ("http", "https") and any(h == d or h.endswith("." + d) for d in HOSTS)


def why(e):
    lines = re.sub(r"\x1b\[[0-9;]*m", "", str(e)).strip().splitlines()
    return (lines or ["erreur inconnue"])[-1][:220]


def opts(extra=None):
    o = {"quiet": True, "no_warnings": True, "noplaylist": True, "socket_timeout": 20}
    if os.path.exists("cookies.txt"):          # utile pour Instagram
        o["cookiefile"] = "cookies.txt"
    if extra:
        o.update(extra)
    return o


@app.before_request
def guard():
    if KEY and request.path.startswith("/api/"):
        if not hmac.compare_digest(request.headers.get("X-Key", ""), KEY):
            return jsonify(error="Clé d'accès invalide"), 401


@app.get("/")
def home():
    return send_from_directory("static", "index.html")


@app.get("/api/info")
def info():
    u = request.args.get("url", "").strip()
    if not host_ok(u):
        return jsonify(error="Lien non supporté (TikTok ou Instagram uniquement)"), 400
    try:
        with yt_dlp.YoutubeDL(opts()) as y:
            d = y.extract_info(u, download=False)
        if d.get("entries"):
            d = next(iter(d["entries"]))
    except Exception as e:
        app.logger.warning("info failed: %s", e)
        return jsonify(error="Lien refusé : " + why(e)), 422
    thumb = None
    if d.get("thumbnail"):
        try:
            rq = urllib.request.Request(d["thumbnail"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(rq, timeout=10) as r:
                b = r.read(3_000_000)
                thumb = "data:%s;base64,%s" % (r.headers.get_content_type(), base64.b64encode(b).decode())
        except Exception:
            pass
    return jsonify(title=d.get("title") or "", track=d.get("track") or "",
                   artist=d.get("artist") or d.get("uploader") or "",
                   duration=d.get("duration"), thumb=thumb)


@app.get("/api/audio")
def audio():
    u = request.args.get("url", "").strip()
    if not host_ok(u):
        return jsonify(error="Lien non supporté"), 400
    tmp = tempfile.mkdtemp()
    try:
        o = opts({"format": "bestaudio/best", "outtmpl": os.path.join(tmp, "a.%(ext)s"),
                  "match_filter": yt_dlp.utils.match_filter_func("duration < 900"),
                  "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
                                      "preferredquality": "192"}]})
        with yt_dlp.YoutubeDL(o) as y:
            y.download([u])
        f = glob.glob(os.path.join(tmp, "a.*"))[0]
        r = send_file(f, mimetype="audio/mpeg")
        r.call_on_close(lambda: shutil.rmtree(tmp, ignore_errors=True))
        return r
    except Exception as e:
        app.logger.warning("audio failed: %s", e)
        shutil.rmtree(tmp, ignore_errors=True)
        return jsonify(error="Extraction impossible : " + why(e)), 422


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
