"""
Unit tests for utils.py — data preprocessing, summary, analysis, and insights.
"""

import pytest
import pandas as pd
import numpy as np
from utils import preprocess_dataframe, compute_summary, compute_analysis, generate_insights


# ─── Fixtures ───

@pytest.fixture
def sample_df():
    """Minimal accident dataset for testing."""
    return pd.DataFrame({
        "Date": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-01-15", "2024-04-05"],
        "Time": ["08:30", "14:00", "22:15", "08:30", "10:00"],
        "Location": ["Highway A1", "City Center", "Highway A1", "Highway A1", "City Center"],
        "Vehicle_Type": ["Car", "Truck", "Motorcycle", "Car", "Bus"],
        "Weather": ["Rainy", "Clear", "Foggy", "Rainy", "Clear"],
        "Severity": ["Fatal", "Major", "Minor", "Fatal", "Major"],
        "Cause": ["Speeding", "Distracted", "DUI", "Speeding", "Distracted"],
        "Fatalities": [2, 0, 0, 2, 1],
        "Injuries": [3, 2, 1, 3, 4],
        "Latitude": [10.0, 10.5, 10.0, 10.0, 10.5],
        "Longitude": [76.0, 76.5, 76.0, 76.0, 76.5],
    })


@pytest.fixture
def sample_df_with_missing():
    """Dataset with missing values and duplicates."""
    return pd.DataFrame({
        "Date": ["2024-01-15", "2024-01-15", "2024-02-20", None],
        "Time": ["08:30", "08:30", None, "10:00"],
        "Location": ["Highway A1", "Highway A1", "City Center", None],
        "Severity": ["Fatal", "Fatal", "Minor", "Major"],
        "Fatalities": [2, 2, 0, np.nan],
        "Injuries": [3, 3, np.nan, 1],
    })


# ─── Preprocessing Tests ───

class TestPreprocessDataframe:
    def test_removes_duplicates(self, sample_df_with_missing):
        df, stats = preprocess_dataframe(sample_df_with_missing)
        assert stats["duplicates_removed"] == 1
        assert stats["total_records"] == 3

    def test_fills_missing_values(self, sample_df_with_missing):
        df, stats = preprocess_dataframe(sample_df_with_missing)
        assert stats["missing_fixed"] > 0
        assert df.isnull().sum().sum() == 0

    def test_parses_date_columns(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        assert "Year" in df.columns
        assert "Month" in df.columns
        assert "Day_of_Week" in df.columns

    def test_parses_time_column(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        assert "Hour" in df.columns
        assert df["Hour"].iloc[0] == 8

    def test_returns_stats_dict(self, sample_df):
        _, stats = preprocess_dataframe(sample_df)
        assert "duplicates_removed" in stats
        assert "missing_fixed" in stats
        assert "total_records" in stats


# ─── Summary Tests ───

class TestComputeSummary:
    def test_total_count(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        summary = compute_summary(df)
        assert summary["total"] == len(df)

    def test_severity_counts(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        summary = compute_summary(df)
        assert summary["fatal"] >= 1
        assert summary["major"] >= 1
        assert summary["minor"] >= 1

    def test_fatality_total(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        summary = compute_summary(df)
        assert summary["totalFatalities"] == 3  # 2+0+0+1 (1 record removed as duplicate)

    def test_peak_hour_present(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        summary = compute_summary(df)
        assert summary["peakHour"] is not None

    def test_most_dangerous_location(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        summary = compute_summary(df)
        assert summary["mostDangerous"] == "Highway A1"


# ─── Analysis Tests ───

class TestComputeAnalysis:
    def test_by_location(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        result = compute_analysis(df)
        assert "byLocation" in result
        assert len(result["byLocation"]) > 0
        assert "name" in result["byLocation"][0]
        assert "count" in result["byLocation"][0]

    def test_by_severity(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        result = compute_analysis(df)
        assert "bySeverity" in result
        for item in result["bySeverity"]:
            assert "name" in item
            assert "value" in item
            assert "fill" in item

    def test_by_hour(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        result = compute_analysis(df)
        assert "byHour" in result

    def test_heatmap_data(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        result = compute_analysis(df)
        assert "heatmap" in result
        assert len(result["heatmap"]) > 0


# ─── Insights Tests ───

class TestGenerateInsights:
    def test_returns_list(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        insights = generate_insights(df)
        assert isinstance(insights, list)
        assert len(insights) > 0

    def test_contains_total(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        insights = generate_insights(df)
        assert any("accident records" in i.lower() for i in insights)

    def test_contains_location(self, sample_df):
        df, _ = preprocess_dataframe(sample_df)
        insights = generate_insights(df)
        assert any("accident-prone" in i.lower() for i in insights)
