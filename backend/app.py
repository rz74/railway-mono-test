from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import tempfile
import uuid

from utils.build_site import build_puzzle_site
from utils.path_config import STATIC_DIR
from static_handlers import (
    serve_key,
    serve_index_map,
    serve_obfuscation_map,
    serve_target,
    serve_mode,
)

# === Setup app and temp storage ===
app = Flask(__name__)
CORS(app)

ZIP_STORAGE = {}  # zip_id -> zip path

# === Routes ===

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/get-key", methods=["GET"])
def serve_key_route():
    return serve_key()

@app.route("/get-index-map", methods=["GET"])
def serve_index_map_route():
    return serve_index_map()

@app.route("/get-obfuscation-map", methods=["GET"])
def serve_obfuscation_map_route():
    return serve_obfuscation_map()

@app.route("/get-target", methods=["GET"])
def serve_target_route():
    return serve_target()

@app.route("/get-delivery-mode", methods=["GET"])
def serve_mode_route():
    return serve_mode()

@app.route("/generate-site", methods=["POST"])
def generate_site():
    try:
        form = request.form
        files = request.files

        filenames = form.getlist("filenames[]")
        indices = list(map(int, form.getlist("indices[]")))
        target_url = form.get("targetUrl")
        delivery_mode = form.get("deliveryMode")
        title = form.get("title", "Secret Puzzle")
        fail_message = form.get("failMessage", "Wrong again? Try harder!")
        netlify_token = form.get("token")

        if not (5 <= len(filenames) <= 50) or not (5 <= len(indices) <= 50):
            return jsonify({"error": "Expected 5 to 50 filenames and indices"}), 400
        if not target_url:
            return jsonify({"error": "Missing target URL"}), 400
        if not delivery_mode:
            return jsonify({"error": "Missing delivery mode"}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            image_paths = []
            for i in range(len(filenames)):
                f = files.get(f"image{i}")
                if not f:
                    return jsonify({"error": f"Missing image{i}"}), 400
                save_path = os.path.join(tmpdir, f"{i}_{f.filename}")
                f.save(save_path)
                image_paths.append(save_path)

            site_path = build_puzzle_site(
                image_paths=image_paths,
                labels=filenames,
                indices=indices,
                target_url=target_url,
                delivery_mode=delivery_mode,
                output_dir=tmpdir,
                title=title,
                fail_message=fail_message
            )

            zip_id = str(uuid.uuid4())[:8]
            final_zip_path = os.path.join(tempfile.gettempdir(), f"puzzle_{zip_id}.zip")
            os.rename(zip_path, final_zip_path)
            ZIP_STORAGE[zip_id] = final_zip_path

            # Skip Netlify deploy
    site_id = os.path.basename(site_path)
    base_url = request.host_url.rstrip("/")
    site_url = f"{base_url}/sites/{site_id}/"
    return jsonify({"url": site_url})

    # if netlify_token:
                print("🚀 Deploying to Netlify...")
                site_url = upload_zip_to_netlify(final_zip_path, netlify_token)
                print(f"✅ Site deployed: {site_url}")
                return jsonify({
                    "url": site_url,
                    "zip_id": zip_id
                })
            else:
                return jsonify({
                    "zip_id": zip_id
                })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/download-site/<zip_id>", methods=["GET"])
def download_site(zip_id):
    path = ZIP_STORAGE.get(zip_id)
    if not path or not os.path.exists(path):
        return jsonify({"error": "ZIP file not found or expired."}), 404
    return send_file(path, as_attachment=True, download_name="puzzle_site.zip")


# === Frontend static routes ===
@app.route('/<path:path>', methods=["GET"])
def serve_frontend_file(path):
    return send_from_directory(os.path.join(app.root_path, "static"), path)

@app.route("/", methods=["GET"])
def root():
    return send_from_directory(os.path.join(app.root_path, "static"), "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


@app.route("/sites/<site_id>/<path:filename>")
def serve_puzzle_file(site_id, filename):
    site_dir = os.path.join("/tmp/generated_sites", site_id)
    return send_from_directory(site_dir, filename)

@app.route("/sites/<site_id>/")
def serve_puzzle_index(site_id):
    site_dir = os.path.join("/tmp/generated_sites", site_id)
    return send_from_directory(site_dir, "index.html")
