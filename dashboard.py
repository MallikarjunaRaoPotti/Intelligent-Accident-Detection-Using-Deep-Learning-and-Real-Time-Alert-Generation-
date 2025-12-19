from flask import Flask, render_template, send_from_directory
import csv
import os

app = Flask(__name__)

IMAGE_FOLDER = "accident_images"


@app.route("/")
def dashboard():
    accidents = []

    if os.path.exists("accident_log.csv"):
        with open("accident_log.csv", "r") as file:
            reader = csv.DictReader(file)
            accidents = list(reader)[::-1]  # latest first

    return render_template("dashboard.html", accidents=accidents)


@app.route("/images/<filename>")
def images(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
