# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.2, `curl -i https://quickpizza.grafana.com/api/names`: status `HTTP/2 200`; `content-type: application/json`; `set-cookie: AWSALB=...` is present (also `AWSALBCORS`). After the blank line, the JSON body contains the same 18 pizza names as Step 0.1. The `-i` option includes the status line and response headers. Cookie values are omitted.
- Step 0.3, status code of the request without a token: 401; body: `{"error":"authentication failed"}`. With the public practice token in `auth.txt`, `GET /api/tools` returns 200 and `{"tools":["Knife","Pizza cutter","Scissors"]}`.
- Step 0.4, the name of your pizza:
- Step 0.12, results of the three runs without a session (optional):
- Step 0.16, blocks of "how many of the three tools are excluded":

## Defect report
- Title:
- Request:
- Expected result:
- Actual result:
- Severity:

## Part A
- Step A4, status codes when the other user reads, changes and deletes:

## Part B
1.
2.
3.
4.
5.
6.
7.
8.
