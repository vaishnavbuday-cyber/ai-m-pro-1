"""
Generate a realistic sample traffic accident dataset for the Traffic Accident Analysis System.
Run this script once to create sample_accident_data.csv.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# Configuration
NUM_RECORDS = 500

LOCATIONS = [
    ("MG Road", 12.9716, 77.5946),
    ("Connaught Place", 28.6315, 77.2167),
    ("Marine Drive", 18.9438, 72.8232),
    ("Anna Salai", 13.0604, 80.2496),
    ("Park Street", 22.5530, 88.3512),
    ("Banjara Hills", 17.4122, 78.4350),
    ("FC Road", 18.5255, 73.8409),
    ("Brigade Road", 12.9719, 77.6074),
    ("Jubilee Hills", 17.4318, 78.4072),
    ("Linking Road", 19.0728, 72.8364),
    ("Outer Ring Road", 12.9352, 77.6245),
    ("NH-48 Highway", 12.8996, 77.5096),
    ("Electronic City", 12.8399, 77.6770),
    ("Whitefield Road", 12.9698, 77.7500),
    ("Silk Board Junction", 12.9172, 77.6227),
    ("Marathahalli Bridge", 12.9562, 77.7009),
    ("Hebbal Flyover", 13.0358, 77.5970),
    ("KR Puram Junction", 13.0012, 77.6881),
    ("Bellandur Gate", 12.9255, 77.6760),
    ("Sarjapur Road", 12.9100, 77.6850),
]

VEHICLE_TYPES = [
    "Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw",
    "Bicycle", "Pedestrian", "Van", "SUV", "Scooter"
]

WEATHER_CONDITIONS = [
    "Clear", "Rainy", "Foggy", "Cloudy", "Stormy", "Windy"
]

SEVERITY_LEVELS = ["Fatal", "Major", "Minor"]
SEVERITY_WEIGHTS = [0.08, 0.30, 0.62]

CAUSES = [
    "Over-speeding", "Drunk driving", "Signal violation", "Wrong-side driving",
    "Distracted driving", "Poor road condition", "Vehicle malfunction",
    "Pedestrian error", "Tailgating", "Lane changing without signal",
    "Overloading", "Tire burst", "Brake failure", "Road rage"
]

def generate_dataset():
    records = []
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta_days = (end_date - start_date).days

    for i in range(1, NUM_RECORDS + 1):
        # Random date within range
        random_days = random.randint(0, delta_days)
        accident_date = start_date + timedelta(days=random_days)

        # Weighted hour generation (more accidents during rush hours)
        hour_weights = [1]*6 + [3]*2 + [5]*2 + [2]*4 + [3]*2 + [5]*3 + [3]*2 + [1]*3
        hour = random.choices(range(24), weights=hour_weights, k=1)[0]
        minute = random.randint(0, 59)
        accident_time = f"{hour:02d}:{minute:02d}"

        # Location with coordinates (add small random offset)
        loc_name, base_lat, base_lng = random.choice(LOCATIONS)
        lat = round(base_lat + random.uniform(-0.01, 0.01), 6)
        lng = round(base_lng + random.uniform(-0.01, 0.01), 6)

        vehicle_type = random.choice(VEHICLE_TYPES)
        weather = random.choices(
            WEATHER_CONDITIONS,
            weights=[40, 25, 15, 10, 5, 5],
            k=1
        )[0]
        severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS, k=1)[0]
        cause = random.choice(CAUSES)

        # Injuries and fatalities based on severity
        if severity == "Fatal":
            injuries = random.randint(1, 8)
            fatalities = random.randint(1, 3)
        elif severity == "Major":
            injuries = random.randint(1, 5)
            fatalities = random.choices([0, 1], weights=[85, 15], k=1)[0]
        else:
            injuries = random.randint(0, 2)
            fatalities = 0

        records.append({
            "ID": i,
            "Date": accident_date.strftime("%Y-%m-%d"),
            "Time": accident_time,
            "Location": loc_name,
            "Latitude": lat,
            "Longitude": lng,
            "Vehicle_Type": vehicle_type,
            "Weather": weather,
            "Severity": severity,
            "Cause": cause,
            "Injuries": injuries,
            "Fatalities": fatalities,
        })

    return records

def main():
    records = generate_dataset()
    output_file = "sample_accident_data.csv"
    fieldnames = [
        "ID", "Date", "Time", "Location", "Latitude", "Longitude",
        "Vehicle_Type", "Weather", "Severity", "Cause", "Injuries", "Fatalities"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records -> {output_file}")

if __name__ == "__main__":
    main()
