"""
Flask Backend - Production-Ready Agentic AI Data Engineering System
"""
import os
import json
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from pathlib import Path

from config import get_config
from agents.ingestion_agent import IngestionAgent
from agents.governance_agent import GovernanceAgent
from agents.quality_agent import QualityAgent
from agents.orchestration_agent import OrchestrationAgent
from agents.insight_agent import InsightAgent

app = Flask(__name__)
config = get_config()
app.config.from_object(config)
CORS(app)

api_key = os.getenv("ANTHROPIC_API_KEY")
ingestion_agent = IngestionAgent(api_key)
governance_agent = GovernanceAgent(api_key)
quality_agent = QualityAgent(api_key)
orchestration_agent = OrchestrationAgent(api_key)
insight_agent = InsightAgent(api_key)

current_data = {}
pipeline_metadata = {}

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": config.CURRENT_VERSION}), 200

@app.route("/api/system-info", methods=["GET"])
def system_info():
    return jsonify({
        "system": "Production-Ready Agentic AI Data Engineering System",
        "agents": ["Ingestion Agent", "Data Governance Agent", "Quality & Validation Agent", "Pipeline Orchestration Agent", "Insight & Reporting Agent"],
        "version": config.CURRENT_VERSION
    }), 200

@app.route("/api/ingest/csv", methods=["POST"])
def ingest_csv():
    data = request.json
    file_path = data.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400
    result = ingestion_agent.ingest_csv(file_path)
    if result["status"] == "success":
        current_data["last_ingestion"] = result
    return jsonify(result), 200

@app.route("/api/ingest/sample-data", methods=["GET"])
def get_sample_data():
    return jsonify({"orders": [{"order_id": 1001, "amount": 1200, "status": "PAID"}]}), 200

@app.route("/api/governance/validate-schema", methods=["POST"])
def validate_schema():
    data = request.json
    result = governance_agent.validate_schema(data.get("schema", {}), data.get("expected_schema", {}))
    return jsonify(result), 200

@app.route("/api/quality/validate", methods=["POST"])
def validate_quality():
    data = request.json
    if isinstance(data.get("data"), list):
        df = pd.DataFrame(data["data"])
        result = quality_agent.validate_data(df)
        return jsonify(result), 200
    return jsonify({"error": "Invalid data format"}), 400

@app.route("/api/orchestration/create-pipeline", methods=["POST"])
def create_pipeline():
    data = request.json
    result = orchestration_agent.create_pipeline(data.get("name", "default"), data.get("stages", []), data.get("dependencies", {}))
    return jsonify(result), 200

@app.route("/api/insights/generate", methods=["POST"])
def generate_insights():
    data = request.json
    if isinstance(data.get("data"), list):
        df = pd.DataFrame(data["data"])
        result = insight_agent.generate_insights(df, data.get("context", ""))
        return jsonify(result), 200
    return jsonify({"error": "Invalid data format"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
