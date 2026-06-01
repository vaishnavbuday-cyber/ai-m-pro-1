"""
Generate a realistic Indian traffic accident dataset for the year 2025.
This includes more diverse Indian locations and the Driver_Age field.
"""

import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(2025)

# Configuration
NUM_RECORDS = 2000
YEAR = 2025

# Diverse Indian Locations (Name, Latitude, Longitude, City)
LOCATIONS = [
    ("MG Road, Bangalore", 12.9716, 77.5946),
    ("Connaught Place, Delhi", 28.6315, 77.2167),
    ("Marine Drive, Mumbai", 18.9438, 72.8232),
    ("Anna Salai, Chennai", 13.0604, 80.2496),
    ("Park Street, Kolkata", 22.5530, 88.3512),
    ("Banjara Hills, Hyderabad", 17.4122, 78.4350),
    ("FC Road, Pune", 18.5255, 73.8409),
    ("Outer Ring Road, Bangalore", 12.9352, 77.6245),
    ("NH-48 Highway, Delhi-Mumbai", 22.3650, 72.9344),
    ("Electronic City, Bangalore", 12.8399, 77.6770),
    ("Marine Drive, Kochi", 9.9760, 76.2757),
    ("Pink City Road, Jaipur", 26.9124, 75.7873),
    ("Sabarmati Road, Ahmedabad", 23.0583, 72.5802),
    ("Hazratganj, Lucknow", 26.8467, 80.9462),
    ("Chandni Chowk, Delhi", 28.6600, 77.2300),
    ("Gateway Area, Mumbai", 18.9220, 72.8347),
    ("Howrah Bridge Road, Kolkata", 22.5851, 88.3468),
    ("Charminar Area, Hyderabad", 17.3616, 78.4747),
    ("Varkala Road, Kerala", 8.7333, 76.7167),
    ("Fatehpur Sikri Road, Agra", 27.0911, 77.6737),
    ("Mall Road, Shimla", 31.1048, 77.1734),
    ("Paltan Bazaar, Guwahati", 26.1820, 91.7520),
    ("Main Guard Gate, Trichy", 10.8284, 78.6946),
    ("Zion Hill, Kodaikanal", 10.2381, 77.4892),
    ("S.G. Highway, Ahmedabad", 23.0225, 72.5714),
    ("Indiranagar 100ft Road, Bangalore", 12.9719, 77.6412),
    ("Salt Lake City, Kolkata", 22.5868, 88.4178),
    ("T. Nagar, Chennai", 13.0418, 80.2341),
    ("Sector 17, Chandigarh", 30.7415, 76.7827),
    ("Raja Park, Jaipur", 26.8966, 75.8344),
]

VEHICLE_TYPES = [
    "Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw",
    "Bicycle", "Pedestrian", "Van", "SUV", "Scooter", "Tractor"
]

WEATHER_CONDITIONS = [
    "Clear", "Rainy", "Foggy", "Cloudy", "Stormy", "Windy", "Heatwave"
]

SEVERITY_LEVELS = ["Fatal", "Major", "Minor"]
SEVERITY_WEIGHTS = [0.10, 0.35, 0.55] # Slightly higher severity for 2025 realism

CAUSES = [
    "Over-speeding", "Drunk driving", "Signal violation", "Wrong-side driving",
    "Distracted driving", "Poor road condition", "Vehicle malfunction",
    "Pedestrian error", "Tailgating", "Lane changing without signal",
    "Overloading", "Tire burst", "Brake failure", "Road rage", "Animal crossing",
    "Sleep deprivation", "Bad lighting"
]

def generate_dataset():
    records = []
    start_date = datetime(YEAR, 1, 1)
    end_date = datetime(YEAR, 12, 31)
    
    delta_days = (end_date - start_date).days

    for i in range(1, NUM_RECORDS + 1):
        # Random date within 2025
        random_days = random.randint(0, delta_days)
        accident_date = start_date + timedelta(days=random_days)

        # Weighted hour generation (rush hours: 8-10 AM, 5-8 PM)
        hour_weights = [1]*6 + [2]*2 + [6]*2 + [3]*4 + [4]*2 + [7]*3 + [5]*2 + [2]*3
        hour = random.choices(range(24), weights=hour_weights, k=1)[0]
        minute = random.randint(0, 59)
        accident_time = f"{hour:02d}:{minute:02d}"

        # Location with coordinates (add small random offset)
        loc_name, base_lat, base_lng = random.choice(LOCATIONS)
        lat = round(base_lat + random.uniform(-0.02, 0.02), 6)
        lng = round(base_lng + random.uniform(-0.02, 0.02), 6)

        vehicle_type = random.choices(VEHICLE_TYPES, weights=[25, 30, 8, 10, 15, 2, 3, 2, 3, 1, 1], k=1)[0]
        
        # Weather weighted by month (more rain in monsoon months)
        month = accident_date.month
        if month in [6, 7, 8, 9]: # Monsoon
            weather_weights = [20, 50, 5, 15, 5, 5, 0]
        elif month in [11, 12, 1]: # Winter
            weather_weights = [40, 5, 40, 10, 0, 5, 0]
        elif month in [4, 5]: # Summer
            weather_weights = [60, 0, 0, 10, 5, 5, 20]
        else:
            weather_weights = [60, 10, 10, 10, 5, 5, 0]
            
        weather = random.choices(WEATHER_CONDITIONS, weights=weather_weights, k=1)[0]
        severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS, k=1)[0]
        cause = random.choice(CAUSES)

        # Injuries and fatalities based on severity
        if severity == "Fatal":
            injuries = random.randint(1, 10)
            fatalities = random.randint(1, 4)
        elif severity == "Major":
            injuries = random.randint(1, 6)
            fatalities = random.choices([0, 1], weights=[90, 10], k=1)[0]
        else:
            injuries = random.randint(0, 3)
            fatalities = 0

        # Driver Age generation
        driver_age = int(random.gauss(34, 11))
        driver_age = max(16, min(85, driver_age))
        
        # Age Group
        if driver_age < 26:
            age_group = "<26"
        elif driver_age <= 40:
            age_group = "26-40"
        elif driver_age <= 60:
            age_group = "41-60"
        else:
            age_group = "60+"

        records.append({
            "ID": 20250000 + i,
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
            "Driver_Age": driver_age,
            "Age_Group": age_group
        })

    return records

def main():
    records = generate_dataset()
    output_file = "indian_accident_data_2025.csv"
    fieldnames = [
        "ID", "Date", "Time", "Location", "Latitude", "Longitude",
        "Vehicle_Type", "Weather", "Severity", "Cause", "Injuries", "Fatalities",
        "Driver_Age", "Age_Group"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Successfully generated {len(records)} records for year 2025.")
    print(f"Saved to: {output_file}")
    
    # Also update the main sample file for the website to use it immediately
    with open("sample_accident_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"Updated sample_accident_data.csv with the 2025 dataset.")

if __name__ == "__main__":
    main()
