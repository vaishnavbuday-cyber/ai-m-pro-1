"""
Traffic Accident Analysis System — Flask Backend
REST API server for data upload, analysis, chart data, and predictions.
"""

import os
import logging
from dotenv import load_dotenv
import pandas as pd
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from utils import preprocess_dataframe, compute_summary, compute_analysis, generate_insights
from swagger_config import SWAGGER_TEMPLATE, SWAGGER_CONFIG
from predictor import AccidentPredictor

# ─── Load environment config ───
load_dotenv()
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", 10))

# ─── Logging ───
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── App setup ───
app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024  # limit upload size

swagger = Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)

# In-memory dataframe store
_current_df = None
_preprocessing_stats = None
_predictor = AccidentPredictor()


def _get_df():
    """Return the current loaded dataframe, or load sample data."""
    global _current_df, _preprocessing_stats
    if _current_df is not None:
        return _current_df

    # Try loading sample data from the project root
    sample_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "sample_accident_data.csv",
    )
    if os.path.exists(sample_path):
        logger.info("Loading sample data from %s", sample_path)
        df = pd.read_csv(sample_path)
        _current_df, _preprocessing_stats = preprocess_dataframe(df)
        return _current_df
    return None


# ─── Error handlers ───

@app.errorhandler(413)
def file_too_large(e):
    """Handle file size exceeding the limit."""
    logger.warning("Upload rejected — file exceeds %d MB limit", MAX_UPLOAD_MB)
    return jsonify({"error": f"File too large. Maximum allowed size is {MAX_UPLOAD_MB} MB."}), 413


@app.errorhandler(500)
def internal_error(e):
    """Handle unexpected server errors."""
    logger.exception("Internal server error")
    return jsonify({"error": "Internal server error. Please try again later."}), 500


# ─── Endpoints ───

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user with Gmail account.
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email: {type: string, example: "admin@gmail.com"}
            password: {type: string, example: "password"}
    responses:
      200:
        description: Successfully logged in
      401:
        description: Unauthorized
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Professional Gmail regex validation
    # Allows letters, numbers, dots, 6-30 chars before @gmail.com
    gmail_regex = r'^[a-z0-9](\.?[a-z0-9]){5,}@gmail\.com$'
    if not re.match(gmail_regex, email):
        return jsonify({"error": "Please enter a valid Gmail address (e.g., name@gmail.com)"}), 401

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 401

    logger.info("Successful login for %s", email)
    return jsonify({
        "message": "Login successful",
        "user": {"email": email}
    })

@app.route("/upload", methods=["POST"])
def upload_data():
    """Upload a CSV or Excel file and return a preview.
    ---
    tags:
      - Data
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: CSV or Excel file to upload
    responses:
      200:
        description: File uploaded successfully with preview data
      400:
        description: Bad request — no file, unsupported format, or unreadable file
      413:
        description: File too large
    """
    global _current_df, _preprocessing_stats

    if "file" not in request.files:
        logger.warning("Upload attempt with no file attached")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        logger.warning("Upload attempt with empty filename")
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename.lower()
    logger.info("Received upload: %s", file.filename)

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            logger.warning("Unsupported file format: %s", filename)
            return jsonify({"error": "Unsupported file format. Use CSV or Excel."}), 400
    except Exception as e:
        logger.error("Failed to read uploaded file: %s", str(e))
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    if df.empty:
        logger.warning("Uploaded file is empty: %s", file.filename)
        return jsonify({"error": "The uploaded file contains no data."}), 400

    _current_df, _preprocessing_stats = preprocess_dataframe(df)
    logger.info("Processed %d records from %s", len(_current_df), file.filename)

    # Auto-train the predictor
    if _predictor.train(_current_df):
        logger.info("Predictor trained successfully (accuracy: %s)", _predictor.accuracy)
    else:
        logger.warning("Predictor training skipped — insufficient features or data")

    # Return preview (first 10 rows) and column names
    preview = _current_df.head(10).fillna("").to_dict(orient="records")
    # Convert Timestamps to strings for JSON serialization
    for row in preview:
        for key, val in row.items():
            if isinstance(val, pd.Timestamp):
                row[key] = val.strftime("%Y-%m-%d")

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename,
        "rows": len(_current_df),
        "columns": list(_current_df.columns),
        "preview": preview,
        "preprocessing": _preprocessing_stats,
    })


