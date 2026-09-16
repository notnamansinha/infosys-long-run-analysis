# Public data policy

This project separates method from source material.

## Allowed in the public repository

- Original code and documentation.
- Synthetic examples created for this repository.
- Public data whose publisher clearly permits the intended reuse.
- Limited factual extractions from public regulatory or issuer filings when the release basis has been documented and no expressive text, images, or source layout is copied.
- Aggregates or transformations whose licence explicitly permits redistribution.
- Links and citations that let readers obtain source material themselves.

## Keep out of the public repository

- Files obtained through a personal, institutional, or subscription login unless redistribution is expressly permitted.
- Screenshots of commercial software interfaces.
- Raw email, correspondence, or attachments containing private information.
- Derived tables, charts, or reports that reproduce restricted source values.
- Credentials, access tokens, account identifiers, and local machine paths.

## Aggregation is not an automatic exception

A report, summary, ratio, chart, or de-identified extract can still be a redistribution or derivative of a restricted source. Volume alone is not the test. Publish a source-derived result only when the governing terms or written permission expressly allow public redistribution of that result.

Do not rely on removing a provider name, changing labels, standardizing categories, or avoiding attribution to make restricted material public. If the permission scope is unclear, keep the source and every source-derived result local and publish the method plus the synthetic fixture instead.

## Privacy and categorical data

Before a permitted public release:

- Remove direct identifiers such as names, email addresses, phone numbers, addresses, account IDs, government IDs, credentials, and free-text correspondence.
- Treat combinations of time, geography, role, employer, category, and other fields as possible quasi-identifiers. Reduce precision or group rare values where appropriate.
- Standardize categorical text with a documented mapping, but keep the original mapping file private unless its publication is authorized.
- Publish only the minimum fields and granularity needed for the stated research question.

Privacy transformation does not create a redistribution licence. Rights review and privacy review are separate release gates.

## Public release gate

For every source-derived public file, record all of the following before staging it:

```text
rights_status: open licence / public-domain / written permission / reviewed factual extraction / not cleared
release_basis: licence, public-domain status, permission, or documented review of a limited factual extraction
publisher:
title:
retrieved:
source_url:
licence_or_permission:
transformations:
pii_review: reviewer and date
reproducible_input: public URL or authorized local-only input
```

If `rights_status` is `reviewed factual extraction`, keep the extract narrow, cite the public filing, omit expressive content and document any accounting or presentation caveats. That category is not a shortcut for copying a database, chart, report, or substantial source compilation. If no defensible release basis is recorded, do not commit the result. Run `python public_release_check.py` and review the staged diff file by file as a final technical check; neither step is legal clearance.

Removing a source file from the latest commit does not remove it from Git history. If a restricted file is ever pushed, stop distributing it, preserve a private copy if needed, and follow the repository host's sensitive-data removal process.

## Provenance record

For every public dataset, add:

```text
publisher:
title:
retrieved:
source_url:
licence:
release_basis:
transformations:
```

If any field is unknown, do not commit the dataset. Use `examples/demo_series.csv` as a safe placeholder while the rights question is resolved.

## Bring-your-own-data workflow

The extraction scripts accept local inputs so users can work under their own access rights. Local source folders belong in an ignored path such as `data/raw/`. Public commits should contain the schema and code, never the protected input or a substitute that recreates it.
