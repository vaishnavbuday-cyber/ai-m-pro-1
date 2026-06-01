"""
Traffic Accident Analysis System — Backend Utilities
Data preprocessing, analysis, and insight generation functions.
"""

import pandas as pd
import numpy as np


def preprocess_dataframe(df):
    """Clean and preprocess the accident dataset.
    Returns (cleaned_df, stats_dict).
    """
    original_rows = len(df)

    # Remove exact duplicates
    df = df.drop_duplicates()
    duplicates_removed = original_rows - len(df)

    # Track missing values
    missing_before = int(df.isnull().sum().sum())

    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Fill categorical columns with mode
    cat_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in cat_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else "Unknown")

    missing_after = int(df.isnull().sum().sum())

    # Parse date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Month_Name"] = df["Date"].dt.strftime("%b")
        df["Day_of_Week"] = df["Date"].dt.day_name()

    # Parse time column
    if "Time" in df.columns:
        try:
            time_parsed = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce")
            df["Hour"] = time_parsed.dt.hour.fillna(12).astype(int)
        except Exception:
            df["Hour"] = 12

    # Auto-generate Driver_Age if missing (for demo purposes)
    if "Driver_Age" not in df.columns:
        np.random.seed(42)  # For reproducibility
        df["Driver_Age"] = np.random.normal(loc=35, scale=12, size=len(df)).clip(16, 80).astype(int)

    # Categorize into Age Groups
    if "Driver_Age" in df.columns:
        bins = [0, 26, 41, 61, 120]
        labels = ["<25", "26-40", "41-60", "60+"]
        df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, right=False).astype(str)

    stats = {
        "duplicates_removed": duplicates_removed,
        "missing_fixed": missing_before - missing_after,
        "total_records": len(df),
    }
    return df, stats


def compute_summary(df):
    """Compute dashboard summary statistics."""
    total = len(df)
    fatal = int((df["Severity"] == "Fatal").sum()) if "Severity" in df.columns else 0
    major = int((df["Severity"] == "Major").sum()) if "Severity" in df.columns else 0
    minor = int((df["Severity"] == "Minor").sum()) if "Severity" in df.columns else 0
    total_fatalities = int(df["Fatalities"].sum()) if "Fatalities" in df.columns else 0
    total_injuries = int(df["Injuries"].sum()) if "Injuries" in df.columns else 0

    peak_hour = None
    if "Hour" in df.columns:
        peak_hour = int(df["Hour"].mode().iloc[0])

    most_dangerous = None
    if "Location" in df.columns:
        most_dangerous = df["Location"].value_counts().idxmax()

    return {
        "total": total,
        "fatal": fatal,
        "major": major,
        "minor": minor,
        "totalFatalities": total_fatalities,
        "totalInjuries": total_injuries,
        "peakHour": peak_hour,
        "mostDangerous": most_dangerous,
    }


