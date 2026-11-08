import uuid


# A username already created by this test cannot be registered twice.
def test_duplicate_username_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in to this test's user with a wrong password is refused.
def test_wrong_password_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users/token/login", json={**user, "password": "Wrong-2026"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# Registration with an empty username is refused with a useful message.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
