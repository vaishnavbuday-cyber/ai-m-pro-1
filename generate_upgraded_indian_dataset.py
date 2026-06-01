"""
Generate an upgraded, realistic Indian traffic accident dataset for the year 2025.
This dataset includes more records, more locations, and additional features for better analysis.
"""

import csv
import random
import math
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

# Configuration
NUM_RECORDS = 5000
YEAR = 2025

# Expanded Indian Locations (Name, Latitude, Longitude, Region)
LOCATIONS = [
    ("MG Road, Bangalore", 12.9716, 77.5946, "South"),
    ("Connaught Place, Delhi", 28.6315, 77.2167, "North"),
    ("Marine Drive, Mumbai", 18.9438, 72.8232, "West"),
    ("Anna Salai, Chennai", 13.0604, 80.2496, "South"),
    ("Park Street, Kolkata", 22.5530, 88.3512, "East"),
    ("Banjara Hills, Hyderabad", 17.4122, 78.4350, "South"),
    ("FC Road, Pune", 18.5255, 73.8409, "West"),
    ("Outer Ring Road, Bangalore", 12.9352, 77.6245, "South"),
    ("NH-48 Highway, Delhi-Mumbai", 22.3650, 72.9344, "West"),
    ("Electronic City, Bangalore", 12.8399, 77.6770, "South"),
    ("Marine Drive, Kochi", 9.9760, 76.2757, "South"),
    ("Pink City Road, Jaipur", 26.9124, 75.7873, "North"),
    ("Sabarmati Road, Ahmedabad", 23.0583, 72.5802, "West"),
    ("Hazratganj, Lucknow", 26.8467, 80.9462, "North"),
    ("Chandni Chowk, Delhi", 28.6600, 77.2300, "North"),
    ("Gateway Area, Mumbai", 18.9220, 72.8347, "West"),
    ("Howrah Bridge Road, Kolkata", 22.5851, 88.3468, "East"),
    ("Charminar Area, Hyderabad", 17.3616, 78.4747, "South"),
    ("Varkala Road, Kerala", 8.7333, 76.7167, "South"),
    ("Fatehpur Sikri Road, Agra", 27.0911, 77.6737, "North"),
    ("Mall Road, Shimla", 31.1048, 77.1734, "North"),
    ("Paltan Bazaar, Guwahati", 26.1820, 91.7520, "East"),
    ("Main Guard Gate, Trichy", 10.8284, 78.6946, "South"),
    ("Zion Hill, Kodaikanal", 10.2381, 77.4892, "South"),
    ("S.G. Highway, Ahmedabad", 23.0225, 72.5714, "West"),
    ("Indiranagar 100ft Road, Bangalore", 12.9719, 77.6412, "South"),
    ("Salt Lake City, Kolkata", 22.5868, 88.4178, "East"),
    ("T. Nagar, Chennai", 13.0418, 80.2341, "South"),
    ("Sector 17, Chandigarh", 30.7415, 76.7827, "North"),
    ("Raja Park, Jaipur", 26.8966, 75.8344, "North"),
    ("Boring Road, Patna", 25.6120, 85.1150, "East"),
    ("Race Course, Coimbatore", 11.0168, 76.9558, "South"),
    ("Civil Lines, Nagpur", 21.1458, 79.0882, "Central"),
    ("Sayajigunj, Vadodara", 22.3072, 73.1812, "West"),
    ("M.G. Road, Indore", 22.7196, 75.8577, "Central"),
    ("Arera Colony, Bhopal", 23.2332, 77.4344, "Central"),
    ("MVP Colony, Visakhapatnam", 17.7122, 83.3292, "South"),
    ("Golden Temple Road, Amritsar", 31.6200, 74.8765, "North"),
    ("Bistupur, Jamshedpur", 22.8046, 86.2029, "East"),
    ("Vartak Nagar, Thane", 19.2183, 72.9781, "West"),
    ("Bibvewadi, Pune", 18.4789, 73.8681, "West"),
    ("Kothrud, Pune", 18.5074, 73.8077, "West"),
    ("Hitech City, Hyderabad", 17.4435, 78.3773, "South"),
    ("Bandra West, Mumbai", 19.0596, 72.8295, "West"),
    ("Gomti Nagar, Lucknow", 26.8667, 80.9944, "North"),
    ("Rishikesh-Haridwar Highway", 30.0668, 78.2911, "North"),
    ("Chenab Bridge Approach, J&K", 33.1500, 74.8333, "North"),
    ("Palm Beach Road, Navi Mumbai", 19.0176, 73.0184, "West"),
    ("Rajpath, Delhi", 28.6147, 77.2091, "North"),
    ("Victoria Memorial Area, Kolkata", 22.5448, 88.3426, "East"),
]

