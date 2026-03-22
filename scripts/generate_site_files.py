from __future__ import annotations

import html
from datetime import date
from pathlib import Path

import generate_articles
import generate_seo_pages


WORKSPACE = Path(__file__).resolve().parents[1]
BASE_URL = "https://example.com"
LASTMOD = date.today().isoformat()
GA_SNIPPET = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-38FFB5J2HT"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-38FFB5J2HT');
    </script>
""".rstrip()


ROBOTS_TXT = f"""User-agent: *
Allow: /
Disallow: /print/
Disallow: /tmp/
Disallow: /draft/
Disallow: /debug/
Disallow: /experimental/

Sitemap: {BASE_URL}/sitemap.xml
"""

WEBMANIFEST = """{
  "name": "Math Crossword",
  "short_name": "Math Crossword",
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#1f88dd",
  "background_color": "#efe1c9",
  "display": "standalone"
}
"""


NOT_FOUND_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Not Found – Math Crossword</title>
    <meta name="description" content="The page you opened could not be found. Return to the main math crossword pages, sizes, or articles." />
    <meta name="robots" content="noindex,follow" />
{ga_snippet}
    <meta name="theme-color" content="#1f88dd" />
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="stylesheet" href="/assets/styles.css" />
  </head>
  <body class="article-page">
    <main class="page-shell">
      <header class="page-topbar">
        <a class="site-logo" href="/" aria-label="Math Crossword home">
          <span class="site-logo-mark">MC</span>
          <span class="site-logo-copy">
            <span class="site-logo-title">Math Crossword</span>
            <span class="site-logo-subtitle">Puzzle Library</span>
          </span>
        </a>
        <nav class="size-tabs" aria-label="Puzzle sizes">
          <a class="size-tab" href="/5x5-math-crossword/" data-size="5">5x5</a>
          <a class="size-tab" href="/7x7-math-crossword/" data-size="7">7x7</a>
          <a class="size-tab" href="/9x9-math-crossword/" data-size="9">9x9</a>
          <a class="size-tab" href="/11x11-math-crossword/" data-size="11">11x11</a>
        </nav>
      </header>

      <section class="article-hero">
        <p class="eyebrow">Error</p>
        <h1>Page not found</h1>
        <p class="subtitle">The page you tried to open is not available. Use one of the links below to get back to the main playable sections of the site.</p>
      </section>

      <section class="seo-stack" aria-label="404 recovery links">
        <section class="seo-card">
          <h2>Go Back to a Live Page</h2>
          <div class="seo-link-grid">
            {links}
          </div>
        </section>
      </section>

      <footer class="site-footer">
        <div class="site-footer__inner">
          <nav class="site-footer__nav" aria-label="Footer">
            <a href="/articles/">Articles</a>
          </nav>
          <span class="site-footer__credit">
            by <a href="https://lukichev.biz/" rel="me">lukichev.biz</a>
          </span>
        </div>
      </footer>
    </main>
  </body>
</html>
"""


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build_sitemap() -> str:
    urls = [page["canonical"] for page in generate_seo_pages.PAGES]
    urls.append(f"{BASE_URL}/articles/")
    urls.extend(f"{BASE_URL}/articles/{article['slug']}/" for article in generate_articles.ARTICLES)

    items = "\n".join(
        f"  <url><loc>{escape(url)}</loc><lastmod>{LASTMOD}</lastmod></url>" for url in urls
    )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}\n"
        "</urlset>\n"
    )


def build_not_found_page() -> str:
    link_items = [
        ("Home", "/", "Return to the main playable math crossword page."),
        ("5x5 Math Crossword", "/5x5-math-crossword/", "Open quick beginner-friendly puzzles."),
        ("7x7 Math Crossword", "/7x7-math-crossword/", "Play the balanced mid-size board."),
        ("9x9 Math Crossword", "/9x9-math-crossword/", "Try a larger logic challenge."),
        ("11x11 Math Crossword", "/11x11-math-crossword/", "Open the biggest puzzle format."),
        ("Articles", "/articles/", "Read guides about printable play, kids, and brain training."),
    ]

    cards = []
    for title, href, text in link_items:
        cards.append(
            f"""
            <a class="seo-link-card" href="{escape(href)}">
              <strong>{escape(title)}</strong>
              <span>{escape(text)}</span>
            </a>
            """.strip()
        )

    return NOT_FOUND_TEMPLATE.format(
        ga_snippet=GA_SNIPPET,
        canonical=escape(f"{BASE_URL}/404.html"),
        links="\n".join(cards),
    )


def main() -> None:
    write_text(WORKSPACE / "robots.txt", ROBOTS_TXT)
    write_text(WORKSPACE / "site.webmanifest", WEBMANIFEST)
    write_text(WORKSPACE / "sitemap.xml", build_sitemap())
    write_text(WORKSPACE / "404.html", build_not_found_page())


if __name__ == "__main__":
    main()
