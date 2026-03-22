from __future__ import annotations

import html
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
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


ARTICLE_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
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
          <a class="size-tab size-tab--aux is-current" href="/articles/">Articles</a>
        </nav>
      </header>

      <section class="article-hero">
        <p class="eyebrow">Articles</p>
        <h1>{heading}</h1>
        <p class="subtitle">{subtitle}</p>
      </section>

      <section class="seo-stack" aria-label="Articles list">
        <section class="seo-card">
          <h2>Explore Math Puzzle Topics</h2>
          <p>These articles cover the educational, practical, and brain-training side of math crosswords and related number puzzles. Each piece is written to be useful, readable, and easy to scan.</p>
          <div class="article-grid">
            {cards}
          </div>
        </section>
      </section>

      <footer class="site-footer">
        <div class="site-footer__inner">
          <nav class="site-footer__nav" aria-label="Footer">
            <a href="/">Play online</a>
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


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
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
          <a class="size-tab size-tab--aux is-current" href="/articles/">Articles</a>
        </nav>
      </header>

      <article class="article-shell">
        <header class="article-hero">
          <p class="eyebrow">Article</p>
          <h1>{heading}</h1>
          <p class="subtitle">{subtitle}</p>
          {context_links}
        </header>

        <div class="article-body">
          {content}

          <section class="seo-card article-related">
            <h2>Related Links</h2>
            <div class="seo-link-grid">
              {related_links}
            </div>
          </section>

          <section class="seo-card article-related">
            <h2>Related Articles</h2>
            <div class="seo-link-grid">
              {related_articles}
            </div>
          </section>

          <section class="article-cta-grid" aria-label="Article actions">
            <a class="article-cta-card" href="/">
              <strong>Play online</strong>
              <span>Open the main puzzle hub and start solving right away.</span>
            </a>
            <a class="article-cta-card" href="/printable-math-crossword/">
              <strong>Print puzzle</strong>
              <span>See how printable pages work and use QR codes to continue online.</span>
            </a>
          </section>
        </div>
      </article>

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


def section(title: str, paragraphs: list[str]) -> str:
    rendered = "\n".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    return f"""
        <section class="seo-card article-section">
          <h2>{escape(title)}</h2>
          {rendered}
        </section>
    """.strip()


def related_links(items: list[tuple[str, str, str]]) -> str:
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
    return "\n".join(cards)


HOW_TO_LINK = ("How to Play", "/how-to-play-math-crossword/", "Read the rules, controls, and basic solving flow.")


def context_links_html(article: dict[str, object]) -> str:
    candidates = [item for item in article["related"] if item[1] != "/"]

    while len(candidates) < 2:
        candidates.append(HOW_TO_LINK)

    first = candidates[0]
    second = candidates[1]

    return (
        '<p class="article-context-links">'
        f'If you want to try this in practice, start with <a href="{escape(first[1])}">{escape(first[0])}</a>, '
        f'continue with <a href="{escape(second[1])}">{escape(second[0])}</a>, '
        f'or review <a href="{escape(HOW_TO_LINK[1])}">{escape(HOW_TO_LINK[0])}</a>.'
        "</p>"
    )


