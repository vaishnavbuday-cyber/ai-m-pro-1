# Traffic Accident Analysis System

A comprehensive, data-driven system for analyzing, visualizing, and reporting on traffic accident data. The project features a full-stack React + Flask dashboard, a standalone Streamlit application for rapid data exploration, ML-powered severity prediction, and an HTML presentation deck.

## Project Structure

- `full_web_app/backend/`: Flask REST API with Swagger docs, ML prediction, and data processing.
- `full_web_app/frontend/`: React dashboard with Vite, dark/light theme, chart export, and loading skeletons.
- `streamlit_app/`: Standalone Streamlit app with interactive maps, charts, and prediction tab.
- `presentation/`: Static HTML/CSS presentation slides.
- `sample_accident_data.csv`: Sample mock dataset for testing and demonstration.
- `Dockerfile` + `docker-compose.yml`: One-command Docker deployment.
- `.github/workflows/ci.yml`: GitHub Actions CI/CD pipeline.

## Prerequisites

- **Python 3.8+** (with `pip` available in your PATH)
- **Node.js 18+** (with `npm` available in your PATH)
- **Docker** (optional, for containerized deployment)

## 🚀 Step-by-Step Guide: How to Run the Project Locally

Follow these instructions carefully to start the whole system from scratch. You will need to keep **two separate terminal windows open at the same time** (one for the backend, one for the frontend).

### Step 1: Start the Flask Backend Server (API)

The backend crunches the data, runs the machine learning predictions, and handles file uploads.

**Easiest Setup (Recommended for Windows):**
1. Open the project folder (`full_web_app` -> `backend` is located here).
2. Look for the file named `start_backend.bat` in the main project folder.
3. **Double-click** `start_backend.bat`.
4. A black terminal window will appear. It will automatically download dependencies and start the server. 
> ✅ **Wait until you see:** `Running on http://127.0.0.1:5000`
> ⚠️ **IMPORTANT:** DO NOT close this black window! Minimize it and leave it running in the background.

**Manual Setup:**
If the `.bat` file doesn't work, open PowerShell or Command Prompt, paste this, and press Enter:
```bash
cd "C:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\full_web_app\backend"
python -m pip install -r requirements.txt
python app.py
```

### Step 2: Start the React Frontend Dashboard (UI)

The frontend is the beautiful user interface where you view charts and graphs. You must start this in a *new* window.

1. Open a **Brand New** PowerShell or Command Prompt window.
2. Run the following commands:
```bash
cd "C:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\full_web_app\frontend"
npm install
npm run dev
```
> ✅ **Wait until you see:** `Local: http://localhost:5173/`
> ⚠️ **IMPORTANT:** DO NOT close this black window either!

### Step 3: Open the Dashboard in Your Browser

1. Open your web browser (Chrome, Edge, Firefox, etc.).
2. Go to this exact web address: **[http://localhost:5173](http://localhost:5173)**
3. You should now see the Traffic Accident Analysis System dashboard!

---

### Additional (Optional) Things to Run

**1. Streamlit Application (Alternative Interface)**
If you want to use the alternative Python-based Streamlit interface instead of the React one, open a third terminal and run:
```bash
cd "C:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\streamlit_app"
python -m pip install streamlit matplotlib seaborn folium streamlit-folium pandas numpy scikit-learn
python -m streamlit run app.py
```
*(The Streamlit app will automatically open in your browser)*

**2. View the Presentation Slides**
1. Open your File Explorer.
2. Go into the `presentation` folder.
3. Double-click the `index.html` file to view your presentation slides in the browser!

## 🐳 Docker Deployment (One Command)

If you have Docker installed, you can run the entire app with:
```bash
cd "C:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project"
docker-compose up --build
```
> ✅ The full app will be accessible at **http://localhost:5000**

## 🧪 Running Tests

```bash
cd "C:\Users\VAISHNAV\OneDrive\Desktop\project\sreekuttans project\full_web_app\backend"
python -m pip install -r requirements.txt
python -m pytest test_utils.py test_app.py -v
```

## Features

- **Secure Access (Gmail):** Modern login interface requiring `@gmail.com` authentication, complete with error handling and glassmorphism UI.
- **Data Upload:** Users can upload custom CSV/Excel datasets for real-time processing.
- **Analytics Dashboard:** Visualizations for accidents by severity, vehicle type, weather conditions, and more.
- **🔮 ML Prediction:** Predict accident severity based on conditions (hour, weather, location, vehicle, cause) using RandomForest.
- **Geospatial Mapping:** Interactive Folium-powered maps visualizing accident hotspots.
- **Reporting:** Auto-generated summaries and actionable insights exportable to CSV and TXT formats.
- **🌗 Dark/Light Theme:** Toggle between dark and light mode in the React dashboard.
- **📥 Chart Export:** Download any chart as a PNG image from the React dashboard.
- **📖 API Documentation:** Interactive Swagger docs at `/apidocs/` for all REST endpoints.
- **🐳 Docker Support:** One-command deployment with Docker Compose.
- **✅ CI/CD:** GitHub Actions workflow for automated testing on every push.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | Authenticate Gmail users |
| `POST` | `/upload` | Upload CSV/Excel file |
| `GET` | `/summary` | Get summary statistics |
| `GET` | `/analysis` | Get aggregated chart data |
| `GET` | `/charts` | Get combined summary + charts + insights |
| `POST` | `/predict` | Predict accident severity |
| `GET` | `/feature-importance` | Get ML feature rankings |
| `GET` | `/health` | Health check |
| `GET` | `/apidocs/` | Swagger API documentation |
