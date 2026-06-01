"""
Integration tests for Flask API endpoints.
"""

import io
import pytest
import pandas as pd
from app import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_csv():
    """Generate a small CSV file in memory."""
    df = pd.DataFrame({
        "Date": ["2024-01-15", "2024-02-20", "2024-03-10"],
        "Time": ["08:30", "14:00", "22:15"],
        "Location": ["Highway A1", "City Center", "Highway A1"],
        "Vehicle_Type": ["Car", "Truck", "Motorcycle"],
        "Weather": ["Rainy", "Clear", "Foggy"],
        "Severity": ["Fatal", "Major", "Minor"],
        "Cause": ["Speeding", "Distracted", "DUI"],
        "Fatalities": [2, 0, 0],
        "Injuries": [3, 2, 1],
    })
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return io.BytesIO(csv_bytes)


# ─── Health ───

class TestHealthEndpoint:
    def test_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_has_status_ok(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "ok"


# ─── Upload ───

class TestUploadEndpoint:
    def test_upload_csv_success(self, client, sample_csv):
        resp = client.post("/upload", data={
            "file": (sample_csv, "test_data.csv"),
        }, content_type="multipart/form-data")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["message"] == "File uploaded successfully"
        assert data["rows"] == 3
        assert "columns" in data
        assert "preview" in data

    def test_upload_no_file(self, client):
        resp = client.post("/upload")
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_upload_unsupported_format(self, client):
        fake = io.BytesIO(b"not a real file")
        resp = client.post("/upload", data={
            "file": (fake, "test.txt"),
        }, content_type="multipart/form-data")
        assert resp.status_code == 400
        assert "Unsupported" in resp.get_json()["error"]


# ─── Summary ───

class TestSummaryEndpoint:
    def test_summary_after_upload(self, client, sample_csv):
        # Upload first
        client.post("/upload", data={
            "file": (sample_csv, "test.csv"),
        }, content_type="multipart/form-data")
        # Then get summary
        resp = client.get("/summary")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total" in data
        assert "fatal" in data
        assert "insights" in data


# ─── Charts ───

class TestChartsEndpoint:
    def test_charts_after_upload(self, client, sample_csv):
        client.post("/upload", data={
            "file": (sample_csv, "test.csv"),
        }, content_type="multipart/form-data")
        resp = client.get("/charts")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "summary" in data
        assert "charts" in data
        assert "insights" in data


# ─── Analysis ───

class TestAnalysisEndpoint:
    def test_analysis_after_upload(self, client, sample_csv):
        client.post("/upload", data={
            "file": (sample_csv, "test.csv"),
        }, content_type="multipart/form-data")
        resp = client.get("/analysis")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, dict)
