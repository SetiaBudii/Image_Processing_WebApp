import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import random

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")

########################## QUIZ #########################################
#route quiz
@app.route("/quiz")
@nocache
def quiz():
    return render_template('quiz.html')
    
#route quiz upload
@app.route("/quiz_upload", methods=["POST"])
@nocache
def quiz_upload():
    image_path = "static/img/img_now_quiz.jpg"  # Path to your imageresul
    image_size = image_processing.get_image_size(image_path)
    rgb_values = image_processing.get_all_rgb(image_path)
    total_index_rgb = len(rgb_values)
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now_quiz.jpg")
    copyfile("static/img/img_now_quiz.jpg", "static/img/img_normal_quiz.jpg")
    return render_template("quiz_uploaded.html", file_path="img/img_now_quiz.jpg",image_size=image_size,rgb=rgb_values, total_index_rgb=total_index_rgb)

#route generate pieces dari gambar
@app.route("/generate", methods=["POST"])
@nocache
def generate():
    img = Image.open("static/img/img_now_quiz.jpg")

    width, height = img.size

    num_rows = int(request.form['size'])
    num_cols = int(request.form['size'])
    piece_width = width // num_cols
    piece_height = height // num_rows

    for row in range(num_rows):
        for col in range(num_cols):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height

            piece = img.crop((left, upper, right, lower))
            piece.save(f'static/img/piece_{row}_{col}.jpg')

    piece_paths = [
        f'static/img/piece_{row}_{col}.jpg'
        for row in range(num_rows) for col in range(num_cols)
    ]
    return render_template("image_pieces.html", piece_paths=piece_paths, num_rows=num_rows)

#route generate pieces dari gambar
@app.route("/random_gambar", methods=["POST"])
@nocache
def random_gambar():
    img = Image.open("static/img/img_now_quiz.jpg")

    width, height = img.size

    num_rows = int(request.form['size-random'])
    num_cols = int(request.form['size-random'])
    piece_width = width // num_cols
    piece_height = height // num_rows

    for row in range(num_rows):
        for col in range(num_cols):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height

            piece = img.crop((left, upper, right, lower))
            piece.save(f'static/img/piece_random{row}_{col}.jpg')

    piece_paths = [
        f'static/img/piece_random{row}_{col}.jpg'
        for row in range(num_rows) for col in range(num_cols)
    ]

    image_coordinates = [(i, j) for i in range(num_rows) for j in range(num_rows)]

    # Acak urutan koordinat gambar
    random.shuffle(image_coordinates)

    return render_template("random_pieces.html", piece_paths=piece_paths, num_rows=num_rows,image_coordinates=image_coordinates)

@app.route("/about")
@nocache
def about():
    return render_template('about.html')

@app.route("/percobaan")
@nocache
def percobaan():
    return render_template('percobaan.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"])


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
