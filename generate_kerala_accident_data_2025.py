"""
Generate a realistic Kerala-specific traffic accident dataset for the year 2025.
All locations are real roads, highways, and urban spots in Kerala.
"""

import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(99)

# Configuration
NUM_RECORDS = 2000
YEAR = 2025

# ── Real Kerala Locations (Name, Latitude, Longitude, District) ──────────────
LOCATIONS = [
    # Thiruvananthapuram
    ("NH-66, Kazhakkoottam, Thiruvananthapuram",    8.5590,  76.8800, "Thiruvananthapuram"),
    ("Kesavadasapuram Junction, Thiruvananthapuram", 8.5290,  76.9417, "Thiruvananthapuram"),
    ("Peroorkada Junction, Thiruvananthapuram",      8.5462,  76.9270, "Thiruvananthapuram"),
    ("Attingal Bypass, Thiruvananthapuram",          8.6938,  76.8148, "Thiruvananthapuram"),
    ("Nemom, Thiruvananthapuram",                    8.4856,  76.9427, "Thiruvananthapuram"),
    ("Vellayambalam, Thiruvananthapuram",            8.5133,  76.9495, "Thiruvananthapuram"),

    # Kollam
    ("NH-66, Kundara, Kollam",                      8.9870,  76.6913, "Kollam"),
    ("Paravur Road, Kollam",                         8.7929,  76.6638, "Kollam"),
    ("Kottarakkara Junction, Kollam",                9.0005,  76.7768, "Kollam"),
    ("Karunagappally Road, Kollam",                  9.0533,  76.5336, "Kollam"),

    # Pathanamthitta
    ("Pandalam Road, Pathanamthitta",                9.2231,  76.6551, "Pathanamthitta"),
    ("Ranni Road, Pathanamthitta",                   9.3820,  76.7829, "Pathanamthitta"),

    # Alappuzha
    ("NH-66, Alappuzha Bypass",                      9.4981,  76.3388, "Alappuzha"),
    ("Cherthala Road, Alappuzha",                    9.6858,  76.3393, "Alappuzha"),
    ("Kuttanad Road, Alappuzha",                     9.3983,  76.4228, "Alappuzha"),

    # Kottayam
    ("MC Road, Kottayam",                            9.5895,  76.5218, "Kottayam"),
    ("Kottayam-Kumily Road (NH-183)",               9.5667,  76.8932, "Kottayam"),
    ("Changanacherry Bypass, Kottayam",              9.4411,  76.5426, "Kottayam"),

    # Idukki
    ("NH-85, Munnar Road, Idukki",                   9.9959,  77.0602, "Idukki"),
    ("Thekkady Road, Idukki",                        9.6000,  77.1600, "Idukki"),
    ("Kattappana Road, Idukki",                      9.7487,  77.1093, "Idukki"),

    # Ernakulam / Kochi
    ("NH-66, Edapally Junction, Kochi",             10.0259,  76.3088, "Ernakulam"),
    ("Marine Drive, Kochi",                          9.9760,  76.2757, "Ernakulam"),
    ("Seaport-Airport Road, Kochi",                 10.0273,  76.3538, "Ernakulam"),
    ("Vytilla Junction, Kochi",                      9.9571,  76.3159, "Ernakulam"),
    ("Perumbavoor Road, Ernakulam",                 10.1075,  76.4764, "Ernakulam"),
    ("Aluva Bypass, Ernakulam",                     10.1031,  76.3571, "Ernakulam"),
    ("Kakkanad, Kochi",                             10.0133,  76.3508, "Ernakulam"),

    # Thrissur
    ("NH-544, Thrissur Bypass",                     10.5276,  76.2144, "Thrissur"),
    ("Chalakudy Road, Thrissur",                    10.3015,  76.3339, "Thrissur"),
    ("Guruvayur Road, Thrissur",                    10.5948,  76.0447, "Thrissur"),
    ("Vadakkanchery Road, Thrissur",                10.5274,  76.5125, "Thrissur"),

    # Palakkad
    ("Palakkad-Coimbatore Highway (NH-544)",        10.7867,  76.6542, "Palakkad"),
    ("Kozhinjampara Road, Palakkad",                10.7250,  76.8432, "Palakkad"),
    ("Ottappalam Bypass, Palakkad",                 10.7750,  76.3785, "Palakkad"),

    # Malappuram
    ("Tirur Road, Malappuram",                      10.9108,  75.9217, "Malappuram"),
    ("NH-66, Kuttippuram, Malappuram",              10.8563,  75.9441, "Malappuram"),
    ("Manjeri Bypass, Malappuram",                  11.1205,  76.1208, "Malappuram"),
    ("Perinthalmanna Road, Malappuram",             10.9750,  76.2269, "Malappuram"),

    # Kozhikode
    ("NH-66, Kozhikode Bypass",                     11.2588,  75.7804, "Kozhikode"),
    ("Mavoor Road, Kozhikode",                      11.2564,  75.8133, "Kozhikode"),
    ("Feroke Junction, Kozhikode",                  11.1697,  75.8497, "Kozhikode"),
    ("Calicut Beach Road, Kozhikode",               11.2588,  75.7731, "Kozhikode"),

    # Wayanad
    ("Kalpetta-Mananthavady Road, Wayanad",         11.6065,  76.0842, "Wayanad"),
    ("Sultan Bathery Road, Wayanad",                11.6619,  76.2599, "Wayanad"),
    ("Vythiri Ghat Road, Wayanad",                  11.5280,  76.0494, "Wayanad"),

    # Kannur
    ("NH-66, Kannur Bypass",                        11.8745,  75.3704, "Kannur"),
    ("Thalassery Road, Kannur",                     11.7480,  75.4930, "Kannur"),
    ("Kannur-Mananthavady Road",                    11.8700,  75.6750, "Kannur"),

    # Kasaragod
    ("NH-66, Kasaragod Bypass",                     12.4996,  74.9869, "Kasaragod"),
    ("Kanhangad Road, Kasaragod",                   12.3574,  75.0960, "Kasaragod"),
]