ARTICLES = [
    {
        "slug": "benefits-of-math-puzzles",
        "title": "Benefits of Math Puzzles for Focus, Logic, and Confidence",
        "description": "Learn how math puzzles support logic, focus, confidence, and everyday arithmetic practice for children and adults.",
        "subtitle": "Why number-based puzzles do more than fill time, and how they support focus, confidence, and practical reasoning.",
        "sections": [
            (
                "Math puzzles turn practice into a problem worth solving",
                [
                    "Many people know they should keep arithmetic and logic skills active, but few enjoy the feeling of sitting down with a page of repetitive drills. Math puzzles solve that problem by changing the emotional frame. Instead of repeating the same process ten times, you face a single interesting task with structure, feedback, and a satisfying end point. That change matters because motivation often determines whether practice happens at all.",
                    "A good puzzle gives players a reason to keep thinking. They are not just finding an answer because someone asked for one. They are looking for the next move, testing a possibility, and using new information to unlock the rest of the board. That is why formats such as math crosswords can feel lighter than worksheets even when they still involve arithmetic, comparison, and careful attention.",
                    "This puzzle-first approach also helps with consistency. People are much more likely to return to a short logic game or a compact number puzzle than to a formal drill session. Over time, that regular exposure can do more for fluency and confidence than occasional large study blocks that feel harder to begin.",
                ],
            ),
            (
                "They train logical thinking, not only calculation",
                [
                    "One of the biggest benefits of math puzzles is that they ask for reasoning as well as arithmetic. A player may know how to add, subtract, multiply, or divide, but the puzzle still requires them to decide where a number belongs and why. That shift from pure calculation to decision-making is a major part of what makes puzzles educational.",
                    "In a math crossword, a number is rarely meaningful on its own. It has to fit a row, a column, the available tray values, and the pattern created by the rest of the grid. This teaches a powerful habit: do not accept an answer until it fits the whole system. That kind of thinking shows up in real learning too, especially when students need to compare options, notice constraints, and avoid jumping at the first idea that seems to work.",
                    "Because of that, puzzles can strengthen the kind of calm, layered thinking that helps across subjects. They reward patience, cross-checking, and the willingness to revise a weak assumption without frustration.",
                ],
            ),
            (
                "Math puzzles support confidence through visible progress",
                [
                    "Confidence often grows when progress is visible. That is another reason puzzles are useful. A player can start with almost nothing, make one correct move, and immediately see the board become more readable. One line leads to another, and the puzzle slowly changes from confusing to structured.",
                    "This matters for learners who hesitate around math. Many people are less afraid of the arithmetic itself than of the feeling of being lost. Puzzles reduce that feeling because they provide constant signals. A tray count changes. A crossing becomes possible. A row narrows to one valid result. Each of those moments shows the player that they are moving forward.",
                    "That sense of earned progress builds resilience. When players solve puzzles regularly, they begin to trust that confusion is temporary and that a careful step will eventually open the board. That is a helpful mindset both inside and outside puzzle solving.",
                ],
            ),
            (
                "They work well for both short breaks and steady routines",
                [
                    "Another practical benefit is flexibility. A smaller board such as a 5x5 can fit into a short break, while larger boards can support a longer focused session. That range makes math puzzles easier to integrate into real life than many study tools that demand a fixed block of time.",
                    "For adults, a short logic session can work as a mental reset between tasks. For students, it can become part of a daily warm-up or after-school routine. Because the format feels contained, it is easier to say yes to one puzzle than to an open-ended study plan.",
                    "This is one reason many players end up using puzzles as maintenance practice. They do not replace all forms of learning, but they make it much easier to stay mentally active in a way that feels enjoyable and sustainable.",
                ],
            ),
            (
                "Why math crosswords are a strong example",
                [
                    "Math crosswords combine many of these benefits in one clean format. They feel familiar, because people understand the idea of a crossword grid, but they replace words with arithmetic and logic. The player must read the layout, work through the crossings, and use structure instead of guessing.",
                    "That makes them especially good for learners who like a clear visual framework. Smaller grids such as the ones on the main site can help new players get started quickly, while larger boards create richer challenges for people who want deeper reasoning. If you want to try the format directly, the main game page is the simplest place to start, and the size pages help you pick a board that matches your comfort level.",
                    "Printable versions add another layer of usefulness. A puzzle can move from screen to paper and back again through the printable section, which makes it easy to use at home, in class, or as part of a personal brain-training routine.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Open the main puzzle hub and try a live math crossword."),
            ("5x5 Math Crossword", "/5x5-math-crossword/", "Start with a compact beginner-friendly grid."),
            ("Printable Puzzles", "/printable-math-crossword/", "Learn how printable pages work for home or school use."),
        ],
    },
    {
        "slug": "math-crossword-for-kids",
        "title": "Math Crossword for Kids: A Friendly Way to Practice Numbers",
        "description": "See why math crosswords are a useful puzzle format for kids, especially on small boards and easy difficulty levels.",
        "subtitle": "How smaller grids, simple arithmetic, and clear visual feedback make math crosswords a good fit for younger learners.",
        "sections": [
            (
                "Why kids respond well to puzzle-based math practice",
                [
                    "Children often engage better when practice feels like discovery rather than correction. A math crossword works well for that because it presents numbers inside a puzzle pattern instead of as a page of isolated exercises. The child is not only solving sums. They are trying to complete a whole board, and each step feels like progress toward a visible goal.",
                    "This matters because motivation is fragile at early stages. If practice feels too evaluative, some children withdraw quickly. A puzzle softens that pressure. It invites experimentation, lets the child notice patterns, and creates a calmer atmosphere around number work.",
                    "When the difficulty is set correctly, the puzzle also gives regular success signals. A row becomes valid, a crossing suddenly makes sense, or one correct number helps solve another. Those moments are small, but they keep the child engaged and willing to continue.",
                ],
            ),
            (
                "Why 5x5 and Easy mode are strong starting points",
                [
                    "For children, the best entry point is usually a smaller board and a gentler difficulty level. A 5x5 puzzle keeps the visual field manageable. The child can see the whole board without feeling that there are too many moving parts, and that alone reduces frustration.",
                    "Easy mode helps for the same reason. More givens and simpler values mean the puzzle opens faster, which teaches the solving flow before the child has to manage too much uncertainty. They can learn how rows and columns interact without getting stuck at the very beginning.",
                    "That combination is why the 5x5 page is such a practical starting place for families and teachers. It gives children enough of the real puzzle structure to feel proud of solving it, but not so much that the task becomes intimidating.",
                ],
            ),
            (
                "What kids actually learn while solving",
                [
                    "A math crossword supports more than basic arithmetic. Children also practice scanning, comparing possibilities, and checking whether one answer still works when a second clue is considered. That is a valuable step toward real mathematical reasoning.",
                    "The format also supports number sense. Children begin to notice which values are plausible before they finish every calculation. They use operators, results, and tray counts as signals. Over time, this can strengthen intuition in a way that feels more natural than repeated drill alone.",
                    "Equally important, puzzles teach productive patience. A child learns that not knowing immediately is normal, that they can move to another line, and that one correct placement can unlock the next part of the board.",
                ],
            ),
            (
                "How parents and teachers can use the format well",
                [
                    "The best way to introduce a child to math crosswords is to stay collaborative at first. Instead of correcting mistakes too quickly, ask simple guiding questions. Which line already has the strongest clues? Which number from the tray seems limited? What happens if this value is placed here?",
                    "This kind of gentle prompting helps children explain their thinking instead of chasing only the answer. That is often where the real learning happens. Even when a child makes a wrong move, the puzzle gives a chance to talk about why it looked reasonable and what changed once the crossing was checked.",
                    "Printable pages are helpful here as well. A teacher can print a puzzle for class use, or a parent can sit beside a child and work slowly on paper. Later, the same puzzle can be revisited online through the printable section and QR flow.",
                ],
            ),
            (
                "Keeping math playful without losing structure",
                [
                    "A good educational activity balances two needs: it should feel enjoyable enough that a child wants to begin, and structured enough that something meaningful is being practiced. Math crosswords fit that balance well. They feel like a game, but the child still has to use arithmetic and logic carefully.",
                    "That is why they work so well as a bridge between free play and formal math. They do not replace instruction, but they can reinforce it in a way that feels much lighter. A short puzzle can become a daily routine, a quiet activity after school, or a shared weekend challenge.",
                    "If the goal is to make number practice feel less heavy and more inviting, a kid-friendly math crossword is a strong place to start. The home page, small size pages, and printable resources all support that kind of gradual introduction.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Start with a live puzzle and choose an easy board."),
            ("5x5 Math Crossword", "/5x5-math-crossword/", "Best starting size for younger solvers."),
            ("Printable Puzzles", "/printable-math-crossword/", "Use printable pages for classroom or home practice."),
        ],
    },
    {
        "slug": "printable-puzzles-for-schools",
        "title": "Printable Math Puzzles for Schools and Classroom Warm-Ups",
        "description": "Learn how printable math crossword puzzles can be used in schools for warm-ups, centers, homework, and low-pressure practice.",
        "subtitle": "Why printable number puzzles are useful in schools, and how teachers can use them without adding complexity to lesson planning.",
        "sections": [
            (
                "Why printable puzzle formats still matter in schools",
                [
                    "Even with strong digital tools available, printable materials still play an important role in classrooms. They are easy to distribute, easy to revisit, and easy to use in environments where device access varies from class to class. A printable math puzzle fits naturally into that reality because it provides structure without needing extra setup.",
                    "Teachers often need activities that can start quickly and end cleanly. A printable math crossword offers that. It can serve as a warm-up, a station activity, an early-finisher task, or a small review assignment without requiring a long explanation every time.",
                    "Because the puzzle is self-contained, it also reduces transition friction. Students can begin immediately, and the teacher can circulate, ask questions, and support different levels of confidence without changing the format itself.",
                ],
            ),
            (
                "Good classroom uses beyond simple filler time",
                [
                    "The strongest printable activities do more than fill a spare ten minutes. They create a real reason for students to think carefully and explain why an answer belongs. That is where math crosswords can be especially useful. Each number interacts with multiple equations, so students have to justify placements instead of relying on one isolated result.",
                    "That makes printable puzzles a good fit for centers, partner work, short review blocks, and low-pressure formative practice. They can also work well at the start of class because they calm the room while still activating arithmetic and reasoning skills.",
                    "For teachers who want variety, different sizes help. A 5x5 or 7x7 puzzle is often enough for a short opening task, while larger grids can be saved for enrichment, clubs, or optional extension work.",
                ],
            ),
            (
                "Why print plus online is a strong combination",
                [
                    "One of the most useful parts of a printable puzzle system is the ability to connect paper and screen without confusion. A student or teacher can print a puzzle, solve part of it offline, and then return to the exact same puzzle online if needed. That continuity makes the material more flexible.",
                    "The printable pages on the site support that with a QR code and a direct puzzle link. A sheet can be used in class, at home, or in a small group, and the same puzzle can still be reopened later on the site. That saves time because no one has to search for a matching digital version.",
                    "This also helps with differentiation. Some students may prefer paper first, while others may want the live tray and interactive checks online. The printable section keeps both routes connected.",
                ],
            ),
            (
                "What teachers should look for in school-friendly puzzles",
                [
                    "School-friendly printable puzzles need a few qualities: clear layout, readable structure, enough givens to create momentum, and a difficulty level that matches the group. If the puzzle is too open, students may lose confidence quickly. If it is too obvious, it becomes busy work.",
                    "This is why controlled size and difficulty matter. Easy and Medium usually work best for general classroom use, while Hard is more useful for enrichment groups or students who already enjoy puzzle-based reasoning.",
                    "The best approach is to match the task to the moment. Small easy puzzles work well as warm-ups. Medium puzzles fit stations or partner reasoning. Printable larger boards are better when there is more time and the goal is sustained thinking rather than quick review.",
                ],
            ),
            (
                "Building a puzzle routine teachers can actually sustain",
                [
                    "Teachers are more likely to keep using a resource when it stays simple. A printable puzzle system works best when it does not ask for extra management. Open one puzzle, print it, hand it out, and know that the same puzzle is available online if needed. That is a practical workflow, not an extra project.",
                    "When that process is easy, puzzles can become part of the weekly rhythm. A class might use one on Friday, after a test, during transition days, or as part of brain-training practice. The key is that the format stays familiar while the content changes.",
                    "For schools that want flexible number practice without turning every activity into a worksheet, printable math crosswords are a strong option. The home page, size pages, and printable resources give enough structure to keep the system useful over time.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Open the main puzzle hub and choose a live puzzle."),
            ("7x7 Math Crossword", "/7x7-math-crossword/", "A balanced size for regular classroom use."),
            ("Printable Puzzles", "/printable-math-crossword/", "See how printable and QR-linked puzzles work."),
        ],
    },
    {
        "slug": "brain-training-with-math-crosswords",
        "title": "Brain Training With Math Crosswords: A Practical Puzzle Habit",
        "description": "Discover how math crosswords support brain training through focus, working memory, pattern recognition, and calm problem solving.",
        "subtitle": "A realistic look at how number puzzles can support focus and mental sharpness without turning into a chore.",
        "sections": [
            (
                "Why puzzle-based brain training feels easier to sustain",
                [
                    "Many people want a brain-training habit, but few want another demanding routine to manage. That is why puzzle-based practice is so attractive. It is structured, finite, and immediately understandable. You are not committing to an abstract self-improvement project. You are solving one puzzle.",
                    "Math crosswords work especially well in this role because they combine several mental actions at once. You calculate, compare options, hold partial information in memory, and watch how each move changes the structure of the board. That keeps the activity active without making it feel chaotic.",
                    "A habit built around one or two short puzzles is often more durable than a plan that feels too formal. The puzzle gives you a natural beginning and end, and that makes it easier to return to the routine the next day.",
                ],
            ),
            (
                "Focus, working memory, and calm attention",
                [
                    "A good math crossword asks for focused attention. You read one line, hold a number in mind, check a crossing, compare tray values, and then decide whether the move really belongs. That process gently exercises working memory because several pieces of information stay active at once.",
                    "It also encourages calm attention rather than frantic speed. Strong puzzle solving usually comes from slowing down just enough to see the pattern. For many players, that makes the activity feel mentally refreshing. It is focused, but not noisy.",
                    "This is one reason puzzle time can work well as a reset between tasks. A short board helps the mind leave scattered work mode and move into a quieter, more deliberate rhythm.",
                ],
            ),
            (
                "Pattern recognition matters as much as arithmetic",
                [
                    "People often assume math puzzles are mainly about calculation, but much of the value comes from pattern recognition. The player starts to notice which kinds of rows tend to open first, how givens constrain later moves, and how the tray narrows possible placements even before every sum is finished.",
                    "That kind of noticing is useful far beyond puzzle solving. It supports the ability to scan for structure, compare relationships, and detect when a promising answer does not really fit the whole system.",
                    "Because the grid keeps giving feedback, players build this sense gradually. A pattern that was invisible at the start becomes obvious after repeated play, and that change is part of what makes the habit satisfying.",
                ],
            ),
            (
                "How to make brain training practical instead of vague",
                [
                    "The simplest way to use math crosswords for brain training is not to overthink the routine. Choose a size that fits the time you actually have. A 5x5 or 7x7 board may be enough for a short daily reset, while 9x9 or 11x11 can work when you want a longer session.",
                    "Difficulty matters too. Medium is often the best everyday mode because it keeps the solve interesting without draining energy. Hard is useful when you want a deeper challenge, but a sustainable habit usually depends more on consistency than on maximum difficulty.",
                    "If a screen break matters, the printable section makes it easy to move the same kind of activity onto paper while keeping the option to return online later.",
                ],
            ),
            (
                "A puzzle habit that stays enjoyable",
                [
                    "The real strength of math crosswords as brain training is that they remain enjoyable. You are still solving something with shape, rhythm, and payoff. That makes it easier to keep going than many forms of cognitive practice that feel more clinical.",
                    "For adults who want to stay mentally active, for students who need a focused routine, or for anyone who enjoys logical play, this kind of puzzle offers a practical middle ground. It is not a miracle solution, and it does not need to be. It is simply a smart, repeatable way to keep the mind working.",
                    "If that sounds useful, the main game page is a good place to start, the size pages help you choose a format, and printable options give you a paper version when you want a quieter session.",
                    "What makes this kind of brain training practical is that it stays specific. You are not trying to improve everything at once. You are giving attention, working memory, and logical comparison a small but repeatable workout inside a format that still feels enjoyable.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Start a simple daily puzzle routine online."),
            ("9x9 Math Crossword", "/9x9-math-crossword/", "Try a larger board for deeper focus and longer sessions."),
            ("Printable Puzzles", "/printable-math-crossword/", "Switch your brain-training routine from screen to paper."),
        ],
    },
    {
        "slug": "math-puzzles-for-classroom-use",
        "title": "Using Math Puzzles in the Classroom Without Overcomplicating Lessons",
        "description": "Practical ideas for using math puzzles in the classroom as warm-ups, partner activities, review tasks, and enrichment.",
        "subtitle": "Ways teachers can use number puzzles in real classrooms while keeping the format simple, useful, and easy to manage.",
        "sections": [
            (
                "Classroom puzzle use works best when the format stays simple",
                [
                    "Teachers often avoid good ideas when they feel expensive in time. A classroom puzzle only becomes useful if it can be introduced quickly, reused easily, and understood without a long explanation every time. That is why compact number puzzles work best when the structure stays familiar.",
                    "Math crosswords fit this need well. Once students understand the basic rules, the teacher can change the puzzle without changing the whole activity format. That makes the routine easier to sustain across weeks instead of turning it into a one-off novelty.",
                    "The strongest classroom tool is usually not the most elaborate one. It is the one students can begin with confidence and the teacher can prepare without adding stress to the rest of the lesson.",
                ],
            ),
            (
                "Where puzzles fit naturally in the school day",
                [
                    "There are several points in the day where math puzzles fit especially well. They work as warm-ups because they settle attention and activate arithmetic thinking. They work during stations because they provide a clear, self-contained task. They also work for early finishers, because they are structured enough to be meaningful but not so large that they derail the class flow.",
                    "Partner work is another strong use case. Two students can talk through one grid, compare reasoning, and explain why a number belongs. That conversation is valuable because it encourages mathematical language without requiring a full formal discussion routine.",
                    "When used well, puzzles become a flexible classroom tool rather than a special event. Different sizes and difficulty levels help teachers match them to the available time and the confidence level of the group.",
                ],
            ),
            (
                "How to choose the right size and difficulty for a class",
                [
                    "Selection matters more than teachers sometimes expect. A puzzle that is too large or too open can waste time because students get stuck before the logic becomes enjoyable. For many classrooms, 5x5 and 7x7 boards are the most practical because they give a complete puzzle experience without demanding a long block.",
                    "Difficulty matters just as much. Easy is often best for whole-group introduction, mixed-confidence groups, or short warm-ups. Medium works well once students know the pattern. Hard is usually better saved for enrichment or puzzle clubs rather than general class use.",
                    "The useful rule is simple: choose the easiest version that still asks students to think. The aim is productive reasoning, not confusion for its own sake.",
                ],
            ),
            (
                "Why online and printable formats work together",
                [
                    "A classroom tool becomes stronger when it can move between paper and screen without friction. Some students work more comfortably online, while others stay calmer with a printed page on the desk. A system that supports both lets the teacher adapt without changing the core activity.",
                    "The site’s printable pages make that easier because the same puzzle can exist in both forms. A teacher can print a puzzle for class, and later students can revisit the exact same board online through the printable link and QR path. That continuity reduces confusion and makes homework or follow-up practice easier to manage.",
                    "For teachers, this also means fewer materials to track. One puzzle can support several contexts instead of needing separate resources for paper and digital use.",
                ],
            ),
            (
                "Keeping puzzle use purposeful, not random",
                [
                    "The most effective classroom puzzle routines are tied to a purpose. Sometimes that purpose is number fluency. Sometimes it is calm entry to class. Sometimes it is collaborative reasoning. When the teacher knows why the puzzle is there, it becomes easier to choose the right size, difficulty, and follow-up questions.",
                    "That does not mean the activity has to become heavy. In fact, part of the value is that it feels lighter than formal practice. Students can still enjoy the puzzle while working on real mathematical habits such as checking, comparing, and justifying an answer.",
                    "If you want a classroom-friendly entry point, start small, stay consistent, and let the format do its work. The home page, size pages, and printable guide give enough structure to make that easy.",
                    "That simplicity is what makes puzzle use realistic for real schools. Teachers can keep the routine light, students can recognize the structure quickly, and the thinking stays meaningful without demanding a complicated setup.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Try a live puzzle to see the format students would use."),
            ("7x7 Math Crossword", "/7x7-math-crossword/", "A practical classroom size with more logic but manageable scope."),
            ("Printable Puzzles", "/printable-math-crossword/", "Use printable versions for warm-ups and station work."),
        ],
    },
    {
        "slug": "choosing-the-right-math-crossword-size",
        "title": "How to Choose the Right Math Crossword Size for Your Goal",
        "description": "A simple guide to choosing between 5x5, 7x7, 9x9, and 11x11 math crossword puzzles based on time and difficulty.",
        "subtitle": "A practical guide to picking the right grid size for quick sessions, steady practice, or deeper long-form solving.",
        "sections": [
            (
                "Size changes the feel of the puzzle more than many players expect",
                [
                    "New players often think difficulty is the only setting that matters, but size changes the whole rhythm of the solve. A smaller board makes information easier to hold at once, while a larger board creates longer chains, more crossings, and more delayed consequences.",
                    "That means choosing the right size is really about choosing the kind of session you want. Are you warming up for five minutes, practicing steadily, or settling in for a deeper puzzle? The answer should shape the board you choose before difficulty even enters the picture.",
                    "Once players understand that, it becomes much easier to enjoy the library. Instead of forcing one size to do everything, they can match the board to the moment.",
                ],
            ),
            (
                "When 5x5 and 7x7 make the most sense",
                [
                    "A 5x5 puzzle is the easiest place to begin. It keeps the board compact, gives faster feedback, and helps new players learn how crossings work without too much visual load. It is also perfect when time is short and you want one clean solve.",
                    "A 7x7 puzzle is often the next step because it adds more interactions without becoming too demanding. Many players settle into 7x7 as their regular size because it feels substantial but still manageable in a short session.",
                    "If the goal is to build comfort, consistency, or a daily routine, these two sizes are usually the best choice. The dedicated size pages make it easy to compare them directly.",
                ],
            ),
            (
                "When larger boards become more rewarding",
                [
                    "A 9x9 board changes the experience. It asks for more patience, more tray awareness, and more willingness to move between regions instead of trying to finish one line immediately. That added complexity can be very rewarding once the basic format feels familiar.",
                    "An 11x11 board takes that even further. It is the strongest choice for players who enjoy long-form logic and do not mind sitting with uncertainty before the board starts to open. The larger the grid, the more important rhythm and structure become.",
                    "This is why larger sizes are often better once Medium already feels comfortable. They are excellent, but they are more enjoyable when the player is ready for the extra scale.",
                ],
            ),
            (
                "Match size to purpose, not only skill",
                [
                    "It is tempting to think bigger always means better, but that is not really how puzzle enjoyment works. Some days a quick 5x5 is the perfect choice, even for experienced players. On other days, a 9x9 or 11x11 board provides the kind of focus that a smaller grid cannot.",
                    "The better question is not what size you should always play. It is what size matches the purpose of this session. Quick reset, regular training, or longer challenge all call for different board choices.",
                    "Difficulty can then fine-tune the experience. Easy makes the entry smoother, Medium offers the most balanced everyday solve, and Hard increases the deduction load regardless of board size.",
                ],
            ),
            (
                "A simple way to decide before you start",
                [
                    "If you want the shortest path to solving, choose 5x5. If you want a regular practice board, choose 7x7. If you want more involved reasoning, choose 9x9. If you want the biggest challenge in the library, choose 11x11.",
                    "That simple rule is enough for most players. You can always adjust after a few sessions, but it gives a strong starting point without overthinking the choice.",
                    "The easiest way to explore is to open the home page, visit one size page at a time, and keep the printable option in mind if you ever want the same kind of puzzle away from the screen.",
                    "Once players stop treating size as a ranking system and start treating it as a session choice, the library becomes much easier to use well. The right board is the one that fits your time, attention, and goal today.",
                    "That is also why category pages are useful. They let you treat each size as its own environment instead of as a small variation of the same puzzle. A few sessions on each board usually make the best fit obvious.",
                    "A player who understands this tends to enjoy the site more. Instead of wondering what they should be able to solve, they can simply choose the board that fits the kind of thinking they want right now.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Open the main hub and compare sizes directly."),
            ("11x11 Math Crossword", "/11x11-math-crossword/", "See the biggest format in the library."),
            ("Printable Puzzles", "/printable-math-crossword/", "Take the same size decision into a print-friendly format."),
        ],
    },
    {
        "slug": "easy-math-crossword-routines-for-daily-practice",
        "title": "Easy Math Crossword Routines for Daily Practice",
        "description": "Build a light daily math practice habit with easy math crosswords, short sessions, and realistic puzzle routines.",
        "subtitle": "How to turn short easy puzzles into a practical daily habit for arithmetic confidence and calm brain training.",
        "sections": [
            (
                "Why easy routines work better than ambitious plans",
                [
                    "A daily practice habit usually succeeds when it stays small enough to begin without resistance. That is why easy math crossword routines can work so well. Instead of aiming for a long session, you solve one approachable puzzle and let consistency do the work.",
                    "This matters because the hardest part of many routines is simply getting started. A short puzzle removes that barrier. The task feels finite, the reward is immediate, and the player can stop after one board without guilt.",
                    "Over time, that low-friction beginning can create more real practice than a larger plan that sounds impressive but rarely happens.",
                ],
            ),
            (
                "Why Easy mode supports daily confidence",
                [
                    "Easy mode is useful for daily practice because it reduces the chance of hitting a wall too early. More givens and simpler values mean the puzzle starts moving sooner, which makes the routine feel encouraging rather than heavy.",
                    "That is important for both children and adults. The goal of a daily puzzle habit is not to prove maximum skill every morning. It is to keep number thinking active and positive enough that the habit lasts.",
                    "Once the routine feels stable, players can still mix in Medium boards. But Easy often provides the best base because it keeps the cost of showing up low.",
                ],
            ),
            (
                "How to build a realistic five-minute puzzle habit",
                [
                    "The simplest routine is to attach one puzzle to an existing anchor in the day. That might be after breakfast, after school, before opening email, or at the end of a study block. The anchor matters more than the exact time.",
                    "Choose a small board such as 5x5 or 7x7, set the expectation to one puzzle, and stop there unless you want more. This protects the routine from becoming too large. A habit survives when it is easy to repeat, not when it demands perfect motivation.",
                    "If the screen is not ideal at that moment, printable pages can support the same routine on paper without breaking continuity.",
                ],
            ),
            (
                "What daily puzzle practice actually improves",
                [
                    "A short daily puzzle can strengthen arithmetic fluency, attention to detail, and comfort with logical elimination. It can also reduce math hesitation by normalizing the process of testing, checking, and correcting small mistakes.",
                    "Just as important, it helps build a steadier relationship with problem solving. The player learns that they do not need to rush. They can read one clue, make one sound move, and let the puzzle develop.",
                    "That kind of quiet confidence is often more valuable than a burst of difficult practice followed by a long break.",
                ],
            ),
            (
                "Keeping the routine fresh without losing structure",
                [
                    "A routine stays stronger when it has some variety inside a stable shape. That is why switching between sizes or moving between Easy and Medium can help once the habit is established. The structure stays familiar, but the board changes enough to remain interesting.",
                    "The best version is still the one you enjoy enough to keep. If 5x5 Easy becomes your dependable daily reset, that is already a strong outcome. If you want a little more depth on weekends, the larger size pages are there when you need them.",
                    "The main thing is not to overcomplicate what is working. One manageable puzzle a day is already a meaningful practice habit.",
                    "That is why daily practice works best when it feels almost ordinary. You open a puzzle, make a few thoughtful moves, finish if you can, and return tomorrow. The strength of the routine comes from repetition, not from intensity.",
                    "For some players, keeping the routine visible helps too. A printed puzzle on the table or a bookmarked size page can act as a gentle cue that removes one more barrier to starting.",
                    "That is usually enough. A simple routine that survives busy weeks is more valuable than an ambitious plan that only works when motivation is unusually high.",
                    "When the routine is built this way, it becomes easier to trust small progress. One easy puzzle may not feel dramatic, but a month of steady short sessions adds up to real comfort and fluency.",
                    "That quiet accumulation is exactly what makes daily puzzle practice worthwhile. It asks for very little in one sitting and still pays off over time.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Start a short daily puzzle routine from the main hub."),
            ("5x5 Math Crossword", "/5x5-math-crossword/", "Use the smallest size for quick and repeatable sessions."),
            ("Printable Puzzles", "/printable-math-crossword/", "Move the same daily routine onto paper when needed."),
        ],
    },
    {
        "slug": "screen-free-math-practice-with-printables",
        "title": "Screen-Free Math Practice With Printable Puzzles",
        "description": "Use printable math crossword puzzles for screen-free practice at home, in class, or during quiet learning time.",
        "subtitle": "Why printable number puzzles are useful when you want calmer, screen-free practice without losing structure.",
        "sections": [
            (
                "Why screen-free practice still matters",
                [
                    "Digital tools are convenient, but there are many moments when paper is simply the better environment. A child may focus more clearly without a device. A classroom may need a low-tech option. A parent may want a quiet activity that does not add more screen time to the day.",
                    "Printable math puzzles work well in those moments because they preserve the structure of the puzzle while changing the medium. The same reasoning, arithmetic, and pattern recognition still apply, but the pace often feels calmer on paper.",
                    "That makes printable puzzle use more than a backup plan. For many people, it is a preferred mode for concentration.",
                ],
            ),
            (
                "What paper changes in a positive way",
                [
                    "On paper, players often scan more slowly and think more deliberately. They may jot possibilities, look across the board more carefully, and take fewer impulsive actions. That slower pace can be especially helpful for learners who become overwhelmed by too much on-screen interaction.",
                    "Paper also makes shared solving easier in some settings. Two students, a parent and child, or a small group can point to the same board, talk through options, and work collaboratively without passing a device around.",
                    "Because the layout stays fixed in front of them, many solvers feel that paper supports steadier attention, especially during longer puzzles.",
                ],
            ),
            (
                "When printable puzzles are most useful",
                [
                    "Printable math crosswords fit naturally into home practice, classroom stations, tutoring, travel, and quiet independent work. They are especially useful when internet access is inconsistent or when a screen would distract from the goal.",
                    "Smaller sizes are perfect for short screen-free practice. Larger boards can support a more immersive paper session when the player wants to settle in for deeper reasoning.",
                    "The printable section on the site is built exactly for this kind of use. It keeps the page clean, gives you a direct puzzle link, and adds a QR code so you can still reconnect to the online version later.",
                ],
            ),
            (
                "How print and online can support each other",
                [
                    "Screen-free does not have to mean disconnected. One of the strongest features of a printable system is that paper and online can work together instead of competing. A player can begin on paper, then switch online later for the same puzzle if they want live tray support or an easy way to continue.",
                    "That connection is especially helpful for families and teachers. A puzzle can be printed in advance, taken anywhere, and still reopened later without confusion. The QR code and direct link solve a common problem: losing track of the exact puzzle you used.",
                    "In other words, printable practice keeps the calm benefits of paper while still preserving digital convenience when it actually helps.",
                ],
            ),
            (
                "Building a useful screen-free puzzle habit",
                [
                    "If you want more screen-free math practice, the easiest routine is to print a few small puzzles and keep them nearby. One puzzle after school, one during a quiet break, or one at the kitchen table can be enough to build a light habit.",
                    "Choose board size based on time and confidence. Start small if the goal is regular use, then expand into larger boards when the routine feels natural. Keep the printable guide handy so the process stays simple.",
                    "That balance of convenience, structure, and calm is what makes printable math crosswords such a useful tool. They meet people where they are instead of forcing every kind of practice to happen in exactly one format.",
                    "For families, teachers, and independent learners, that flexibility matters a lot. It means math practice can stay available even when the best environment is a table, a clipboard, or a backpack instead of a screen.",
                    "It also helps reduce the all-or-nothing feeling that sometimes surrounds study time. If a learner is not in the mood for a device, practice does not have to disappear. The same kind of puzzle can still happen on paper.",
                    "That practical flexibility is what makes printables more than a convenience feature. They become a reliable second path for keeping puzzle-based learning available in more real-life situations.",
                    "In practice, that often means more use, not less. A format that works in kitchens, classrooms, and quiet corners of the day has a better chance of becoming part of a real routine.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Return to the main puzzle hub for live play."),
            ("5x5 Math Crossword", "/5x5-math-crossword/", "Pick a quick size for short screen-free sessions."),
            ("Printable Puzzles", "/printable-math-crossword/", "Use the printable hub to move between paper and screen."),
        ],
    },
    {
        "slug": "how-math-crosswords-build-number-sense",
        "title": "How Math Crosswords Build Number Sense Through Puzzle Solving",
        "description": "See how math crosswords help build number sense by combining arithmetic, estimation, pattern recognition, and constraint-based thinking.",
        "subtitle": "Why number sense grows naturally when arithmetic is placed inside a puzzle with crossings, constraints, and visible structure.",
        "sections": [
            (
                "Number sense is more than getting an answer quickly",
                [
                    "Number sense includes fluency, estimation, comparison, and the ability to feel whether a value is reasonable before every step is fully written out. It is not just about reaching the answer. It is about understanding how numbers behave.",
                    "That is why some learners who can compute still struggle in flexible problem-solving situations. They know the procedure, but they do not always have a strong intuitive feel for what fits, what seems too large, or what relationships are likely to matter.",
                    "Math crosswords help because they place arithmetic inside a visible system of constraints. The player does not simply compute one line and move on. They compare possibilities and notice which values make sense across the board.",
                ],
            ),
            (
                "Crossings force players to think relationally",
                [
                    "In a regular exercise, a single equation stands alone. In a crossword-style puzzle, one value belongs to more than one line. That crossing changes the nature of the task. A number has to be right in context, not only correct in isolation.",
                    "This pushes players toward relational thinking. They begin to ask whether a number fits the surrounding structure, whether it leaves realistic options for the crossing line, and whether the tray even supports that choice. These are number-sense questions as much as they are puzzle questions.",
                    "Over time, this can improve how players read arithmetic itself. They stop seeing it as a series of separate mini-tasks and begin seeing it as a connected system of constraints and possibilities.",
                ],
            ),
            (
                "Tray awareness supports estimation and plausibility",
                [
                    "The tray is especially useful for building number sense because it keeps the set of available values visible. A player quickly learns that even a mathematically possible answer may be impossible within this puzzle because the necessary value is no longer available.",
                    "That awareness encourages plausibility checking. Before placing a number, the player starts to ask whether it is likely, whether it matches the range of the line, and whether using it here would make the rest of the board harder to resolve.",
                    "These habits matter outside puzzles too. They strengthen the sense that numbers are not random symbols but resources inside a structured situation.",
                ],
            ),
            (
                "Smaller boards are a strong place to grow intuition",
                [
                    "For players who want to build number sense, smaller boards can be especially useful. A 5x5 or 7x7 puzzle lets the whole system stay visible at once, which makes relationships easier to notice. The player can read across the board and see how one placement changes the whole picture.",
                    "Easy and Medium modes help at first because they create enough traction for patterns to become visible. Once the player is comfortable, larger boards deepen the same skill by requiring more patience and broader scanning.",
                    "This gradual path is one reason the size pages are useful. They let players adjust complexity without abandoning the core structure that is helping the intuition develop.",
                ],
            ),
            (
                "Why puzzle-based number sense often feels more natural",
                [
                    "People often build better intuition when they are using numbers for a purpose rather than memorizing isolated facts. A puzzle gives them that purpose. Each number matters because it helps complete a visible structure, not because it appears on a disconnected list.",
                    "That purposeful context makes noticing easier. Players begin to anticipate patterns, rule out weak options, and sense when a line is heading in the right direction. Those are all signs of stronger number sense.",
                    "For anyone who wants arithmetic practice to feel more meaningful, math crosswords are a strong tool. The main game page gives an easy starting point, and printable resources make it possible to continue the same kind of practice away from the screen.",
                    "The more regularly a player sees numbers in this kind of connected setting, the more natural estimation and plausibility become. That is why puzzle-based number sense often feels less forced and more durable than isolated drill alone.",
                    "Seen this way, the puzzle becomes a bridge between raw arithmetic and flexible mathematical thinking. It gives numbers a context, and that context is often what helps intuition deepen.",
                    "For learners who need arithmetic to feel more connected and less mechanical, that bridge is a big advantage. It makes practice feel like reasoning rather than repetition alone.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "Try a live puzzle and watch number sense develop through play."),
            ("7x7 Math Crossword", "/7x7-math-crossword/", "A balanced board for seeing number relationships clearly."),
            ("Printable Puzzles", "/printable-math-crossword/", "Use paper versions for slower, more deliberate scanning."),
        ],
    },
    {
        "slug": "why-teachers-use-number-puzzles",
        "title": "Why Teachers Use Number Puzzles to Support Math Learning",
        "description": "Explore why teachers use number puzzles to support engagement, logic, classroom routines, and low-pressure math practice.",
        "subtitle": "The practical reasons teachers reach for number puzzles when they want focus, engagement, and meaningful low-pressure practice.",
        "sections": [
            (
                "Teachers need practice formats students will actually enter",
                [
                    "A classroom resource is only useful if students will begin it with reasonable confidence. That is one reason teachers often use number puzzles. They create a task with a clear goal, a visible finish, and a format that feels more inviting than a page of repeated exercises.",
                    "This does not mean the learning disappears. In fact, students often work more carefully because they want to complete the whole board. The puzzle gives them a reason to persist through small moments of uncertainty.",
                    "Teachers value that combination of engagement and structure. It is easier to support meaningful practice when the activity does not feel like punishment.",
                ],
            ),
            (
                "Number puzzles encourage explanation, not only answers",
                [
                    "When a student places a number in a puzzle, the teacher can ask an important question: why there? That question matters because it moves the conversation away from answer-only thinking and toward reasoning.",
                    "In a math crossword, students often need to refer to crossings, givens, or tray limits to justify a choice. That naturally creates mathematical talk. Students explain, compare, reconsider, and sometimes revise. Those moments are educationally rich even when the puzzle itself looks simple.",
                    "This is one reason number puzzles fit well in partner tasks and small-group support. The format encourages visible thinking without needing a large formal discussion routine every time.",
                ],
            ),
            (
                "They fit multiple classroom roles",
                [
                    "Teachers also appreciate tools that are flexible. Number puzzles can function as warm-ups, center tasks, enrichment work, early-finisher activities, or homework extensions. The same basic format can serve different purposes depending on the size and difficulty chosen.",
                    "That flexibility reduces planning overhead. Once students know the rules, the teacher can keep reusing the structure while varying the content and challenge. This is much easier to sustain than introducing a brand-new activity every week.",
                    "The size pages on the site support that kind of use because they make it simple to choose between quick boards and larger challenges.",
                ],
            ),
            (
                "Low-pressure practice often produces better effort",
                [
                    "Some of the best classroom learning happens when the pressure drops slightly but the thinking stays real. Number puzzles can create that environment. Students still need to reason, calculate, and check their work, but the task feels more playful and less evaluative.",
                    "This matters especially for learners who tense up around math. A puzzle does not erase that feeling entirely, but it often softens the entry point enough for the student to stay involved. Once they get one or two values placed, the board starts giving information back, and confidence grows.",
                    "Teachers often notice that students will work longer on a puzzle than on a comparable worksheet because the puzzle feels like a problem to solve rather than a set of tasks to finish.",
                ],
            ),
            (
                "Why this works especially well with print and digital together",
                [
                    "The strongest systems give teachers options. Some classes will benefit from paper. Others will like the live online tray and instant interaction. When both formats point to the same puzzle, the teacher can adapt without changing the learning objective.",
                    "That is one reason printable and online math crosswords work well together. A puzzle can begin on paper, continue online, and stay recognizable throughout. That saves time and helps students focus on the reasoning instead of on a changing interface.",
                    "For teachers who want a simple way to add structure, logic, and engagement to math practice, number puzzles remain one of the most practical tools available.",
                    "They respect classroom limits while still giving students a meaningful task. That combination is rare, and it explains why puzzle formats remain such a reliable choice for teachers who want practice that students will actually enter.",
                    "When a resource can support engagement, reasoning, and simple classroom management at the same time, it earns its place. That is the real reason number puzzles stay useful year after year.",
                    "Teachers do not need every activity to do everything. They need dependable formats that invite students in and support good thinking, and number puzzles often meet that need unusually well.",
                    "That dependable quality is often what keeps a resource in rotation. When a puzzle format works across groups, moods, and classroom moments, it becomes part of the teaching toolkit instead of a temporary experiment.",
                ],
            ),
        ],
        "related": [
            ("Home", "/", "See the live version of the puzzle format teachers can use."),
            ("7x7 Math Crossword", "/7x7-math-crossword/", "A useful classroom size for balanced problem solving."),
            ("Printable Puzzles", "/printable-math-crossword/", "Use printable versions for paper-based classroom routines."),
        ],
    },
]


def article_card(article: dict[str, object]) -> str:
    return f"""
            <a class="seo-link-card article-card" href="/articles/{escape(article['slug'])}/">
              <strong>{escape(article['title'])}</strong>
              <span>{escape(article['description'])}</span>
            </a>
    """.strip()


def related_article_cards(slug: str, limit: int = 2) -> str:
    cards = []

    for article in ARTICLES:
        if article["slug"] == slug:
            continue

        cards.append(
            f"""
            <a class="seo-link-card article-card" href="/articles/{escape(article['slug'])}/">
              <strong>{escape(article['title'])}</strong>
              <span>{escape(article['description'])}</span>
            </a>
            """.strip()
        )

        if len(cards) >= limit:
            break

    return "\n".join(cards)


def write_page(path: str, content: str) -> None:
    destination = WORKSPACE / path.lstrip("/")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)


def render_article(article: dict[str, object]) -> str:
    content = "\n".join(section(title, paragraphs) for title, paragraphs in article["sections"])
    return ARTICLE_TEMPLATE.format(
        title=escape(article["title"]),
        description=escape(article["description"]),
        ga_snippet=GA_SNIPPET,
        canonical=escape(f"https://example.com/articles/{article['slug']}/"),
        heading=escape(article["title"]),
        subtitle=escape(article["subtitle"]),
        context_links=context_links_html(article),
        content=content,
        related_links=related_links(article["related"] + [HOW_TO_LINK]),
        related_articles=related_article_cards(article["slug"]),
    )


def render_index() -> str:
    cards = "\n".join(article_card(article) for article in ARTICLES)
    return ARTICLE_INDEX_TEMPLATE.format(
        title=escape("Math Puzzle Articles – Guides, Ideas, and Printable Tips"),
        description=escape("Browse articles about math puzzles, printable crosswords, classroom use, brain training, and kid-friendly number games."),
        ga_snippet=GA_SNIPPET,
        canonical=escape("https://example.com/articles/"),
        heading=escape("Math Puzzle Articles"),
        subtitle=escape("Short, useful reads about math crosswords, classroom ideas, printable practice, brain training, and number-based learning."),
        cards=cards,
    )


def main() -> None:
    write_page("/articles/index.html", render_index())

    for article in ARTICLES:
        write_page(f"/articles/{article['slug']}/index.html", render_article(article))


if __name__ == "__main__":
    main()
