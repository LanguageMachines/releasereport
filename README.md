# Release Reports

This repository contains automatically generated software release reports (may be manually edited after initial generation) to report progress back to CLARIAH.

The reports are in ``reports/``


## Technical Details

* To run the ``releasereport.py`` script, set the ``GITHUB_USER`` and ``GITHUB_PASS`` environment variables.
* Markdown to PDF conversion is done as follows with ``pandoc``: ``pandoc -s -f gfm -H ../header.sty -o 2018-04-03-to-2018-06-21.pdf 2018-04-03-to-2018-06-21.md``


