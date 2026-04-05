from __future__ import annotations

import html
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
DATA_PATH = WORKSPACE / "data" / "puzzles.json"
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


GAME_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
{ga_snippet}
    <meta name="robots" content="noindex,follow" />
    <meta name="theme-color" content="#1f88dd" />
    <link rel="canonical" href="{canonical}" />
    <link rel="preload" href="/data/puzzles.json" as="fetch" crossorigin="anonymous" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="stylesheet" href="/assets/styles.css" />
  </head>
  <body data-page-mode="puzzle" data-puzzle-id="{puzzle_id}">
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
          <a class="size-tab size-tab--aux" href="/articles/">Articles</a>
        </nav>
      </header>

      <section class="hero-card">
        <div class="hero-copy">
          <p class="eyebrow">Puzzle Page</p>
          <h1 id="page-heading">{heading}</h1>
          <p id="page-subtitle" class="subtitle">
            {subtitle}
          </p>
          <div class="meta-strip hero-meta-strip">
            <div class="meta-card">
              <span class="meta-label">Size</span>
              <strong id="size-value">{size_label}</strong>
            </div>
            <div class="meta-card">
              <span class="meta-label">Timer</span>
              <strong id="timer">00:00</strong>
            </div>
            <div class="meta-card">
              <span class="meta-label">Difficulty</span>
              <strong id="collection-value">{difficulty_label}</strong>
            </div>
          </div>
        </div>

        <div class="game-panel">
          <div class="panel-top">
            <div
              class="difficulty-switch"
              role="group"
              aria-label="Select puzzle difficulty"
            >
              <button type="button" data-difficulty="easy">Easy</button>
              <button type="button" data-difficulty="medium">Medium</button>
              <button type="button" data-difficulty="hard">Hard</button>
            </div>
          </div>

          <div class="board-frame">
            <div
              id="board"
              class="board"
              aria-label="Math crossword board"
              role="grid"
            ></div>
          </div>

          <p id="status" class="status-line" aria-live="polite"></p>

          <section class="tray-panel" aria-labelledby="tray-heading">
            <div class="tray-heading-row">
              <h2 id="tray-heading">Numbers Tray</h2>
            </div>
            <div id="tray" class="tray" aria-label="Available values"></div>
          </section>

          <div class="controls">
            <button type="button" id="reset-button">Reset</button>
            <button type="button" id="hint-button">Hint</button>
            <button type="button" id="check-button">Check</button>
            <button type="button" id="new-puzzle-button" class="accent-button">
              New Puzzle
            </button>
          </div>

          <div class="tool-actions">
            <button type="button" id="print-button" class="ghost-button">
              Print Puzzle
            </button>
            <button type="button" id="copy-link-button" class="ghost-button">
              Copy Link
            </button>
          </div>
        </div>
      </section>

      <section class="seo-stack puzzle-link-stack" aria-label="Puzzle links">
        <section class="seo-card puzzle-links">
          <h2>More Ways to Use This Puzzle</h2>
          <div class="seo-link-grid">
            <a class="seo-link-card" href="{size_path}">
              <strong>Back to {size_label}</strong>
              <span>Open the main {size_label} category page and browse the format.</span>
            </a>
            <a class="seo-link-card" href="{size_path}">
              <strong>More {size_label} puzzles</strong>
              <span>Play more boards in the same size with fresh IDs and stable links.</span>
            </a>
            <a class="seo-link-card" href="/print/{puzzle_id}/">
              <strong>Printable version</strong>
              <span>Open the paper-friendly page with QR back to this exact puzzle.</span>
            </a>
            <a class="seo-link-card" href="/how-to-play-math-crossword/">
              <strong>How to play</strong>
              <span>Review rules, tray controls, and beginner solving tips.</span>
            </a>
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

    <div id="completion-popup" class="completion-overlay" hidden>
      <div
        class="completion-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="completion-title"
      >
        <p class="eyebrow">Completed</p>
        <h2 id="completion-title">Puzzle solved</h2>
        <p id="completion-summary" class="completion-summary"></p>
        <div class="completion-actions">
          <button type="button" id="popup-next-button" class="accent-button">
            Next Puzzle
          </button>
          <button type="button" id="popup-print-button">
            Print
          </button>
          <button type="button" id="popup-copy-link-button">
            Copy Link
          </button>
        </div>
      </div>
    </div>

    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""


PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} Print View</title>
    <meta name="description" content="{description}" />
{ga_snippet}
    <meta name="robots" content="noindex,follow" />
    <meta name="theme-color" content="#1f88dd" />
    <link rel="canonical" href="{canonical}" />
    <link rel="preload" href="/data/puzzles.json" as="fetch" crossorigin="anonymous" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="stylesheet" href="/assets/styles.css" />
  </head>
  <body class="print-page" data-page-mode="print" data-puzzle-id="{puzzle_id}">
    <main class="print-shell">
      <section class="print-card">
        <div class="print-header">
          <div>
            <p class="eyebrow">Printable Puzzle</p>
            <h1 id="page-heading">{heading}</h1>
            <p id="page-subtitle">{subtitle}</p>
          </div>
          <div class="print-actions">
            <button type="button" id="print-page-button" class="accent-button">Print</button>
            <a id="open-online-button" class="ghost-button" href="/puzzle/{puzzle_id}/">Open Online</a>
          </div>
        </div>

        <div class="print-body">
          <div>
            <div class="board-frame">
              <div id="print-board" class="board print-board" aria-label="Printable math crossword"></div>
            </div>
          </div>
          <aside class="print-side">
            <div>
              <p class="eyebrow">Solve online</p>
              <h2 id="print-title">{heading}</h2>
            </div>
            <img id="print-qr" class="print-qr" alt="QR code" />
            <a id="print-link" class="print-link" href="/puzzle/{puzzle_id}/"></a>
          </aside>
        </div>
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

    <script type="module" src="/src/print-entry.js"></script>
  </body>
</html>
"""


def title_case(value: str) -> str:
    return value[0].upper() + value[1:]


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def render_pages() -> None:
    puzzles = json.loads(DATA_PATH.read_text())

    for puzzle in puzzles:
        size_label = f"{puzzle['size']}x{puzzle['size']}"
        difficulty_label = title_case(puzzle["difficulty"])
        title = f"Math Crossword {size_label} {difficulty_label} Puzzle #{puzzle['index']}"
        heading = f"{size_label} {difficulty_label} Math Crossword"
        description = f"Play a {size_label} {puzzle['difficulty']} math crossword puzzle online."
        canonical = f"https://example.com/puzzle/{puzzle['id']}/"
        subtitle = "Stable URL puzzle from the fixed library. Print it, copy the link, or jump back online with the QR code."
        size_path = f"/{puzzle['size']}x{puzzle['size']}-math-crossword/"

        game_html = GAME_TEMPLATE.format(
            title=escape(title),
            description=escape(description),
            ga_snippet=GA_SNIPPET,
            canonical=escape(canonical),
            puzzle_id=escape(puzzle["id"]),
            heading=escape(heading),
            subtitle=escape(subtitle),
            size_label=escape(size_label),
            difficulty_label=escape(difficulty_label),
            size_path=escape(size_path),
        )
        print_html = PRINT_TEMPLATE.format(
            title=escape(title),
            description=escape(description),
            ga_snippet=GA_SNIPPET,
            canonical=escape(canonical),
            puzzle_id=escape(puzzle["id"]),
            heading=escape(heading),
            subtitle=escape("Print-friendly view with QR back to the online puzzle."),
        )

        puzzle_dir = WORKSPACE / "puzzle" / puzzle["id"]
        print_dir = WORKSPACE / "print" / puzzle["id"]
        puzzle_dir.mkdir(parents=True, exist_ok=True)
        print_dir.mkdir(parents=True, exist_ok=True)
        (puzzle_dir / "index.html").write_text(game_html)
        (print_dir / "index.html").write_text(print_html)


if __name__ == "__main__":
    render_pages()
