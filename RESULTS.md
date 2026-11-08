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
1. Real API integration tests can detect a mismatch between request JSON handling and server validation, and failures in routing/session persistence across the load balancer and backend storage. Stubs can return the expected answers without exercising those integrations. Unit tests with stubs are still useful because they isolate logic, run quickly and deterministically, and do not depend on network availability.
2. Unique fictitious users keep each test's ratings separate, avoid collisions, and prevent changes to other students' data. The public token represents shared practice data. In Project 2, create uniquely named records using the group's authorized account, keep track of their IDs, and clean up only those records; never reuse another group's data.
3. A requests.Session retains AWSALB cookies so later requests reach the backend that knows the user created earlier. Without it, creation and login can reach different servers. The three optional runs were fail (login 401), pass, fail (login 401), with no code change. The demonstration test was removed afterwards.
4. Excluding all three tools revealed Defect 1. An empty 500 looks like an internal failure and gives an API client no reason it can display or act upon; a 400 with a message explains that the restriction cannot be satisfied. Keeping the test as strict xfail documents the intended contract while acknowledging the known bug. Once the fix makes it pass, strict xfail produces a failing XPASS so the marker must be removed.
5. Base choice requires 1 + (3-1) + (4-1) + (2-1) + (3-1) = 9 tests. All combinations require 3 × 4 × 2 × 3 = 72 tests. Boundary tests in Step A3 are separate from these nine creation cases.
6. Observed GET 404, PUT 400 and DELETE 400. For an authenticated user lacking permission, 403 would be a clear choice; 404 can deliberately hide a resource's existence. A 400 is less precise, but all operations were refused and the owner's full rating remained unchanged. This meets the lab's explicit 4xx requirement, so the differing codes alone do not demonstrate an authorization defect without a stronger status-code contract.
7. The read-only command `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` returned HTTP 200 with a ratings array containing 50 entries, even though the token was the made-up 16-character value and was never issued by login. The rating contents are not reproduced here. Accepting an unissued token on a protected endpoint is an authentication defect; the expected response is 401 with an authentication error. On a real system, an outsider could potentially obtain protected rating information without authenticating. This observation establishes read access only, not write access or which users own the returned records. No writes were attempted with this token.
8. API tests directly check exact status codes, JSON fields, validation and authorization rules, including inputs a UI cannot submit. Browser tests can check visible layout, rendering and whether controls let a user complete the intended workflow, which API-only tests cannot see.

## Step-by-step execution
- Step 0.5: Python requests returned names: 200, application/json, dict, first name Americana; tools: 200, Knife/Pizza cutter/Scissors; vegetarian pizza: 200, The Nasty Fungi e Olive.
- Step 0.6: Margherita passed; Pineapple Supreme failed with AssertionError; restored Margherita and confirmed 1 passed. Environment: Python 3.13.
- Step 0.9: Created a unique fictitious user (201), logged in (200), read own empty ratings (200, {"ratings": []}); session retained AWSALB and AWSALBCORS cookies. Private token was not saved.

## Final verification
- Command: `pytest -v --html=report.html --self-contained-html`.
- Result on 9 November 2026 (Asia/Bangkok): 32 passed, 1 xfailed in 48.40 seconds; no unexpected failures or errors.
- Opened the self-contained HTML report in a browser and verified its summary and the expected failure's 500-versus-400 assertion.