def compute_analysis(df, age_breaks=[25, 40, 60]):
    """Compute aggregated analysis data for charts."""
    result = {}

    # By location
    if "Location" in df.columns:
        loc_counts = df["Location"].value_counts().head(15)
        result["byLocation"] = [{"name": n, "count": int(c)} for n, c in loc_counts.items()]

    # Monthly trend
    if "Date" in df.columns and "Year" in df.columns:
        monthly = df.groupby([df["Date"].dt.to_period("M")]).size().reset_index(name="count")
        monthly["period"] = monthly["Date"].astype(str)
        result["byMonth"] = [{"name": r["period"], "count": int(r["count"])} for _, r in monthly.iterrows()]

    # By severity
    if "Severity" in df.columns:
        sev = df["Severity"].value_counts()
        colors = {"Fatal": "#ff4757", "Major": "#ffa502", "Minor": "#2ed573"}
        result["bySeverity"] = [{"name": n, "value": int(c), "fill": colors.get(n, "#70a1ff")} for n, c in sev.items()]

    # By hour
    if "Hour" in df.columns:
        hour_counts = df["Hour"].value_counts().sort_index()
        result["byHour"] = [{"name": f"{int(h)}:00", "count": int(c)} for h, c in hour_counts.items()]

    # By weather
    if "Weather" in df.columns:
        weather = df["Weather"].value_counts()
        result["byWeather"] = [{"name": n, "count": int(c)} for n, c in weather.items()]

    # By cause
    if "Cause" in df.columns:
        cause = df["Cause"].value_counts().head(10)
        result["byCause"] = [{"name": n, "count": int(c)} for n, c in cause.items()]

    # By vehicle type
    if "Vehicle_Type" in df.columns:
        vehicle = df["Vehicle_Type"].value_counts()
        result["byVehicle"] = [{"name": n, "count": int(c)} for n, c in vehicle.items()]

    # By road type
    if "Road_Type" in df.columns:
        road = df["Road_Type"].value_counts()
        result["byRoadType"] = [{"name": n, "count": int(c)} for n, c in road.items()]

    # By light condition
    if "Light_Condition" in df.columns:
        light = df["Light_Condition"].value_counts()
        result["byLight"] = [{"name": n, "count": int(c)} for n, c in light.items()]

    # By region
    if "Region" in df.columns:
        region = df["Region"].value_counts()
        result["byRegion"] = [{"name": n, "count": int(c)} for n, c in region.items()]

    # By age group
    if "Driver_Age" in df.columns:
        bins = [0, age_breaks[0] + 1, age_breaks[1] + 1, age_breaks[2] + 1, 120]
        labels = [f"<{age_breaks[0]+1}", f"{age_breaks[0]+1}-{age_breaks[1]}", f"{age_breaks[1]+1}-{age_breaks[2]}", f"{age_breaks[2]+1}+"]
        df_age_group = pd.cut(df["Driver_Age"], bins=bins, labels=labels, right=False).astype(str)
        age_counts = df_age_group.value_counts()
        result["byAgeGroup"] = [{"name": n, "count": int(age_counts.get(n, 0))} for n in labels]

    # Day-of-week x Hour heatmap data
    if "Day_of_Week" in df.columns and "Hour" in df.columns:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_data = []
        for day in day_order:
            day_df = df[df["Day_of_Week"] == day]
            if not day_df.empty:
                for hour in range(24):
                    count = int((day_df["Hour"] == hour).sum())
                    heatmap_data.append({"day": day, "hour": hour, "count": count})
        result["heatmap"] = heatmap_data

    return result


def generate_insights(df):
    """Auto-generate key insights from the data."""
    insights = []
    total = len(df)
    insights.append(f"Total {total} accident records analyzed.")

    if "Severity" in df.columns:
        fatal_pct = (df["Severity"] == "Fatal").mean() * 100
        insights.append(f"Fatal accidents account for {fatal_pct:.1f}% of all incidents.")

    if "Location" in df.columns:
        top_loc = df["Location"].value_counts().idxmax()
        top_count = int(df["Location"].value_counts().max())
        insights.append(f"Most accident-prone area: {top_loc} ({top_count} incidents).")

    if "Hour" in df.columns:
        peak = int(df["Hour"].mode().iloc[0])
        insights.append(f"Peak accident hour: {peak}:00 hours.")

    if "Weather" in df.columns:
        insights.append(f"Most common weather during accidents: {df['Weather'].value_counts().idxmax()}.")

    if "Cause" in df.columns:
        insights.append(f"Leading cause: {df['Cause'].value_counts().idxmax()}.")

    if "Vehicle_Type" in df.columns:
        insights.append(f"Most involved vehicle type: {df['Vehicle_Type'].value_counts().idxmax()}.")

    if "Road_Type" in df.columns:
        insights.append(f"Most dangerous road type: {df['Road_Type'].value_counts().idxmax()}.")

    if "Region" in df.columns:
        insights.append(f"Region with highest incidents: {df['Region'].value_counts().idxmax()}.")

    if "Fatalities" in df.columns:
        insights.append(f"Total fatalities recorded: {int(df['Fatalities'].sum())}.")

    return insights
