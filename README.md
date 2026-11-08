# API lab

ITCS386 Software Verification and Validation: API testing with pytest and requests.
Target: https://quickpizza.grafana.com

## Setup and execution

Use Python 3.10 or newer, Git and curl. Clone this repository into a folder outside cloud-sync services.

```sh
git clone https://github.com/Title-v/api-lab.git
cd api-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

On Windows PowerShell, use `python -m venv .venv` and `.venv\Scripts\activate`; use `curl.exe` for curl commands.

## Input domain model: POST /api/ratings

| Characteristic | Blocks | Values in the tests |
| --- | --- | --- |
| C1 Value of stars | below 1; 1 to 5 (base); above 5 | 0; 3; 6 |
| C2 Type of stars | whole number (base); decimal; text; missing | 3; 3.5; "3"; omitted field |
| C3 Pizza | exists (base); does not exist | a new pizza; 999999999 |
| C4 Token | user's own (base); none; wrong length | from auth; no header; token short |

Base choice varies one characteristic at a time, keeping the others at their base. The model requires 1 + (3-1) + (4-1) + (2-1) + (3-1) = 9 tests, versus 3 × 4 × 2 × 3 = 72 combinations. The C1 range blocks concern numeric values; C2 separately varies representation and missingness.

## Shared-site rules

Use fictional, unique users. Only create, modify or delete ratings owned by the current test. The public practice token is used only for the introductory tools/pizza requests, never for ratings writes. Ratings created by tests are cleaned up. Session cookies keep authenticated requests on the same backend. Run tests when needed, never in a repeated loop.

### Block-to-test mapping (Step A2)

All names below are in `test_create_rating.py`. Error messages were observed with curl before writing these assertions, using a fresh user's token and the same session cookies.

| Characteristic / block | Test |
| --- | --- |
| All four base blocks (C1 in range, C2 integer, C3 exists, C4 own token) | `test_base_choice_is_saved` |
| C1 below 1 | `test_stars_out_of_range[0]` |
| C1 above 5 | `test_stars_out_of_range[6]` |
| C2 decimal | `test_stars_wrong_type[decimal]` |
| C2 text | `test_stars_wrong_type[text]` |
| C2 missing | `test_missing_stars` |
| C3 does not exist | `test_nonexistent_pizza` |
| C4 none | `test_invalid_token[none]` |
| C4 wrong length | `test_invalid_token[short]` |

## Results and report

See `RESULTS.md` for observed responses, the defect report and reflection answers. `test_excluded_tools.py::test_all_tools_excluded_is_refused` is strict xfail for the confirmed all-tools-excluded defect. The final suite contains 33 cases: 32 passing cases and 1 expected failure while that defect remains.

```sh
pytest -v --html=report.html --self-contained-html
```

Open `report.html` in a browser. Short tracebacks avoid including authentication fixture values in published reports. The optional no-session demonstration was removed after three runs, as instructed. Each completed lab step has its own Git commit. Compared with the introductory snippets, successful create-rating tests also clean up their own ratings to respect the shared-site rule.
