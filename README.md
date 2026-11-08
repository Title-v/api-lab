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
