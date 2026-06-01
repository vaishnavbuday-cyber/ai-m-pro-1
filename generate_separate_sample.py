"""
Generate a smaller separate sample accident dataset for testing.
"""

import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(99)

NUM_RECORDS = 100
YEAR = 2025

# Small subset of locations for a "sample"
LOCATIONS = [
    ("MG Road, Bangalore", 12.9716, 77.5946, "South"),
    ("Connaught Place, Delhi", 28.6315, 77.2167, "North"),
    ("Marine Drive, Mumbai", 18.9438, 72.8232, "West"),
    ("Anna Salai, Chennai", 13.0604, 80.2496, "South"),
    ("Park Street, Kolkata", 22.5530, 88.3512, "East"),
]

VEHICLE_TYPES = ["Car", "Motorcycle", "Bus", "Auto-rickshaw"]
WEATHER_CONDITIONS = ["Clear", "Rainy", "Foggy"]
SEVERITY_LEVELS = ["Fatal", "Major", "Minor"]
CAUSES = ["Over-speeding", "Drunk driving", "Signal violation", "Poor road condition"]
ROAD_TYPES = ["Highway", "City Road"]
LIGHT_CONDITIONS = ["Daylight", "Darkness"]

def generate_sample():
    records = []
    start_date = datetime(YEAR, 1, 1)
    
    for i in range(1, NUM_RECORDS + 1):
        accident_date = start_date + timedelta(days=random.randint(0, 364))
        accident_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        loc_name, base_lat, base_lng, region = random.choice(LOCATIONS)
        
        records.append({
            "ID": 20259000 + i,
            "Date": accident_date.strftime("%Y-%m-%d"),
            "Time": accident_time,
            "Location": loc_name,
            "Latitude": round(base_lat + random.uniform(-0.01, 0.01), 6),
            "Longitude": round(base_lng + random.uniform(-0.01, 0.01), 6),
            "Vehicle_Type": random.choice(VEHICLE_TYPES),
            "Weather": random.choice(WEATHER_CONDITIONS),
            "Severity": random.choice(SEVERITY_LEVELS),
            "Cause": random.choice(CAUSES),
            "Injuries": random.randint(0, 5),
            "Fatalities": random.randint(0, 2),
            "Driver_Age": random.randint(18, 70),
            "Age_Group": "Unknown", # Pre-process handles this
            "Road_Type": random.choice(ROAD_TYPES),
            "Light_Condition": random.choice(LIGHT_CONDITIONS),
            "Region": region
        })
    return records

def main():
    records = generate_sample()
    output_file = "separate_sample_accident_data.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Created separate sample dataset: {output_file}")

if __name__ == "__main__":
    main()
