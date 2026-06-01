// Mock accident data for the React dashboard
const LOCATIONS = [
    { name: "MG Road", lat: 12.9716, lng: 77.5946 },
    { name: "Connaught Place", lat: 28.6315, lng: 77.2167 },
    { name: "Marine Drive", lat: 18.9438, lng: 72.8232 },
    { name: "Anna Salai", lat: 13.0604, lng: 80.2496 },
    { name: "Park Street", lat: 22.5530, lng: 88.3512 },
    { name: "Banjara Hills", lat: 17.4122, lng: 78.4350 },
    { name: "FC Road", lat: 18.5255, lng: 73.8409 },
    { name: "Brigade Road", lat: 12.9719, lng: 77.6074 },
    { name: "Outer Ring Road", lat: 12.9352, lng: 77.6245 },
    { name: "Electronic City", lat: 12.8399, lng: 77.6770 },
    { name: "Silk Board Junction", lat: 12.9172, lng: 77.6227 },
    { name: "Hebbal Flyover", lat: 13.0358, lng: 77.5970 },
    { name: "Bellandur Gate", lat: 12.9255, lng: 77.6760 },
    { name: "Sarjapur Road", lat: 12.9100, lng: 77.6850 },
    { name: "Whitefield Road", lat: 12.9698, lng: 77.7500 },
];

const VEHICLE_TYPES = ["Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw", "Bicycle", "Pedestrian", "Van", "SUV", "Scooter"];
const WEATHER = ["Clear", "Rainy", "Foggy", "Cloudy", "Stormy", "Windy"];
const SEVERITIES = ["Fatal", "Major", "Minor"];
const CAUSES = ["Over-speeding", "Drunk driving", "Signal violation", "Wrong-side driving", "Distracted driving", "Poor road condition", "Vehicle malfunction", "Pedestrian error", "Tailgating", "Brake failure"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function seededRandom(seed) {
    let s = seed;
    return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}

function generateMockData(count = 500) {
    const rng = seededRandom(42);
    const pick = arr => arr[Math.floor(rng() * arr.length)];
    const records = [];

    for (let i = 0; i < count; i++) {
        const loc = pick(LOCATIONS);
        const sev = rng() < 0.08 ? "Fatal" : rng() < 0.38 ? "Major" : "Minor";
        const year = 2022 + Math.floor(rng() * 3);
        const month = Math.floor(rng() * 12);
        const day = 1 + Math.floor(rng() * 28);
        const hour = Math.floor(rng() * 24);

        records.push({
            id: i + 1,
            date: `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
            time: `${String(hour).padStart(2, '0')}:${String(Math.floor(rng() * 60)).padStart(2, '0')}`,
            location: loc.name, lat: loc.lat + (rng() - 0.5) * 0.02, lng: loc.lng + (rng() - 0.5) * 0.02,
            vehicleType: pick(VEHICLE_TYPES), weather: pick(WEATHER),
            severity: sev, cause: pick(CAUSES),
            injuries: sev === "Fatal" ? 1 + Math.floor(rng() * 8) : sev === "Major" ? 1 + Math.floor(rng() * 5) : Math.floor(rng() * 2),
            fatalities: sev === "Fatal" ? 1 + Math.floor(rng() * 3) : 0,
            year, month: MONTHS[month], monthIdx: month, hour,
        });
    }
    return records;
}

// Pre-computed aggregations
const MOCK_DATA = generateMockData(500);

function computeStats(data) {
    const total = data.length;
    const fatal = data.filter(d => d.severity === "Fatal").length;
    const major = data.filter(d => d.severity === "Major").length;
    const minor = data.filter(d => d.severity === "Minor").length;
    const totalFatalities = data.reduce((s, d) => s + d.fatalities, 0);

    // Location counts
    const locCounts = {};
    data.forEach(d => { locCounts[d.location] = (locCounts[d.location] || 0) + 1; });
    const byLocation = Object.entries(locCounts).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count);

    // Monthly trend
    const monthCounts = {};
    data.forEach(d => { const key = `${d.year}-${d.month}`; monthCounts[key] = (monthCounts[key] || 0) + 1; });
    const byMonth = Object.entries(monthCounts).map(([name, count]) => ({ name, count })).sort((a, b) => a.name.localeCompare(b.name));

    // Severity distribution
    const bySeverity = [
        { name: "Fatal", value: fatal, fill: "#ff4757" },
        { name: "Major", value: major, fill: "#ffa502" },
        { name: "Minor", value: minor, fill: "#2ed573" },
    ];

    // Hourly
    const hourCounts = Array(24).fill(0);
    data.forEach(d => { hourCounts[d.hour]++; });
    const byHour = hourCounts.map((count, h) => ({ name: `${h}:00`, count }));

    // By weather
    const weatherCounts = {};
    data.forEach(d => { weatherCounts[d.weather] = (weatherCounts[d.weather] || 0) + 1; });
    const byWeather = Object.entries(weatherCounts).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count);

    // By cause
    const causeCounts = {};
    data.forEach(d => { causeCounts[d.cause] = (causeCounts[d.cause] || 0) + 1; });
    const byCause = Object.entries(causeCounts).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count).slice(0, 10);

    // By vehicle
    const vehicleCounts = {};
    data.forEach(d => { vehicleCounts[d.vehicleType] = (vehicleCounts[d.vehicleType] || 0) + 1; });
    const byVehicle = Object.entries(vehicleCounts).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count);

    // Peak hour
    const peakHour = hourCounts.indexOf(Math.max(...hourCounts));
    const mostDangerous = byLocation[0]?.name || "N/A";

    return { total, fatal, major, minor, totalFatalities, byLocation, byMonth, bySeverity, byHour, byWeather, byCause, byVehicle, peakHour, mostDangerous };
}
