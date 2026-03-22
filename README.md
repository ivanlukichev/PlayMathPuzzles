# example.com

Static Math Crossword site prepared for GitHub and Cloudflare Pages.

## Project structure

- `index.html` and section folders contain the published static pages.
- `src/` contains the browser-side game logic.
- `data/puzzles.json` contains the puzzle dataset.
- `scripts/` regenerates SEO pages, articles, puzzle pages, and site files.

## Local maintenance

Regenerate content with Python 3:

```bash
python3 scripts/generate_articles.py
python3 scripts/generate_seo_pages.py
python3 scripts/generate_static_pages.py
python3 scripts/generate_site_files.py
```

## Cloudflare Pages

- Framework preset: `None`
- Build command: none
- Build output directory: `.`
- Production branch: `main`
- Custom domain: `example.com`
