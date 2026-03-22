# example.com

Static Math Crossword site prepared for Cloudflare deployment from GitHub.

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

Build the deployable static asset directory:

```bash
python3 scripts/prepare_public_dir.py
```

## Cloudflare Workers Builds

- Build command: `python3 scripts/prepare_public_dir.py`
- Deploy command: `npx wrangler deploy`
- Path: `/`
- Custom domain: `example.com`

This repository targets the current GitHub-connected Workers flow. The build step prepares a `public/` directory, and Wrangler deploys it as static assets.

```bash
python3 scripts/prepare_public_dir.py
npx wrangler deploy
```
