# Fortune Cookie

something small, just for you.

A tiny static site: tap the bag, a cookie pops out, crack it open for a fortune. Eight cookies a day.

## Files

- `index.html` – the whole page (styles, animation, sounds, sharing)
- `fortunes.js` – the fortunes and their lucky numbers, plus how many cookies a day (`PER_DAY`)
- `img/` – the bag and cookie cut-outs, link-preview image and icons; `make-bag.py` / `make-halves.py` rebuild the cut-outs

## Publishing on GitHub Pages

1. Merge into `main`.
2. In the repo on GitHub: **Settings → Pages → Build and deployment**, set **Source** to *Deploy from a branch*, branch `main`, folder `/ (root)`, and save.
3. After a minute it's live at https://camilledaisy.github.io/fortunecookie/

The link-preview tags in `index.html` point at that address; if it ends up somewhere else, update the `og:url` and `og:image` lines.
