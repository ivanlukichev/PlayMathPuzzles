from __future__ import annotations

import html
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]

SIZE_LINKS = [
    ("5x5", "/5x5-math-crossword/", "Fast, beginner-friendly puzzles for quick sessions."),
    ("7x7", "/7x7-math-crossword/", "A balanced format with more crossings and more logic."),
    ("9x9", "/9x9-math-crossword/", "Longer chains and deeper solving for experienced players."),
    ("11x11", "/11x11-math-crossword/", "The largest grid for focused, expert-style play."),
]

DIFFICULTY_LINKS = [
    ("Easy", "/math-crossword-easy/", "Gentle starts with simpler numbers and more givens."),
    ("Medium", "/math-crossword-medium/", "A balanced level with a mix of arithmetic and logic."),
    ("Hard", "/math-crossword-hard/", "Fewer givens, tighter logic, and tougher deductions."),
]

RESOURCE_LINKS = [
    ("How to Play", "/how-to-play-math-crossword/", "Learn the rules, controls, and beginner strategy."),
    ("Printable Puzzles", "/printable-math-crossword/", "Print puzzles, share links, and continue online with QR."),
]

ARTICLES_LINK = ("Articles", "/articles/", "Read guides on brain training, printable use, kids, and classroom play.")
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

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
{ga_snippet}
    <meta name="theme-color" content="#1f88dd" />
    <link rel="canonical" href="{canonical}" />
    <link rel="preload" href="/data/puzzles.json" as="fetch" crossorigin="anonymous" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="stylesheet" href="/assets/styles.css" />
  </head>
  <body {body_attrs}>
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
          <p class="eyebrow">{eyebrow}</p>
          <h1 id="page-heading">{heading}</h1>
          <p id="page-subtitle" class="subtitle">
            {subtitle}
          </p>
          <div class="meta-strip hero-meta-strip">
            <div class="meta-card">
              <span class="meta-label">Size</span>
              <strong id="size-value">{size_value}</strong>
            </div>
            <div class="meta-card">
              <span class="meta-label">Timer</span>
              <strong id="timer">00:00</strong>
            </div>
            <div class="meta-card">
              <span class="meta-label">Difficulty</span>
              <strong id="collection-value">{difficulty_value}</strong>
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

      <section class="seo-stack" aria-label="Page content">
        {content_html}
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

REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="robots" content="noindex,follow" />
    <title>Redirecting…</title>
    <link rel="canonical" href="{target}" />
    <script>
      window.location.replace("{target}");
    </script>
  </head>
  <body>
    <p>Redirecting to <a href="{target}">{target}</a>…</p>
  </body>
