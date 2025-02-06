from flask import Flask, session, request, render_template, redirect
from PIL import Image
from stroke import image_to_stroke
import uuid
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = load_dotenv()

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html",
                               一時保存パス = session.get("一時保存パス"),
                               元の名前 = session.get("元の名前"))
    elif request.method == "POST":

        画像ファイル = request.files["uploaded_image"]
        元の画像 = Image.open(画像ファイル.stream)

        元のファイル名 = 画像ファイル.filename

        一時保存用ディレクトリ = f"static/images/{uuid.uuid4()}"
        os.makedirs(一時保存用ディレクトリ)

        一時保存パス = f"{一時保存用ディレクトリ}/outline.svg"

        image_to_stroke(元の画像, 一時保存パス)

        session["一時保存パス"] = 一時保存パス
        session["元の名前"] = 元のファイル名

        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)