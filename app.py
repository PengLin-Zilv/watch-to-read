import os
from flask import Flask, request, jsonify, send_file, render_template
from services.youtube import get_transcript
from services.claude import process_transcript
from services.ebook import generate_pdf

app = Flask(__name__)
OUTPUT_DIR = "outputs"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    url = data.get("url", "").strip()
    difficulty = data.get("difficulty", "beginner").strip()

    if not url:
        return jsonify({"error": "YouTube URL is required"}), 400

    # Step 1: Get transcript
    try:
        transcript = get_transcript(url)
    except Exception as e:
        return jsonify({"error": f"Failed to get transcript: {str(e)}"}), 400

    # Step 2: Process with Claude
    try:
        content = process_transcript(transcript, difficulty)
    except Exception as e:
        return jsonify({"error": f"Failed to process with AI: {str(e)}"}), 500

    # Step 3: Generate PDF
    try:
        filename = content["title"].replace(" ", "_")[:50] + ".pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)
        generate_pdf(content, output_path)
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

    return send_file(output_path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(debug=True)