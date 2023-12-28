import base64
import json
import os

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from ocr import PaddleOCRHanler
from werkzeug.utils import secure_filename

paddle_ocr_handler = PaddleOCRHanler()
UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def register_router(flask_app: Flask):
    flask_app.add_url_rule("/ocr/", view_func=ocr_main, methods=["POST"])
    flask_app.add_url_rule(
        "/display/<path:filename>", view_func=display_image, methods=["GET"]
    )
    flask_app.add_url_rule("/", view_func=upload_form)
    flask_app.add_url_rule("/", view_func=upload_image, methods=["POST"])


def ocr_main():
    in_data = json.loads(request.get_data())
    img = in_data.get("image")
    if not img:
        abort(400, {"message": "image is required."})
    if not isinstance(img, str):
        abort(400, {"message": "image must be a string."})
    res = paddle_ocr_handler.get_ocr_text(img)
    ocr_res = json.dumps({"result": res}, ensure_ascii=False)
    return ocr_res


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_form():
    return render_template("upload.html")


def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    print(file.filename)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        flash("Image and ocr results displayed below")
        with open(
            os.path.join(current_app.config["UPLOAD_FOLDER"], filename), "rb"
        ) as f:
            bt = f.read()
        base64_bytes = base64.b64encode(bt)
        base64_string = base64_bytes.decode("utf-8")
        res = paddle_ocr_handler.get_ocr_text(base64_string)
        return render_template("upload.html", filename=filename, dict={"res": res})
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)
