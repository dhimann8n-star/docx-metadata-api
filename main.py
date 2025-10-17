from flask import Flask, request, jsonify
from docx import Document
import base64, tempfile, os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "DOCX Metadata Extraction API",
        "endpoint": "/extract_metadata",
        "method": "POST",
        "body_format": {"file": "base64_encoded_docx_data"}
    })

@app.route('/extract_metadata', methods=['POST'])
def extract_metadata():
    try:
        data = request.get_json()
        if not data or 'file' not in data:
            return jsonify({"error": "No file data received"}), 400

        binary = base64.b64decode(data['file'])
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name

        with open(temp_path, "wb") as f:
            f.write(binary)

        try:
            doc = Document(temp_path)
            props = doc.core_properties
            author = props.author or "Unknown"
            last_mod = props.last_modified_by or "Unknown"
            return jsonify({"Author": author, "LastSavedBy": last_mod})
        except Exception:
            return jsonify({"error": "Invalid DOCX file"}), 400
        finally:
            os.remove(temp_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

