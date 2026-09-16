# Contributing

Keep contributions narrow, inspectable, and reproducible.

Before opening a pull request:

1. Run `python public_release_check.py`.
2. Run `git diff --check`.
3. Record the source and licence for every new dataset or image.
4. Confirm that no private path, credential, commercial export, or restricted derivative is staged.

Code contributions should include a short example or a clear explanation of the expected input schema. Data contributions require explicit redistribution permission. A public URL alone does not prove that copying or republishing the contents is permitted.

Use synthetic fixtures when a real dataset cannot be redistributed. Keep large or access-controlled inputs outside the repository and document how an authorized user can supply them locally.

For a permitted CSV contribution, use `prepare_public_subset.py` with an explicit `--keep` list and the `--rights-confirmed` acknowledgement, then complete `RELEASE_CHECKLIST.md`. The tool is deliberately conservative and does not replace a rights or privacy review.