VEHICLE_TYPES = [
    "Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw",
    "Bicycle", "Van", "SUV", "Scooter", "Tractor", "Lorry"
]
VEHICLE_WEIGHTS = [22, 32, 8, 10, 16, 2, 3, 3, 6, 2, 3]

WEATHER_CONDITIONS = [
    "Clear", "Rainy", "Foggy", "Cloudy", "Stormy", "Windy", "Heatwave"
]

SEVERITY_LEVELS = ["Fatal", "Major", "Minor"]

CAUSES = [
    "Over-speeding", "Drunk driving", "Signal violation", "Wrong-side driving",
    "Distracted driving", "Poor road condition", "Vehicle malfunction",
    "Pedestrian error", "Tailgating", "Lane changing without signal",
    "Overloading", "Tire burst", "Brake failure", "Road rage", "Animal crossing",
    "Sleep deprivation", "Bad lighting", "Using phone while driving"
]

ROAD_TYPES = ["National Highway", "State Highway", "City Road", "Rural Road", "Residential Street"]
LIGHT_CONDITIONS = ["Daylight", "Twilight", "Darkness (Lit)", "Darkness (Unlit)"]


def get_age_group(age):
    if age < 26:
        return "<26"
    elif age <= 40:
        return "26-40"
    elif age <= 60:
        return "41-60"
    else:
        return "60+"


