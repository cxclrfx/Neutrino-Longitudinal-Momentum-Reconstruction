# Dependency and licensing review

The repository was empty before implementation. No third-party source code was
copied into the reconstruction, scripts, or tests. The numerical core and tests
use the Python standard library only. Python is distributed under the PSF license.

Optional figure generation uses the pinned environment in requirements-figures.txt.
Installed distribution metadata and available license texts were inspected:

| Package | Version | License |
|---|---|---|
| matplotlib | 3.10.7 | Matplotlib license (PSF-based) |
| numpy | 2.5.3 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 |
| contourpy | 1.4.0 | BSD-3-Clause |
| cycler | 0.12.1 | BSD-3-Clause |
| fonttools | 4.66.1 | MIT |
| kiwisolver | 1.5.1 | BSD-3-Clause |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause |
| pillow | 12.3.0 | MIT-CMU |
| pyparsing | 3.3.3 | MIT |
| python-dateutil | 2.9.0.post0 | Apache-2.0 OR BSD-3-Clause |
| six | 1.17.0 | MIT |
| setuptools (build) | 80.9.0 | MIT |

These dependencies introduce no identified incompatibility with the original
AGPL-3.0-or-later software. Dependencies and their binaries are not vendored.
Upstream notices remain applicable if anyone redistributes them. PDF figures
embed DejaVu font subsets; their separate license is retained under figures/.
GitHub Actions uses actions/checkout and actions/setup-python (MIT); those actions
are referenced, not copied into the repository.

Software and original documentation use AGPL-3.0-or-later; alternative commercial
terms are available by agreement. CERN source data/metadata remain CC0-1.0.
LICENSE is the full unmodified GNU AGPL version 3 text downloaded from
https://www.gnu.org/licenses/agpl-3.0.txt; NOTICE expressly grants the later-version option.
