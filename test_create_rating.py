import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth)
    assert res.status_code == 201
    body = res.json()
    try:
        assert body["stars"] == 3
        assert body["pizza_id"] == pizza_id
    finally:
        api.delete(f"/api/ratings/{body['id']}", headers=auth)


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal and text stars are rejected with their observed type errors.
@pytest.mark.parametrize("stars,error", [
    (3.5, "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"),
    ("3", "json: cannot unmarshal string into Go struct field Rating.stars of type int"),
], ids=["decimal", "text"])
def test_stars_wrong_type(api, auth, pizza_id, stars, error):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": error}


# C2: omitting stars is rejected while pizza and token stay at base values.
def test_missing_stars(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a nonexistent pizza cannot receive a rating.
def test_nonexistent_pizza(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: absent and wrong-length tokens cannot create ratings.
@pytest.mark.parametrize("headers", [{}, {"Authorization": "token short"}], ids=["none", "short"])
def test_invalid_token(api, pizza_id, headers):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=headers)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