def generate_kerala_dataset():
    records = []
    start_date = datetime(YEAR, 1, 1)
    end_date   = datetime(YEAR, 12, 31)
    delta_days = (end_date - start_date).days

    for i in range(1, NUM_RECORDS + 1):
        # ── Date & Time ──────────────────────────────────────────────────────
        random_days  = random.randint(0, delta_days)
        accident_date = start_date + timedelta(days=random_days)
        month        = accident_date.month

        # Rush-hour weighted time distribution (exactly 24 values: hours 0-23)
        # 0-4 (night): 5 values; 5-6 (early): 2; 7-8 (morning rush): 2; 9-12: 4; 13-16 (afternoon): 4; 17-20 (evening): 4; 21-23: 3
        hour_weights = [1, 1, 1, 1, 1, 2, 3, 8, 10, 5, 5, 5, 5, 10, 10, 10, 10, 8, 6, 4, 3, 2, 1, 1]
        hour   = random.choices(range(24), weights=hour_weights, k=1)[0]
        minute = random.randint(0, 59)
        accident_time = f"{hour:02d}:{minute:02d}"

        # ── Location ─────────────────────────────────────────────────────────
        loc_name, base_lat, base_lng, district = random.choice(LOCATIONS)
        lat = round(base_lat + random.uniform(-0.012, 0.012), 6)
        lng = round(base_lng + random.uniform(-0.012, 0.012), 6)

        # ── Vehicle ──────────────────────────────────────────────────────────
        vehicle_type = random.choices(VEHICLE_TYPES, weights=VEHICLE_WEIGHTS, k=1)[0]

        # ── Weather (Kerala-specific: heavy monsoon Jun-Sep) ─────────────────
        if month in [6, 7, 8, 9]:           # South-west monsoon
            weather_weights = [5, 70, 3, 12, 8, 2, 0]
        elif month in [10, 11]:             # North-east monsoon
            weather_weights = [20, 40, 5, 20, 10, 5, 0]
        elif month in [12, 1, 2]:           # Cool dry season
            weather_weights = [55, 5, 15, 20, 0, 5, 0]
        else:                               # Mar-May – hot & pre-monsoon
            weather_weights = [45, 5, 0, 15, 5, 10, 20]
        weather = random.choices(WEATHER_CONDITIONS, weights=weather_weights, k=1)[0]

        # ── Road & Light ─────────────────────────────────────────────────────
        road_type = random.choices(ROAD_TYPES, weights=[22, 18, 35, 15, 10], k=1)[0]
        if 6 <= hour <= 17:
            light = "Daylight"
        elif hour in [5, 18, 19]:
            light = "Twilight"
        else:
            light = random.choices(
                ["Darkness (Lit)", "Darkness (Unlit)"], weights=[65, 35], k=1
            )[0]

        # ── Severity & Cause ─────────────────────────────────────────────────
        if road_type in ["National Highway", "State Highway"]:
            severity_weights = [0.20, 0.43, 0.37]
            # weights must have exactly 18 entries — one for each item in CAUSES
            # Over-speeding, Drunk driving, Signal violation, Wrong-side driving,
            # Distracted driving, Poor road condition, Vehicle malfunction,
            # Pedestrian error, Tailgating, Lane changing without signal,
            # Overloading, Tire burst, Brake failure, Road rage, Animal crossing,
            # Sleep deprivation, Bad lighting, Using phone while driving
            cause = random.choices(
                CAUSES,
                weights=[30, 8, 4, 10, 10, 8, 4, 2, 6, 5, 4, 4, 2, 1, 1, 1, 1, 2],
                k=1
            )[0]
        else:
            severity_weights = [0.06, 0.32, 0.62]
            cause = random.choice(CAUSES)

        # Night-time drunk-driving bump
        if hour >= 22 or hour <= 4:
            if random.random() < 0.30:
                cause = "Drunk driving"
                severity_weights = [0.28, 0.50, 0.22]

        # Heavy rain visibility → lower severity on city roads slightly adjusted
        if weather in ["Rainy", "Stormy"] and road_type == "National Highway":
            severity_weights = [w * 1.2 for w in severity_weights]
            total = sum(severity_weights)
            severity_weights = [w / total for w in severity_weights]

        severity = random.choices(SEVERITY_LEVELS, weights=severity_weights, k=1)[0]

        # ── Injuries & Fatalities ─────────────────────────────────────────────
        if severity == "Fatal":
            injuries   = random.randint(1, 10)
            fatalities = random.randint(1, 5)
        elif severity == "Major":
            injuries   = random.randint(1, 7)
            fatalities = random.choices([0, 1], weights=[88, 12], k=1)[0]
        else:
            injuries   = random.randint(0, 3)
            fatalities = 0

        # ── Driver Age ────────────────────────────────────────────────────────
        if vehicle_type in ["Motorcycle", "Scooter"]:
            driver_age = int(random.gauss(26, 8))
        else:
            driver_age = int(random.gauss(37, 12))
        driver_age = max(18, min(80, driver_age))
        age_group  = get_age_group(driver_age)

        records.append({
            "ID":              20250000 + i,
            "Date":            accident_date.strftime("%Y-%m-%d"),
            "Time":            accident_time,
            "Location":        loc_name,
            "District":        district,
            "Lat":             lat,
            "Lng":             lng,
            "Region":          "South",         # Kerala is entirely in South region
            "Vehicle_Type":    vehicle_type,
            "Weather":         weather,
            "Road_Type":       road_type,
            "Light_Condition": light,
            "Severity":        severity,
            "Cause":           cause,
            "Injuries":        injuries,
            "Fatalities":      fatalities,
            "Driver_Age":      driver_age,
            "Age_Group":       age_group,
        })

    return records


def main():
    records = generate_kerala_dataset()

    # ── Save primary Kerala dataset ───────────────────────────────────────────
    output_file = "kerala_accident_data_2025.csv"
    fieldnames  = list(records[0].keys())

    with open(
        r"c:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\\" + output_file,
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"✅  Generated {len(records)} Kerala accident records → {output_file}")

    # ── Save a backend-compatible copy (sample_data.csv) ─────────────────────
    # Rename Lat/Lng to Latitude/Longitude and add District alongside Location
    compat_records = []
    for r in records:
        cr = dict(r)
        cr["Latitude"]  = cr.pop("Lat")
        cr["Longitude"] = cr.pop("Lng")
        compat_records.append(cr)

    compat_fieldnames = [
        "ID", "Date", "Time", "Location", "District",
        "Latitude", "Longitude", "Region",
        "Vehicle_Type", "Weather", "Severity", "Cause",
        "Injuries", "Fatalities", "Driver_Age", "Age_Group",
        "Road_Type", "Light_Condition"
    ]

    compat_file = r"c:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\sample_data.csv"
    with open(compat_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=compat_fieldnames)
        writer.writeheader()
        writer.writerows(compat_records)

    print(f"✅  Also saved backend-compatible copy → sample_data.csv")

    # ── Quick summary stats ───────────────────────────────────────────────────
    from collections import Counter
    severities  = Counter(r["Severity"]  for r in records)
    districts   = Counter(r["District"]  for r in records)
    top5_causes = Counter(r["Cause"]     for r in records).most_common(5)
    total_fatal = sum(r["Fatalities"] for r in records)
    total_inj   = sum(r["Injuries"]   for r in records)

    print("\n── Dataset Summary ─────────────────────────────────────────────────")
    print(f"  Total records  : {len(records)}")
    print(f"  Severity       : {dict(severities)}")
    print(f"  Total fatalities: {total_fatal}  |  Total injuries: {total_inj}")
    print(f"  Top 5 causes   : {top5_causes}")
    print(f"  Districts      : {dict(districts.most_common(5))} (top 5)")


if __name__ == "__main__":
    main()
