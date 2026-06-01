"""
Swagger/OpenAPI configuration for the Traffic Accident Analysis API.
"""

SWAGGER_TEMPLATE = {
    "info": {
        "title": "Traffic Accident Analysis API",
        "description": "REST API for uploading, analyzing, and visualizing traffic accident data.",
        "version": "1.0.0",
        "contact": {
            "name": "Traffic Accident Analysis Team",
        },
    },
    "basePath": "/",
    "schemes": ["http"],
}

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}
