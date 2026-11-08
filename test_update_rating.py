import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Boundary stars 1/5 are saved; refused updates 0/6 leave the rating unchanged.
@pytest.mark.parametrize("stars,status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    if status == 200:
        assert res.json()["stars"] == stars
    else:
        assert res.json() == {"error": STARS_ERROR}
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json()["stars"] == (stars if status == 200 else rating["stars"])
