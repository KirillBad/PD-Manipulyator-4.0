import os
import uuid

from flask import Response, jsonify, render_template, request, send_from_directory

from app import app

from .object_detection import object_detection_handler

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def uid():
    return str(uuid.uuid4())


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def index():
    app.logger.info(
        f"{request.user_agent.string} got home page from {request.remote_addr}"
    )
    return render_template("index.html")


@app.route("/about")
def about():
    app.logger.info(
        f"{request.user_agent.string} got about page from {request.remote_addr}"
    )
    return render_template("about.html")


@app.route("/object-detection", methods=["POST", "GET"])
def object_detection():
    content_type = request.form.get("content")
    model = request.form.get("model")
    file = request.files.get("file")

    if content_type == "image":
        app.logger.info(
            f"{request.user_agent.string} {request.remote_addr} started image processing"
        )
        return jsonify(object_detection_handler.handle_image(model, file))
    elif content_type == "video":
        app.logger.info(
            f"{request.user_agent.string} {request.remote_addr} started video processing"
        )
        input_path, filename = object_detection_handler.save_file(file)
        return jsonify({"video_id": filename, "model": model, "content_type": "video"})
    elif content_type == "camera":
        app.logger.info(
            f"{request.user_agent.string} {request.remote_addr} started camera processing"
        )
        return jsonify({"video_id": 0, "model": model, "content_type": "camera"})


@app.route("/video_feed/<video_id>")
def video_feed(video_id):
    def generate():
        return object_detection_handler.process_video(
            video_id, request.args.get("model"), request.args.get("content_type")
        )

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/media/output/<path:filename>")
def media_files(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "media/output"), filename
    )
