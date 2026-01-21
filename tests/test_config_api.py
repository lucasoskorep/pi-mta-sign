import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestStationsEndpoint:
    def test_get_stations_returns_list(self, client):
        response = client.get("/api/stations")
        assert response.status_code == 200
        data = response.json()
        assert "stations" in data
        assert isinstance(data["stations"], list)

    def test_get_stations_returns_station_objects(self, client):
        response = client.get("/api/stations")
        assert response.status_code == 200
        data = response.json()
        if len(data["stations"]) > 0:
            station = data["stations"][0]
            assert "id" in station
            assert "name" in station

    def test_get_stations_search_filters_by_name(self, client):
        response = client.get("/api/stations", params={"search": "Times"})
        assert response.status_code == 200
        data = response.json()
        for station in data["stations"]:
            assert "times" in station["name"].lower() or "Times" in station["id"]

    def test_get_stations_search_filters_by_id(self, client):
        response = client.get("/api/stations", params={"search": "127"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["stations"]) > 0
        found = any(s["id"] == "127" for s in data["stations"])
        assert found


class TestLinesEndpoint:
    def test_get_lines_returns_list(self, client):
        response = client.get("/api/lines")
        assert response.status_code == 200
        data = response.json()
        assert "lines" in data
        assert isinstance(data["lines"], list)

    def test_get_lines_contains_expected_lines(self, client):
        response = client.get("/api/lines")
        assert response.status_code == 200
        data = response.json()
        lines = data["lines"]
        # Check for some known lines
        assert "A" in lines
        assert "C" in lines
        assert "E" in lines
        assert "1" in lines
        assert "L" in lines

    def test_get_lines_are_sorted(self, client):
        response = client.get("/api/lines")
        assert response.status_code == 200
        data = response.json()
        lines = data["lines"]
        assert lines == sorted(lines)


class TestConfigEndpoint:
    def test_get_config_returns_response(self, client):
        response = client.get("/api/config")
        assert response.status_code == 200