@app.route("/summary", methods=["GET"])
def get_summary():
    """Return summary statistics for the loaded dataset.
    ---
    tags:
      - Analysis
    responses:
      200:
        description: Summary statistics including totals, severity counts, insights
      400:
        description: No data loaded
    """
    df = _get_df()
    if df is None:
        return jsonify({"error": "No data loaded. Upload a file first."}), 400

    logger.info("Serving summary for %d records", len(df))
    summary = compute_summary(df)
    insights = generate_insights(df)
    summary["insights"] = insights
    if _preprocessing_stats:
        summary["preprocessing"] = _preprocessing_stats
    return jsonify(summary)


@app.route("/analysis", methods=["GET"])
def get_analysis():
    """Return aggregated analysis data for charts.
    ---
    tags:
      - Analysis
    responses:
      200:
        description: Aggregated chart data (by location, month, severity, hour, weather, cause, vehicle)
      400:
        description: No data loaded
    """
    df = _get_df()
    if df is None:
        return jsonify({"error": "No data loaded. Upload a file first."}), 400

    logger.info("Serving analysis for %d records", len(df))
    
    # Get custom age breaks from query params (if provided)
    # Expected format: ?age1=25&age2=40&age3=60
    try:
        age1 = int(request.args.get("age1", 25))
        age2 = int(request.args.get("age2", 40))
        age3 = int(request.args.get("age3", 60))
        age_breaks = [age1, age2, age3]
    except ValueError:
        age_breaks = [25, 40, 60]

    analysis = compute_analysis(df, age_breaks)
    return jsonify(analysis)


@app.route("/charts", methods=["GET"])
def get_charts():
    """Return combined chart-ready data (summary + analysis + insights).
    ---
    tags:
      - Analysis
    responses:
      200:
        description: Combined summary, chart data, and insights
      400:
        description: No data loaded
    """
    df = _get_df()
    if df is None:
        return jsonify({"error": "No data loaded. Upload a file first."}), 400

    logger.info("Serving charts for %d records", len(df))
    summary = compute_summary(df)
    analysis = compute_analysis(df)
    insights = generate_insights(df)

    return jsonify({
        "summary": summary,
        "charts": analysis,
        "insights": insights,
    })


@app.route("/predict", methods=["POST"])
def predict():
    """Predict accident severity based on input features.
    ---
    tags:
      - Prediction
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Hour: {type: integer, example: 14}
            Weather: {type: string, example: "Rainy"}
            Location: {type: string, example: "Highway A1"}
            Vehicle_Type: {type: string, example: "Car"}
            Cause: {type: string, example: "Speeding"}
    responses:
      200:
        description: Predicted severity with confidence
      400:
        description: Missing features or model not trained
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON with feature values."}), 400

    logger.info("Prediction request with features: %s", list(data.keys()))
    result = _predictor.predict(data)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@app.route("/feature-importance", methods=["GET"])
def feature_importance():
    """Return ranked feature importance from the trained model.
    ---
    tags:
      - Prediction
    responses:
      200:
        description: Feature importance rankings and model accuracy
      400:
        description: Model not trained
    """
    result = _predictor.get_feature_importance()
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint.
    ---
    tags:
      - System
    responses:
      200:
        description: Server status and data load state
    """
    df = _get_df()
    logger.info("Health check — data loaded: %s", df is not None)
    return jsonify({
        "status": "ok",
        "dataLoaded": df is not None,
        "recordCount": len(df) if df is not None else 0,
    })


if __name__ == "__main__":
    print("=" * 60)
    print("  Traffic Accident Analysis System — Backend Server")
    print(f"  Running on http://localhost:{FLASK_PORT}")
    print(f"  Swagger docs at http://localhost:{FLASK_PORT}/apidocs/")
    print("=" * 60)
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT)
