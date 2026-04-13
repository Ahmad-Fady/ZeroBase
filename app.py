from flask import Flask, jsonify, render_template, request

import db_manager

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/learn")
def learn():
    return render_template("earning.html")


@app.route("/internships")
def internships():
    return render_template("internships.html")


@app.route("/jobs")
def jobs():
    return render_template("jobs.html")


@app.route("/api/data", methods=["GET"])
@app.route("/data", methods=["GET"])
def data_index():
    try:
        results = db_manager.get_all_data()
        return jsonify(results)
    except Exception:
        # Keep frontend usable when DB is unavailable.
        return jsonify([])


@app.route("/api/data", methods=["POST"])
@app.route("/data", methods=["POST"])
def data_create():
    content = (request.json or {}).get("content", "")
    if not content:
        return jsonify({"message": "Missing content"}), 400

    try:
        db_manager.add_entry(content)
        return jsonify({"message": "Saved!"}), 201
    except Exception:
        return jsonify({"message": "Database unavailable"}), 503


if __name__ == "__main__":
    app.run(debug=True)
