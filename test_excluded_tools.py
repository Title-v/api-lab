import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]])
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# An impossible tool restriction should be refused with 400 and a JSON error.
@pytest.mark.xfail(reason="Defect 1: excluding all tools returns 500 with an empty body instead of 400 with a JSON error", strict=True)
def test_all_tools_excluded_is_refused(api, auth):
    res = api.post("/api/pizza", json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}, headers=auth)
    assert res.status_code == 400
    assert isinstance(res.json().get("error"), str)
    assert res.json()["error"]
