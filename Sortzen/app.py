from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from organizer import organize_files
import os
import uuid
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/organize", methods=["POST"])
def organize():

    job_id = str(uuid.uuid4())

    source_folder = os.path.join(UPLOAD_FOLDER, job_id)
    result_folder = os.path.join(RESULT_FOLDER, job_id)

    os.makedirs(source_folder, exist_ok=True)

    uploaded_files = request.files.getlist("files")

    total_files = 0

    for file in uploaded_files:

        if file and file.filename:

            filename = secure_filename(file.filename)

            if filename:
                file.save(os.path.join(source_folder, filename))
                total_files += 1

    if total_files == 0:
        return render_template(
            "index.html",
            message="Please select valid files."
        )

    shutil.copytree(source_folder, result_folder)

    organized_count = organize_files(result_folder)

    zip_path = shutil.make_archive(result_folder, "zip", result_folder)

    return render_template(
        "index.html",
        total_files=total_files,
        organized_files=organized_count,
        categories=len([
            name for name in os.listdir(result_folder)
            if os.path.isdir(os.path.join(result_folder, name))
        ]),
        message="Files organized successfully!",
        download_url=f"/download/{job_id}"
    )


@app.route("/download/<job_id>")
def download(job_id):

    zip_path = os.path.join(RESULT_FOLDER, job_id + ".zip")

    if os.path.exists(zip_path):
        return send_file(
            zip_path,
            as_attachment=True,
            download_name="SORTZEN_Organized_Files.zip"
        )

    return "Download file not found!", 404


if __name__ == "__main__":
    app.run(debug=True)