"""Turn the scanner page (artifact source) into the app's www/index.html."""
import re, pathlib
root = pathlib.Path(__file__).parent
src = (root / "src" / "index.html").read_text(encoding="utf-8")
# bundled copies instead of the CDN, so the app works offline
src = re.sub(r'https://cdnjs\.cloudflare\.com/ajax/libs/[^"]*/([^"/]+\.js)', r'vendor/\1', src)
head = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<style>
:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); color-scheme: light; }
body { margin: 0; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
</head>
<body>
"""
(root / "www" / "index.html").write_text(head + src + "\n</body>\n</html>\n", encoding="utf-8")
print("www/index.html", len(src), "chars; cdn refs left:", src.count("cdnjs"))
