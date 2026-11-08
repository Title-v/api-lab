# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.2, `curl -i https://quickpizza.grafana.com/api/names`: status `HTTP/2 200`; `content-type: application/json`; `set-cookie: AWSALB=...` is present (also `AWSALBCORS`). After the blank line, the JSON body contains the same 18 pizza names as Step 0.1. The `-i` option includes the status line and response headers. Cookie values are omitted.
- Step 0.3, status code of the request without a token: 401; body: `{"error":"authentication failed"}`. With the public practice token in `auth.txt`, `GET /api/tools` returns 200 and `{"tools":["Knife","Pizza cutter","Scissors"]}`.
- Step 0.4, the name of your pizza: The Funny Pugliese. Sent `curl -H "@auth.txt" -d "@veg.json" https://quickpizza.grafana.com/api/pizza` with `{"mustBeVegetarian": true}`. Response status: 200; every ingredient has `"vegetarian": true`.
- Step 0.12, results of the three runs without a session (optional): failed (login 401), passed, failed (login 401). Removed the demonstration test afterwards.
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, or 3 distinct tools. The original two inputs both covered only the 1-tool block. Added [], [Knife, Scissors], and all three tools; only the all-three block failed.

## Defect report
- Title: Defect 1: excluding every tool causes an internal server error.
- Request: POST /api/pizza with {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}; confirmed with `curl -H "@auth.txt" -d "@excluded_all.json" https://quickpizza.grafana.com/api/pizza`.
- Expected result: 400 with a non-empty JSON error message explaining that no pizza satisfies the request.
- Actual result: 500 with an empty body (0 bytes), reproduced with pytest and curl.
- Severity: Medium: a validly formed but unsatisfiable restriction triggers a server error and gives clients no actionable explanation; no data loss was observed.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: GET 404, PUT 400, DELETE 400. The owner could still read the full unchanged rating after every refused attempt. Full suite: 32 passed, 1 xfailed.

## Part B
1.
2.
3.
4.
5.
6.
7.
8.

## Step-by-step execution
- Step 0.5: Python requests returned names: 200, application/json, dict, first name Americana; tools: 200, Knife/Pizza cutter/Scissors; vegetarian pizza: 200, The Nasty Fungi e Olive.
- Step 0.6: Margherita passed; Pineapple Supreme failed with AssertionError; restored Margherita and confirmed 1 passed. Environment: Python 3.13.
- Step 0.9: Created a unique fictitious user (201), logged in (200), read own empty ratings (200, {"ratings": []}); session retained AWSALB and AWSALBCORS cookies. Private token was not saved.
