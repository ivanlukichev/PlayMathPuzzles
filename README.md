# PlayMathPuzzles

PlayMathPuzzles is an interactive collection of browser-based math puzzles designed to train logic, thinking, and problem-solving skills.

## About

- Lightweight math crossword gameplay in the browser
- Puzzle dataset and static pages generated ahead of deployment
- Prepared for Cloudflare GitHub-connected Workers deployment

## Project structure

- `index.html` and section folders contain the published static pages
- `src/` contains the browser-side game logic
- `data/puzzles.json` contains the puzzle dataset
- `scripts/` regenerates SEO pages, articles, puzzle pages, and deploy assets

## Local maintenance

Regenerate site content with Python 3:

```bash
python3 scripts/generate_articles.py
python3 scripts/generate_seo_pages.py
python3 scripts/generate_static_pages.py
python3 scripts/generate_site_files.py
```

Prepare the deployable static asset directory:

```bash
python3 scripts/prepare_public_dir.py
```

## Cloudflare

- Build command: `python3 scripts/prepare_public_dir.py`
- Deploy command: `npx wrangler deploy`
- Path: `/`
- Current target domain: `example.com`

This repository targets the current GitHub-connected Workers flow. The build step prepares a `public/` directory, and Wrangler deploys it as static assets.

## Author

Ivan Lukichev  
https://lukichev.biz
