# Site Papers Mirror Bundle

## Assumptions

This bundle goes into `StegVerse-Labs/Site`.

The source repo is:

```text
StegVerse-Labs/GCAT-BCAT-Engine
```

The source folder is:

```text
publisher/papers
```

The target public page is:

```text
Papers.html
```

The target mirrored directory is:

```text
papers/
```

## Done condition

The mirror is working when the Site repo contains:

```text
scripts/mirror_papers.py
Papers.html
papers/index.html
papers/papers_manifest.json
github/workflows/mirror-papers.yml
```

and the workflow:

```text
Mirror Papers from GCAT-BCAT-Engine
```

runs green and commits any changed paper files back to the Site repo.

## What it fixes

This fixes both surfaces:

```text
/Papers.html
/papers/
```

`Papers.html` becomes the public index page.

`papers/index.html` prevents the `papers/` route from returning 404 after the workflow has run.

## How it works

```text
Checkout Site
Checkout GCAT-BCAT-Engine into _source
Copy _source/publisher/papers into Site/papers
Generate Papers.html
Generate papers/index.html
Generate papers/papers_manifest.json
Commit changes back to Site
```

## iOS workflow note

The workflow is included at:

```text
github/workflows/mirror-papers.yml
```

The leading dot has been removed for iOS display and Files-app compatibility.

In GitHub, place it at:

```text
.github/workflows/mirror-papers.yml
```

## Important note

This mirror runs on a schedule or manually from the Site repo.

A push to `GCAT-BCAT-Engine` does not automatically trigger the Site workflow unless you add a dispatch workflow in the source repo later.
