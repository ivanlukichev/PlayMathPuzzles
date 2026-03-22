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
- Build command: leave empty
- Build output directory: `.`
- Production branch: `main`
- Custom domain: `example.com`

If you use a deploy command, use Pages deploy rather than Workers deploy:

```bash
npx wrangler pages deploy .
```

or:

```bash
npm run deploy
```

Do not use `npx wrangler deploy` for this repository. That command targets Workers deployments and does not use `pages_build_output_dir`.
