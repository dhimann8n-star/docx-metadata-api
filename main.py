from flask import Flask, request, jsonify
from docx import Document
import base64
import io

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "method": "POST",
        "endpoint": "/extract_metadata",
        "message": "DOCX Metadata Extraction API",
        "body_format": {"file": "base64_encoded_docx_data"}
    })

@app.route('/extract_metadata', methods=['POST'])
def extract_metadata():
    try:
        data = request.get_json()
        if not data or "file" not in data:
            return jsonify({"error": "Missing 'file' key"}), 400

        # Decode base64 to bytes
        file_bytes = base64.b64decode(data["file"])
        doc = Document(io.BytesIO(file_bytes))

        # Extract metadata
        properties = doc.core_properties
        metadata = {
            "author": properties.author,
            "last_modified_by": properties.last_modified_by,
            "title": properties.title,
            "subject": properties.subject,
            "category": properties.category,
            "comments": properties.comments
        }

        return jsonify(metadata)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
