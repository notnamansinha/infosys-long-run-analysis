# Public release checklist

Use this checklist before adding any real data, chart, report, or derived result.

## Rights

- [ ] I recorded a release basis: open licence, public-domain status, written permission, or reviewed limited factual extraction from a public filing.
- [ ] If relying on a factual extraction, it is narrow and does not copy expressive text, imagery, layout, or a substantial third-party compilation.
- [ ] If relying on permission or a licence, it explicitly covers the exact public result, including aggregates, charts, summaries, or derivatives.
- [ ] The source, licence or permission, retrieval date, and transformations are recorded.
- [ ] I am not relying on a small row count, a renamed source, missing attribution, or de-identification as a substitute for permission.

## Privacy

- [ ] Direct identifiers, credentials, private correspondence, and free text are absent.
- [ ] Quasi-identifiers and rare categories have been reviewed for re-identification risk.
- [ ] Categories are standardized through a documented mapping where needed.
- [ ] The release contains only the minimum fields and precision required.

## Repository hygiene

- [ ] The file is reproducible from a public or authorized input.
- [ ] No private source file or source-derived result remains in the staged diff.
- [ ] `python public_release_check.py` passes.
- [ ] `git diff --cached --check` passes after reviewing each staged file.

The checker is a technical backstop, not a legal opinion or a guarantee of anonymity. If the rights scope is unclear, keep the material local and publish the schema, method, and synthetic fixture instead.
