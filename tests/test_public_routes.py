"""Public route security regression checks for the hosted demo API."""
from fastapi.testclient import TestClient

from api.index import app


client = TestClient(app)


def test_public_ui_assets_are_served():
    for name in ("style.css", "app.js", "avatar.png"):
        assert client.get(f"/ui/{name}").status_code == 200


def test_private_repository_files_are_not_public():
    for path in (
        "/data/auracommerce.db",
        "/Yves_Iragena_SaaS_Resume_FINAL.pdf",
        "/AuraCommerce_Project_Report.pdf",
        "/remote.txt",
        "/requirements.txt",
        "/ui/../data/auracommerce.db",
    ):
        assert client.get(path).status_code == 404, path


def test_unknown_ui_asset_is_not_served():
    assert client.get("/ui/private.txt").status_code == 404


def test_api_state_uses_demo_data():
    response = client.get("/api/state")
    assert response.status_code == 200
    assert "health_score" in response.json()