</html>
"""


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def section(title: str, *parts: str) -> str:
    body = "\n".join(parts)
    return f"""
        <section class="seo-card">
          <h2>{escape(title)}</h2>
          {body}
        </section>
    """.strip()


def paragraph(text: str) -> str:
    return f"<p>{escape(text)}</p>"


def bullets(items: list[str]) -> str:
    entries = "\n".join(f"<li>{escape(item)}</li>" for item in items)
    return f'<ul class="seo-list">\n{entries}\n</ul>'


def link_cards(items: list[tuple[str, str, str]]) -> str:
    cards = []
    for title, href, text in items:
        cards.append(
            f"""
            <a class="seo-link-card" href="{escape(href)}">
              <strong>{escape(title)}</strong>
              <span>{escape(text)}</span>
            </a>
            """.strip()
        )

    return '<div class="seo-link-grid">\n' + "\n".join(cards) + "\n</div>"


def faq(items: list[tuple[str, str]]) -> str:
    entries = []
    for question, answer in items:
        entries.append(
            f"""
            <article class="faq-item">
              <h3>{escape(question)}</h3>
              <p>{escape(answer)}</p>
            </article>
            """.strip()
        )

    return section("Frequently Asked Questions", '<div class="faq-grid">\n' + "\n".join(entries) + "\n</div>")


def build_body_attrs(default_size: int | None, default_difficulty: str | None) -> str:
    attrs = ['data-page-mode="home"']

    if default_size is not None:
        attrs.append(f'data-default-size="{default_size}"')

    if default_difficulty is not None:
        attrs.append(f'data-default-difficulty="{escape(default_difficulty)}"')

    return " ".join(attrs)


def render_page(config: dict[str, object]) -> str:
    return PAGE_TEMPLATE.format(
        title=escape(config["title"]),
        description=escape(config["description"]),
        ga_snippet=GA_SNIPPET,
        canonical=escape(config["canonical"]),
        body_attrs=build_body_attrs(config.get("default_size"), config.get("default_difficulty")),
        eyebrow=escape(config["eyebrow"]),
        heading=escape(config["heading"]),
        subtitle=escape(config["subtitle"]),
        size_value=escape(config["size_value"]),
        difficulty_value=escape(config["difficulty_value"]),
        content_html="\n".join(config["sections"]),
    )


HOME_SECTIONS = [
    section(
        "What Is a Math Crossword Puzzle?",
        paragraph(
            "A math crossword puzzle is a number puzzle where arithmetic takes the place of words. Instead of filling letters into clues, you place missing numbers so that every horizontal and vertical equation is valid."
        ),
        paragraph(
            "The format feels familiar if you enjoy classic crosswords, but the thinking is different. You watch how one answer affects another, use the tray to track which numbers are still available, and solve the grid through logic, arithmetic, and pattern recognition."
        ),
        paragraph(
            "That mix makes math crosswords useful for both fun and practice. They build confidence with basic operations, reward careful reasoning, and stay approachable because every move gives you more information."
        ),
    ),
    section(
        "How to Play Math Crossword Online",
        paragraph(
            "Start by choosing a number from the tray or by tapping an empty cell in the grid. The game supports both directions, so you can think in the order that feels natural."
        ),
        bullets(
            [
                "Pick a value and place it into a white cell, or pick the cell first and then choose the value.",
                "Use the givens, operators, and equals signs to test what can fit.",
                "Tap Hint if you want one correct value revealed.",
                "Use Check when you want to see whether the puzzle is solved correctly.",
                "Hit New Puzzle to load another crossword in the same category.",
            ]
        ),
        paragraph(
            "Because every puzzle lives in a fixed library, you can also copy a link, open a direct puzzle URL, or print a version of the same grid for paper solving."
        ),
    ),
    section(
        "Choose Your Puzzle Size",
        paragraph(
            "Different grid sizes create different solving rhythms. Smaller boards are quick and friendly, while larger boards ask for longer chains of reasoning and more sustained attention."
        ),
        link_cards(SIZE_LINKS),
        paragraph(
            "If you are new to the format, start with 5x5 or 7x7. If you want a deeper logic workout, move up to 9x9 or 11x11 and let the extra crossings guide the solve."
        ),
    ),
    section(
        "Difficulty Levels",
        paragraph(
            "Each size supports three clear difficulty levels. Easy uses simpler numbers and more givens. Medium is the balanced everyday mode. Hard reduces help and asks you to lean more on deduction."
        ),
        link_cards(DIFFICULTY_LINKS),
        paragraph(
            "That means you can choose whether you want a fast warm-up, a relaxed practice session, or a more demanding puzzle that unfolds step by step."
        ),
    ),
    section(
        "Why Play Math Crossword Puzzles?",
        bullets(
            [
                "They train logical thinking without feeling like a worksheet.",
                "They give you regular arithmetic practice in a puzzle format.",
                "They are easy to start and satisfying to finish.",
                "They work well for children, adults, students, and casual brain-training fans.",
                "They fit short breaks as well as longer focused sessions.",
            ]
        ),
        paragraph(
            "Many players enjoy the calm rhythm of solving. You test a number, read the crossings, rule out weak options, and gradually watch the grid become more certain."
        ),
    ),
    section(
        "Printable and Shareable Puzzles",
        paragraph(
            "Every puzzle can be opened online, shared with a direct link, and printed in a clean paper-friendly format. Printable pages include a QR code, which makes it easy to return from paper back to the matching online puzzle."
        ),
        paragraph(
            "That is useful if you want to solve on paper at home, use a puzzle in class, send a challenge to a friend, or move between devices without losing the exact puzzle you picked."
        ),
        link_cards(RESOURCE_LINKS + [ARTICLES_LINK]),
    ),
    faq(
        [
            ("What is a math crossword puzzle?", "It is a crossword-style logic puzzle where you fill missing numbers so that every row and column equation is mathematically correct."),
            ("Can I play math crosswords for free?", "Yes. The site is built around a fixed free library of playable puzzles."),
            ("Are there different difficulty levels?", "Yes. Every playable size supports Easy, Medium, and Hard modes."),
            ("Can I print puzzles?", "Yes. Every puzzle has a print-friendly page, and the print version includes a QR code back to the online puzzle."),
            ("Which puzzle size should I start with?", "Most new players do best with 5x5 or 7x7 before moving into 9x9 and 11x11."),
        ]
    ),
]


def size_sections(
    about: list[str],
    audience: list[str],
    tips: list[str],
    other_sizes: list[tuple[str, str, str]],
    article_links: list[tuple[str, str, str]],
) -> list[str]:
    return [
        section("About This Puzzle Size", *(paragraph(text) for text in about)),
        section("Who Is This Puzzle Size For?", *(paragraph(text) for text in audience)),
        section(
            "Difficulty Options",
            paragraph(
                "This page includes Easy, Medium, and Hard math crossword puzzles. Easy gives you more traction at the start, Medium offers a balanced solve, and Hard asks for cleaner logic with less help."
            ),
            paragraph(
                "That range makes it easy to stay on one board size while adjusting the amount of challenge to match your mood, skill level, or available time."
            ),
            link_cards(DIFFICULTY_LINKS),
        ),
        section("Tips for Solving These Puzzles", bullets(tips)),
        section(
            "Try Other Grid Sizes",
            link_cards(other_sizes),
            link_cards(RESOURCE_LINKS + [ARTICLES_LINK, ("Home", "/", "Return to the main math crossword hub.")]),
            link_cards(article_links),
        ),
    ]


SIZE_PAGES = [
    {
        "path": "/5x5-math-crossword/index.html",
        "canonical": "https://example.com/5x5-math-crossword/",
        "title": "5x5 Math Crossword Puzzle – Play Online",
        "description": "Solve 5x5 math crossword puzzles online. A compact and fun number logic game for beginners and quick brain training.",
        "eyebrow": "Size Guide",
        "heading": "5x5 Math Crossword Puzzle",
        "subtitle": "Play short, approachable number crosswords that teach the rhythm of the game without overwhelming the board.",
        "size_value": "5x5",
        "difficulty_value": "Medium",
        "default_size": 5,
        "default_difficulty": "medium",
        "sections": size_sections(
            [
                "5x5 math crossword puzzles are the quickest way to get into the format. The board is compact, the clue structure is easier to read, and each move gives feedback fast.",
                "That makes 5x5 ideal for learning how rows and columns interact. You can see the full puzzle at a glance, spot obvious number placements earlier, and develop confidence before jumping to larger grids.",
                "It is also a great option when you want a puzzle break without committing to a long session. A 5x5 board feels light, but it still gives you enough crossings to be satisfying.",
            ],
            [
                "This size is a strong starting point for beginners, younger players, and anyone who wants a quick daily logic warm-up.",
                "It also works well for experienced solvers who want a short, clean puzzle between longer tasks or as a warm-up before moving into 7x7 and beyond.",
            ],
            [
                "Start with equations that already contain a result or a strong given number.",
                "Use the smaller grid to scan every crossing before committing to a guess.",
                "Keep an eye on the tray because duplicate values disappear quickly on compact boards.",
                "If you feel stuck, switch to the intersecting equation instead of staring at one line too long.",
                "Use Easy mode first if you are learning how math crosswords behave.",
            ],
            [item for item in SIZE_LINKS if item[0] != "5x5"],
            [
                ("Math Crossword for Kids", "/articles/math-crossword-for-kids/", "See why small easy boards work well for younger solvers."),
                ("Easy Daily Practice", "/articles/easy-math-crossword-routines-for-daily-practice/", "Use short 5x5 puzzles as a simple routine."),
            ],
        ),
        "faq": [
            ("Is 5x5 good for beginners?", "Yes. It is the easiest size to read quickly and the best place to learn the solving flow."),
            ("Can 5x5 still be challenging?", "Yes. Hard 5x5 puzzles can still ask for careful tray management and logical elimination."),
        ],
        "aliases": ["/5x5/index.html"],
    },
    {
        "path": "/7x7-math-crossword/index.html",
        "canonical": "https://example.com/7x7-math-crossword/",
        "title": "7x7 Math Crossword Puzzle – Play Online",
        "description": "Play 7x7 math crossword puzzles online. Enjoy a balanced number logic challenge with more crossings and richer deduction.",
        "eyebrow": "Size Guide",
        "heading": "7x7 Math Crossword Puzzle",
        "subtitle": "A balanced board size for regular practice, with enough crossings to feel thoughtful without becoming overwhelming.",
        "size_value": "7x7",
        "difficulty_value": "Medium",
        "default_size": 7,
        "default_difficulty": "medium",
        "sections": size_sections(
            [
                "7x7 math crosswords sit in the sweet spot between speed and depth. The grid has more moving parts than 5x5, but it still stays readable on a single screen.",
                "That extra space creates more intersections, which means your deductions travel farther. A number placed in one equation can unlock multiple lines, and that makes the solve feel more layered.",
                "For many players, 7x7 becomes the everyday format. It is big enough to be interesting, yet still short enough for a focused break or a daily routine.",
            ],
            [
                "This size is ideal for players who already understand the basics and want more substance without jumping straight into the longest boards.",
                "It is also a great choice for regular brain training because it rewards steady logic instead of speed alone.",
            ],
            [
                "Look for lines where one missing value affects two nearby equations at once.",
                "When the board opens up, use the tray counts to eliminate tempting but impossible repeats.",
                "Check result cells early because they often constrain several later moves.",
                "If one area stalls, move to another cluster and come back with fresh information.",
                "Medium mode is often the best place to learn this size before testing Hard.",
            ],
            [item for item in SIZE_LINKS if item[0] != "7x7"],
            [
                ("Choosing the Right Size", "/articles/choosing-the-right-math-crossword-size/", "Compare board sizes and pick the right solving rhythm."),
                ("Number Sense", "/articles/how-math-crosswords-build-number-sense/", "See how balanced grids strengthen pattern reading."),
            ],
        ),
        "faq": [
            ("Is 7x7 a good balance?", "Yes. It is often the best mix of speed, readability, and logic density."),
            ("Should I move from 5x5 to 7x7 next?", "Usually yes. It is the most natural step up for players who want more crossings and longer solves."),
        ],
        "aliases": ["/7x7/index.html"],
    },
    {
        "path": "/9x9-math-crossword/index.html",
        "canonical": "https://example.com/9x9-math-crossword/",
        "title": "9x9 Math Crossword Puzzle – Play Online",
        "description": "Play 9x9 math crossword puzzles online. Tackle a deeper number logic game with more crossings, longer chains, and stronger deduction.",
        "eyebrow": "Size Guide",
        "heading": "9x9 Math Crossword Puzzle",
        "subtitle": "Step into a more serious logic challenge with larger clusters, longer solving chains, and more satisfying payoffs.",
        "size_value": "9x9",
        "difficulty_value": "Medium",
        "default_size": 9,
        "default_difficulty": "medium",
        "sections": size_sections(
            [
                "9x9 math crossword puzzles feel noticeably deeper than the smaller formats. The board introduces more intersections, more delayed consequences, and more places where one correct value can reshape the solve.",
                "Because the grid is larger, you often need to build momentum in layers. Early placements may not finish a line right away, but they narrow the board enough for a second and third deduction to land.",
                "That makes 9x9 a rewarding format for experienced players who enjoy patient reasoning rather than quick completion alone.",
            ],
            [
                "This size is well suited to confident solvers who already feel comfortable with the controls and want longer sessions.",
                "It is also a good fit for puzzle fans who enjoy tracking several active possibilities before the board begins to resolve.",
            ],
            [
                "Treat the grid as clusters instead of trying to solve everything in strict order.",
                "Use strong givens and finished results to anchor one side of the board first.",
                "Watch repeated numbers carefully because the tray becomes a major source of information here.",
                "Expect progress to come in waves rather than one move at a time.",
                "If Hard feels too dense, stay on Medium until the larger board starts to feel natural.",
            ],
            [item for item in SIZE_LINKS if item[0] != "9x9"],
            [
                ("Brain Training", "/articles/brain-training-with-math-crosswords/", "Use larger boards for longer focus sessions."),
                ("Benefits of Math Puzzles", "/articles/benefits-of-math-puzzles/", "Why deeper boards are useful for logic and concentration."),
            ],
        ),
        "faq": [
            ("Is 9x9 harder than 7x7?", "In most cases yes, because it has more crossings and longer deduction chains."),
            ("Do 9x9 puzzles take longer?", "Usually yes. They are designed for more focused sessions and deeper logic work."),
        ],
        "aliases": ["/9x9/index.html"],
    },
    {
        "path": "/11x11-math-crossword/index.html",
        "canonical": "https://example.com/11x11-math-crossword/",
        "title": "11x11 Math Crossword Puzzle – Play Online",
        "description": "Challenge yourself with 11x11 math crossword puzzles online. Solve the largest number logic grids with long-form reasoning and expert focus.",
        "eyebrow": "Size Guide",
        "heading": "11x11 Math Crossword Puzzle",
        "subtitle": "Play the largest format on the site, built for long-form concentration, dense crossings, and expert-style deduction.",
        "size_value": "11x11",
        "difficulty_value": "Medium",
        "default_size": 11,
        "default_difficulty": "medium",
        "sections": size_sections(
            [
                "11x11 math crosswords are the biggest puzzles in the library. They create long solving sessions, multiple active regions, and plenty of moments where one breakthrough unlocks an entire section.",
                "The board rewards patience. You often have to hold partial information in several places, revisit lines after the tray changes, and trust that a small deduction will matter later.",
                "For experienced players, that is exactly the appeal. The larger format turns arithmetic and logic into a more immersive, puzzle-room style experience.",
            ],
            [
                "This size is best for players who already enjoy 9x9 puzzles and want an even bigger challenge.",
                "It is especially good for people who like slow, deliberate solving and do not mind spending more time building structure before the final cascade of answers appears.",
            ],
            [
                "Start by finding the densest cluster of givens instead of scanning the whole board evenly.",
                "Use finished results as anchors and expand outward from them.",
                "When several regions are open, rotate between them rather than forcing one line too hard.",
                "Trust tray counts. On the biggest boards, they often reveal what the equations do not show immediately.",
                "Save Hard mode for when Medium already feels readable and controlled.",
            ],
            [item for item in SIZE_LINKS if item[0] != "11x11"],
            [
                ("Brain Training", "/articles/brain-training-with-math-crosswords/", "See why long-form puzzles work well for sustained focus."),
                ("Benefits of Math Puzzles", "/articles/benefits-of-math-puzzles/", "Read how deep logic puzzles build patience and confidence."),
            ],
        ),
        "faq": [
            ("Is 11x11 the hardest format?", "Yes. It is the largest board on the site and usually the most demanding to solve cleanly."),
            ("Who should try 11x11?", "Players who already enjoy the bigger boards and want the longest, most involved math crossword sessions."),
        ],
        "aliases": ["/11x11/index.html"],
    },
]


DIFFICULTY_PAGES = [
    {
        "path": "/math-crossword-easy/index.html",
        "canonical": "https://example.com/math-crossword-easy/",
        "title": "Easy Math Crossword Puzzles – Play Online",
        "description": "Play easy math crossword puzzles online. Solve beginner-friendly number logic games with simpler numbers and more givens.",
        "eyebrow": "Difficulty Guide",
        "heading": "Easy Math Crossword Puzzles",
        "subtitle": "A friendly starting point with clearer openings, simpler numbers, and enough givens to help the logic flow quickly.",
        "size_value": "5x5",
        "difficulty_value": "Easy",
        "default_size": 5,
        "default_difficulty": "easy",
        "sections": [
            section(
                "What Makes This Difficulty Level Different?",
                paragraph("Easy math crossword puzzles are designed to feel readable from the start. You get simpler arithmetic, more givens, and enough structure to make early progress without too much friction."),
                paragraph("That does not make them trivial. The fun still comes from crossing equations and careful number placement, but the board opens faster and gives new players room to learn the format."),
            ),
            section(
                "Who Should Choose This Level?",
                paragraph("Easy is the best choice for beginners, children, casual puzzle players, and anyone who wants a lighter session."),
                paragraph("It is also useful as a warm-up mode. Even experienced solvers often enjoy an easy puzzle when they want a quick, clean solve without a heavy time commitment."),
            ),
            section(
                "Recommended Puzzle Sizes",
                paragraph("Easy works especially well on 5x5 and 7x7 boards because those sizes keep the puzzle readable while the extra givens teach the logic naturally."),
                link_cards([SIZE_LINKS[0], SIZE_LINKS[1], SIZE_LINKS[2]]),
            ),
            section(
                "Play More Math Crossword Levels",
                paragraph("Once Easy feels comfortable, move to Medium for a more balanced solve or jump to Hard when you want fewer givens and deeper reasoning."),
                link_cards([item for item in DIFFICULTY_LINKS if item[0] != "Easy"]),
                link_cards(RESOURCE_LINKS + [ARTICLES_LINK, ("Home", "/", "Return to the main math crossword hub.")]),
                link_cards(
                    [
                        ("Math Crossword for Kids", "/articles/math-crossword-for-kids/", "Use Easy mode and small boards for younger learners."),
                        ("Benefits of Math Puzzles", "/articles/benefits-of-math-puzzles/", "See why gentle puzzle practice supports confidence."),
                    ]
                ),
            ),
        ],
        "faq": [
            ("Is Easy good for beginners?", "Yes. Easy is built to teach the flow of the game with more help on the board."),
            ("Can Easy puzzles still be fun for adults?", "Yes. They are quick, clean, and satisfying when you want a relaxed brain-training session."),
        ],
    },
    {
        "path": "/math-crossword-medium/index.html",
        "canonical": "https://example.com/math-crossword-medium/",
        "title": "Medium Math Crossword Puzzles – Play Online",
        "description": "Play medium math crossword puzzles online. Enjoy balanced number logic games with steady deduction and satisfying arithmetic challenge.",
        "eyebrow": "Difficulty Guide",
        "heading": "Medium Math Crossword Puzzles",
        "subtitle": "Balanced puzzles for regular play, with enough givens to get started and enough resistance to keep the solve interesting.",
        "size_value": "7x7",
        "difficulty_value": "Medium",
        "default_size": 7,
        "default_difficulty": "medium",
        "sections": [
            section(
                "What Makes This Difficulty Level Different?",
                paragraph("Medium is the center of the library. It mixes arithmetic and deduction in a way that feels fair but not automatic, so you still have to read crossings carefully and manage the tray well."),
                paragraph("You usually get a few strong openings, but the board will not solve itself. Medium asks you to think through the interactions and build the answer step by step."),
            ),
            section(
                "Who Should Choose This Level?",
                paragraph("Medium is ideal for most players. If you understand the rules and want a satisfying puzzle without the heavier pressure of Hard, this is usually the right choice."),
                paragraph("It is especially good for regular practice because it stays engaging across every board size."),
            ),
            section(
                "Recommended Puzzle Sizes",
                paragraph("Medium plays well across the whole site, but 7x7 and 9x9 are especially strong because they combine balanced givens with rich crossing logic."),
                link_cards([SIZE_LINKS[1], SIZE_LINKS[2], SIZE_LINKS[3]]),
            ),
            section(
                "Play More Math Crossword Levels",
                paragraph("Stay on Medium when you want consistent challenge, drop to Easy for a faster solve, or move up to Hard for fewer givens and tighter deductions."),
                link_cards([item for item in DIFFICULTY_LINKS if item[0] != "Medium"]),
                link_cards(RESOURCE_LINKS + [ARTICLES_LINK, ("Home", "/", "Return to the main math crossword hub.")]),
                link_cards(
                    [
                        ("Choosing the Right Size", "/articles/choosing-the-right-math-crossword-size/", "Pick the board size that feels best for steady daily play."),
                        ("Number Sense", "/articles/how-math-crosswords-build-number-sense/", "Medium puzzles are a strong place to build arithmetic intuition."),
                    ]
                ),
            ),
        ],
        "faq": [
            ("Is Medium the default level?", "Yes. Medium is the best all-purpose starting level for most returning players."),
            ("Which size works best on Medium?", "Many players like 7x7 and 9x9 because they combine readable boards with stronger logic chains."),
        ],
    },
    {
        "path": "/math-crossword-hard/index.html",
        "canonical": "https://example.com/math-crossword-hard/",
        "title": "Hard Math Crossword Puzzles – Play Online",
        "description": "Challenge yourself with hard math crossword puzzles. Solve tricky number logic games with fewer givens and deeper reasoning.",
        "eyebrow": "Difficulty Guide",
        "heading": "Hard Math Crossword Puzzles",
        "subtitle": "A tougher mode with fewer givens, tighter logic, and more pressure on careful reading, tray control, and sustained attention.",
        "size_value": "9x9",
        "difficulty_value": "Hard",
        "default_size": 9,
        "default_difficulty": "hard",
        "sections": [
            section(
                "What Makes This Difficulty Level Different?",
                paragraph("Hard math crossword puzzles remove much of the early help. You see fewer givens, more delayed payoffs, and more moments where one wrong assumption can ripple across the board."),
                paragraph("That means the solve depends less on obvious starts and more on disciplined deduction. Hard mode rewards players who are comfortable reading several crossings and waiting for the best move."),
            ),
            section(
                "Who Should Choose This Level?",
                paragraph("Hard is best for experienced players, puzzle fans who enjoy slower reasoning, and anyone who wants a genuine challenge rather than a quick warm-up."),
                paragraph("If you are still learning the format, it usually makes sense to grow into Hard after Medium feels stable."),
            ),
            section(
                "Recommended Puzzle Sizes",
                paragraph("Hard becomes especially interesting on 9x9 and 11x11 because larger grids give the logic more room to build. Skilled players may also enjoy Hard 7x7 for compact but sharp puzzles."),
                link_cards([SIZE_LINKS[2], SIZE_LINKS[3], SIZE_LINKS[1]]),
            ),
            section(
                "Play More Math Crossword Levels",
                paragraph("If Hard feels too dense, step back to Medium for a balanced solve. If you want the same size with gentler openings, Easy can help you learn the board patterns first."),
                link_cards([item for item in DIFFICULTY_LINKS if item[0] != "Hard"]),
                link_cards(RESOURCE_LINKS + [ARTICLES_LINK, ("Home", "/", "Return to the main math crossword hub.")]),
                link_cards(
                    [
                        ("Brain Training", "/articles/brain-training-with-math-crosswords/", "Use hard boards for longer, more deliberate focus."),
                        ("Benefits of Math Puzzles", "/articles/benefits-of-math-puzzles/", "Read why tougher logic puzzles reward patience and confidence."),
                    ]
                ),
            ),
        ],
        "faq": [
            ("Is Hard best on large boards?", "Usually yes. Hard 9x9 and 11x11 give the deepest deduction chains."),
            ("Does Hard mean fewer givens?", "Yes. Hard mode is designed around less help and more logic."),
        ],
    },
]

HOW_TO_SECTIONS = [
    section(
        "What Is a Math Crossword?",
        paragraph("A math crossword is a crossword-style puzzle made from arithmetic instead of words. Some cells already show operators or fixed numbers, while other cells are blank and need to be filled with the correct values."),
        paragraph("Each horizontal and vertical line must form a valid equation. Because the equations cross, every number you place affects more than one part of the puzzle."),
    ),
    section(
        "Basic Rules",
        bullets(
            [
                "Only fill the white number cells.",
                "Operators and equals signs are fixed and cannot be changed.",
                "Every row and column equation must be mathematically correct.",
                "The tray shows which values are available for the puzzle.",
                "A completed puzzle must satisfy the whole grid, not just one line.",
            ]
        ),
        paragraph("The key idea is to solve with both arithmetic and cross-checking. A number that works in one line still has to fit every crossing equation that touches it."),
    ),
    section(
        "How to Fill the Grid",
        paragraph("You can play in two ways. Tap a value in the tray and then choose a cell, or tap a cell first and then choose the value you want to place. The game supports both flows so you can solve in the order that feels most natural."),
        paragraph("When both a cell and a value are selected, the number is placed automatically. The selected tray value stays active, which makes it easier to place the same number again if the puzzle needs duplicates."),
        bullets(
            [
                "Tap an already selected filled cell again to clear it.",
                "Use Reset if you want to restart the whole board.",
                "Use Hint when you want one correct value revealed.",
                "Use Check to confirm whether the full solution is correct.",
            ]
        ),
    ),
    section(
        "How Difficulty Works",
        paragraph("Difficulty changes the feel of the solve more than the rules. Easy puzzles use simpler numbers and more givens, so the board opens quickly. Medium is a balanced mode with enough structure to get started but enough resistance to stay interesting."),
        paragraph("Hard reduces help. You may get very few givens, repeated values in the tray matter more, and the solve depends more heavily on clean deduction rather than quick arithmetic alone."),
        link_cards(DIFFICULTY_LINKS),
    ),
    section(
        "Tips for Beginners",
        bullets(
            [
                "Start with 5x5 or 7x7 puzzles.",
                "Use Easy mode first so you can learn the pattern of crossings.",
                "Look for completed results and strong givens before scanning the whole board.",
                "Watch the tray counts because they tell you which numbers are still possible.",
                "If one area gets stuck, move to a crossing line and return later.",
            ]
        ),
        paragraph("Beginners often improve quickly once they stop trying to solve one line in isolation. The puzzle becomes easier when you let the crossings do part of the work."),
    ),
    section(
        "Common Mistakes",
        bullets(
            [
                "Forcing a number because it fits one equation but ignoring the crossing.",
                "Using up a tray value mentally without checking how many copies remain.",
                "Staying on one stubborn area for too long instead of rotating to another cluster.",
                "Jumping into Hard too early and treating confusion as a strategy problem instead of a difficulty mismatch.",
            ]
        ),
        paragraph("The best habit is simple: place only what the board supports, then let each confirmed number create the next opening."),
        link_cards(SIZE_LINKS + RESOURCE_LINKS + [ARTICLES_LINK]),
        link_cards(
            [
                ("Choosing the Right Size", "/articles/choosing-the-right-math-crossword-size/", "Match board size to your attention span and experience."),
                ("Math Crossword for Kids", "/articles/math-crossword-for-kids/", "See the best beginner path for younger players."),
            ]
        ),
    ),
    faq(
        [
            ("How do I start a math crossword?", "Choose a smaller board, stay on Easy or Medium, and begin with rows or columns that already show a result or a given number."),
            ("Do I have to solve rows before columns?", "No. You can solve in any order as long as every crossing remains valid."),
            ("What does the tray do?", "The tray shows which values are available and how many copies are still unused."),
            ("When should I use Hint?", "Hint is best when you understand the rules but need one solid number to reopen the board."),
            ("Is there a printable version?", "Yes. Every puzzle has a print page and a QR code back to the online version."),
        ]
    ),
]

PRINTABLE_SECTIONS = [
    section(
        "How to Print a Puzzle",
        paragraph("Every puzzle on the site has a print-friendly page. Open the puzzle you want, choose Print Puzzle, and you will get a cleaner layout built for paper solving."),
        paragraph("The print view removes the interactive controls and keeps the essentials: the grid, the heading, the link, and the QR code that points back to the exact online puzzle."),
    ),
    section(
        "Why Printable Puzzles Are Useful",
        paragraph("Printable math crosswords are useful when you want to solve away from the screen, use a puzzle in class, add one to a study session, or keep a few brain-training sheets at home."),
        paragraph("Paper solving also changes the rhythm in a nice way. Some players like writing possibilities by hand, scanning the board more slowly, and returning to the online version only when they want the same puzzle on another device."),
    ),
    section(
        "Use QR Codes to Continue Online",
        paragraph("Each print page includes a QR code that opens the matching online puzzle URL. That makes it easy to move from paper back to the live version without searching or trying to remember which puzzle you printed."),
        paragraph("It is especially handy for teachers, parents, and anyone sharing puzzles with friends. One printed sheet can become a smooth bridge back to the digital version."),
    ),
    section(
        "Best Puzzle Sizes for Printing",
        paragraph("5x5 and 7x7 are the easiest sizes to print for quick solving sessions. 9x9 and 11x11 are better when you want a longer paper challenge with more crossings and more time on the page."),
        link_cards(SIZE_LINKS),
    ),
    section(
        "Printable Puzzles for Home, School, and Brain Training",
        paragraph("Printable math crosswords work well for individual practice, classroom warm-ups, family puzzle time, and low-pressure arithmetic review."),
        paragraph("Because the puzzles are also shareable online, you can print a board for paper use, send the direct link to another person, or let someone scan the QR code and solve the same puzzle digitally."),
        paragraph("That flexibility makes printable pages useful beyond solo play. They can become quick classroom materials, short homework extras, rainy-day logic sheets, or a simple brain-training stack that stays ready on the desk."),
        link_cards(DIFFICULTY_LINKS + [("Home", "/", "Return to the main math crossword hub."), ("How to Play", "/how-to-play-math-crossword/", "Read the rules and solving basics."), ARTICLES_LINK]),
        link_cards(
            [
                ("Printable Puzzles for Schools", "/articles/printable-puzzles-for-schools/", "Use print pages in class, homework, and centers."),
                ("Screen-Free Math Practice", "/articles/screen-free-math-practice-with-printables/", "Build a simple paper-first routine with QR back to online play."),
            ]
        ),
    ),
    faq(
        [
            ("Can I print math crossword puzzles?", "Yes. Every puzzle has a print-friendly page designed for paper solving."),
            ("Does the print version include a QR code?", "Yes. The QR code takes you back to the same online puzzle."),
            ("Can I share a printable puzzle?", "Yes. You can share either the print page or the direct puzzle link."),
            ("Which size is best for printing?", "5x5 and 7x7 are best for quick sheets, while 9x9 and 11x11 are better for longer sessions."),
        ]
    ),
]

PAGES = [
    {
        "path": "/index.html",
        "canonical": "https://example.com/",
        "title": "Math Crossword Puzzles Online – Play Free Number Logic Games",
        "description": "Play math crossword puzzles online. Solve number-based logic games in different sizes and difficulty levels. Free and printable.",
        "eyebrow": "Main Puzzle Hub",
        "heading": "Math Crossword",
        "subtitle": "Play free number-based crossword puzzles online in multiple sizes, switch difficulty any time, and keep solving with printable and shareable puzzle links.",
        "size_value": "5x5",
        "difficulty_value": "Medium",
        "default_size": None,
        "default_difficulty": None,
        "sections": HOME_SECTIONS,
    },
    *SIZE_PAGES,
    *DIFFICULTY_PAGES,
    {
        "path": "/how-to-play-math-crossword/index.html",
        "canonical": "https://example.com/how-to-play-math-crossword/",
        "title": "How to Play Math Crossword – Rules, Tips, and Strategy",
        "description": "Learn how to play math crossword puzzles online. Read the rules, understand the grid, and pick up beginner tips for solving number crosswords.",
        "eyebrow": "How To Play",
        "heading": "How to Play Math Crossword",
        "subtitle": "Learn the rules, understand the grid, and build a solving routine that works on every size and difficulty level.",
        "size_value": "5x5",
        "difficulty_value": "Medium",
        "default_size": 5,
        "default_difficulty": "medium",
        "sections": HOW_TO_SECTIONS,
    },
    {
        "path": "/printable-math-crossword/index.html",
        "canonical": "https://example.com/printable-math-crossword/",
        "title": "Printable Math Crossword Puzzles – Print and Play",
        "description": "Print printable math crossword puzzles for home, school, and brain training. Use QR codes to continue each puzzle online.",
        "eyebrow": "Printable Puzzles",
        "heading": "Printable Math Crossword Puzzles",
        "subtitle": "Print a puzzle, solve on paper, and jump back online with a QR code whenever you want the exact same board on screen.",
        "size_value": "7x7",
        "difficulty_value": "Medium",
        "default_size": 7,
        "default_difficulty": "medium",
        "sections": PRINTABLE_SECTIONS,
    },
]


def write_page(path: str, html_output: str) -> None:
    destination = WORKSPACE / path.lstrip("/")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html_output)


def write_redirect(path: str, target: str) -> None:
    write_page(path, REDIRECT_TEMPLATE.format(target=escape(target)))


def append_page(page: dict[str, object], faq_items: list[tuple[str, str]] | None = None) -> None:
    config = dict(page)
    sections = list(config["sections"])

    if faq_items:
        sections.append(faq(faq_items))

    config["sections"] = sections
    html_output = render_page(config)
    write_page(config["path"], html_output)

    for alias in config.get("aliases", []):
        write_redirect(alias, config["path"].replace("/index.html", "/"))


def main() -> None:
    for page in PAGES:
        append_page(page, page.get("faq"))


if __name__ == "__main__":
    main()