VEHICLE_TYPES = [
    "Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw",
    "Bicycle", "Van", "SUV", "Scooter", "Tractor", "Lorry"
]
VEHICLE_WEIGHTS = [25, 30, 8, 12, 15, 2, 3, 3, 5, 2, 2]

WEATHER_CONDITIONS = [
    "Clear", "Rainy", "Foggy", "Cloudy", "Stormy", "Windy", "Heatwave"
]

SEVERITY_LEVELS = ["Fatal", "Major", "Minor"]
SEVERITY_WEIGHTS = [0.12, 0.38, 0.50]

CAUSES = [
    "Over-speeding", "Drunk driving", "Signal violation", "Wrong-side driving",
    "Distracted driving", "Poor road condition", "Vehicle malfunction",
    "Pedestrian error", "Tailgating", "Lane changing without signal",
    "Overloading", "Tire burst", "Brake failure", "Road rage", "Animal crossing",
    "Sleep deprivation", "Bad lighting", "Using phone while driving"
]

ROAD_TYPES = ["National Highway", "State Highway", "City Road", "Rural Road", "Residential Street"]
LIGHT_CONDITIONS = ["Daylight", "Twilight", "Darkness (Lit)", "Darkness (Unlit)"]

def generate_upgraded_dataset():
    records = []
    start_date = datetime(YEAR, 1, 1)
    end_date = datetime(YEAR, 12, 31)
    delta_days = (end_date - start_date).days

    for i in range(1, NUM_RECORDS + 1):
        # 1. Date and Time logic
        random_days = random.randint(0, delta_days)
        accident_date = start_date + timedelta(days=random_days)
        month = accident_date.month
        day_of_week = accident_date.strftime("%A")

        # Rush hour weights (24 hours)
        # 0-5 (1), 6-7 (2,3), 8-9 (8,8), 10-13 (4,4,4,4), 14-17 (10,10,10,10), 18-21 (6,6,4,2), 22-23 (1,1)
        hour_weights = [1]*6 + [2,3] + [8,8] + [4]*4 + [10]*4 + [6,6,4,2] + [1,1]
        # Weighted hour favoring daytime and evening rush
        hour = random.choices(range(24), weights=hour_weights, k=1)[0]
        minute = random.randint(0, 59)
        accident_time = f"{hour:02d}:{minute:02d}"

        # 2. Location logic
        loc_name, base_lat, base_lng, region = random.choice(LOCATIONS)
        lat = round(base_lat + random.uniform(-0.015, 0.015), 6)
        lng = round(base_lng + random.uniform(-0.015, 0.015), 6)

        # 3. Vehicle Type Weighting
        vehicle_type = random.choices(VEHICLE_TYPES, weights=VEHICLE_WEIGHTS, k=1)[0]

        # 4. Weather logic (Correlated with Month and Region)
        if month in [6, 7, 8, 9]: # Monsoon
            weather_weights = [15, 60, 5, 10, 5, 5, 0]
        elif month in [11, 12, 1]: # Winter
            if region == "North":
                weather_weights = [30, 5, 50, 10, 0, 5, 0] # High fog in North
            else:
                weather_weights = [60, 5, 10, 20, 0, 5, 0]
        elif month in [4, 5]: # Summer
            weather_weights = [65, 0, 0, 10, 5, 5, 15]
        else:
            weather_weights = [70, 5, 5, 10, 5, 5, 0]
        weather = random.choices(WEATHER_CONDITIONS, weights=weather_weights, k=1)[0]

        # 5. Road and Light logic
        road_type = random.choices(ROAD_TYPES, weights=[20, 15, 40, 15, 10], k=1)[0]
        if 6 <= hour <= 17:
            light = "Daylight"
        elif hour in [5, 18, 19]:
            light = "Twilight"
        else:
            light = random.choices(["Darkness (Lit)", "Darkness (Unlit)"], weights=[70, 30], k=1)[0]

        # 6. Severity and Cause correlation
        # Higher speed causes on highways lead to more fatal/major accidents
        if road_type in ["National Highway", "State Highway"]:
            severity_weights = [0.25, 0.45, 0.30]
            cause = random.choices(CAUSES, weights=[30, 10, 5, 10, 10, 5, 5, 2, 5, 5, 5, 3, 2, 1, 1, 1, 0, 0], k=1)[0]
        else:
            severity_weights = [0.05, 0.30, 0.65]
            cause = random.choice(CAUSES)
            
        # Nighttime drunk driving
        if hour >= 22 or hour <= 4:
            if random.random() < 0.3:
                cause = "Drunk driving"
                severity_weights = [0.30, 0.50, 0.20]

        severity = random.choices(SEVERITY_LEVELS, weights=severity_weights, k=1)[0]

        # 7. Injuries and Fatalities based on severity
        if severity == "Fatal":
            injuries = random.randint(1, 12)
            fatalities = random.randint(1, 6)
        elif severity == "Major":
            injuries = random.randint(1, 8)
            fatalities = random.choices([0, 1], weights=[85, 15], k=1)[0]
        else:
            injuries = random.randint(0, 4)
            fatalities = 0

        # 8. Driver Age logic
        # Older drivers slightly more in cars, younger on motorcycles
        if vehicle_type in ["Motorcycle", "Scooter"]:
            driver_age = int(random.gauss(26, 8))
        else:
            driver_age = int(random.gauss(38, 12))
            
        driver_age = max(18, min(85, driver_age))
        
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
            "Lat": lat, # Shortened for CSV
            "Lng": lng,
            "Region": region,
            "Vehicle_Type": vehicle_type,
            "Weather": weather,
            "Road_Type": road_type,
            "Light_Condition": light,
            "Severity": severity,
            "Cause": cause,
            "Injuries": injuries,
            "Fatalities": fatalities,
            "Driver_Age": driver_age,
            "Age_Group": age_group
        })

    return records

def main():
    records = generate_upgraded_dataset()
    output_file = "upgraded_indian_accident_data_2025.csv"
    fieldnames = list(records[0].keys())

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Successfully generated {len(records)} upgraded records for year 2025.")
    print(f"Saved to: {output_file}")
    
    # Also update the main sample file for the website to use it immediately
    # We must ensure we don't break the frontend/backend expectations.
    # The existing code expects "Latitude" and "Longitude" (full names) and maybe specific ordering.
    # Let's map Lat/Lng back to Latitude/Longitude for compatibility.
    
    for r in records:
        r["Latitude"] = r.pop("Lat")
        r["Longitude"] = r.pop("Lng")
        
    compat_fieldnames = [
        "ID", "Date", "Time", "Location", "Latitude", "Longitude",
        "Vehicle_Type", "Weather", "Severity", "Cause", "Injuries", "Fatalities",
        "Driver_Age", "Age_Group", "Road_Type", "Light_Condition", "Region"
    ]
    
    with open("sample_accident_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=compat_fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"Updated sample_accident_data.csv with the upgraded dataset.")

if __name__ == "__main__":
    main()
