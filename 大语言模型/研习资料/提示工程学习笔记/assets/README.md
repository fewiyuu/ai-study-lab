# study-page-v2 Runtime

Reusable runtime assets for learning-kit hosted or multi-page courses.

## Files

- `study-page.css`: shared study-page shell and components.
- `index-page.css`: shared course index / map styling.
- `study-page.js`: local interactions for progress, nav, copy, code folding,
  KaTeX, Prism, shape/data tracing, input-output demos, terminal labs,
  practice checks, and Markdown export.
- `vendor/`: local KaTeX and Prism assets. Do not replace these with CDN links
  in learner-facing pages.

## Expected Page Links

From a unit folder one level below the course root, use:

```html
<link rel="stylesheet" href="../assets/vendor/katex/katex.min.css">
<link rel="stylesheet" href="../assets/vendor/prism/prism-tomorrow.min.css">
<link rel="stylesheet" href="../assets/vendor/prism/prism-line-numbers.min.css">
<link rel="stylesheet" href="../assets/study-page.css">
...
<script src="../assets/vendor/katex/katex.min.js"></script>
<script src="../assets/vendor/katex/auto-render.min.js"></script>
<script src="../assets/vendor/prism/prism-core.min.js"></script>
<script src="../assets/vendor/prism/prism-clike.min.js"></script>
<script src="../assets/vendor/prism/prism-python.min.js"></script>
<script src="../assets/vendor/prism/prism-bash.min.js"></script>
<script src="../assets/vendor/prism/prism-json.min.js"></script>
<script src="../assets/vendor/prism/prism-line-numbers.min.js"></script>
<script src="../assets/study-page.js"></script>
```

Adjust the prefix if the page is deeper than one folder.

## DOM Contracts

Use `assets/templates/snippets/study-page-v2-components.md` instead of
inventing new component markup.
