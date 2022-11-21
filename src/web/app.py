from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import base64
import numpy as np
import cv2
import os

app = Flask(__name__)
jwt_token_cookie_name = "pymanotoken"
username_cookie_name = "pymanousername"
api_url = os.environ.get("API_URL", "127.0.0.1:5000")

def check_token() -> bool:
    """
    Check if the token exist and is valid
    """
    try:
        if not jwt_token_cookie_name in request.cookies:
            return False

        pymanotoken = request.cookies.get(jwt_token_cookie_name)
        r = requests.get(
            url="http://{url}/check-token".format(url=api_url),
            headers={"x-access-token": pymanotoken},
        )

        if r.status_code == 200:
            return True
        return False
    except:
        return False


def get_current_user_name() -> str:
    """
    Get the username of the current user
    """
    if not username_cookie_name in request.cookies:
        return ""
    return request.cookies.get(username_cookie_name)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]

        r = requests.post(
            url="http://{url}/login".format(url = api_url),
            json={"username": username, "password": password},
        )

        if r.status_code == 201:
            token = r.json()["token"]
            username = r.json()["username"]
            resp = make_response(redirect(url_for("canvas")))
            resp.set_cookie(jwt_token_cookie_name, token)
            resp.set_cookie(username_cookie_name, username)
            return resp
        msg = "Incorrect username/password"
    return render_template("index.html", msg=msg)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie(jwt_token_cookie_name)
    return resp


@app.route("/canvas", methods=["GET", "POST"])
def canvas():
    prediction = ""

    if request.method == "GET" or not "imageData" in request.form:
        if not check_token():
            return redirect(url_for("login"), 302)

    else:

        image_data = request.form["imageData"]

        # The canvas returns an image with a transparent background.
        # The model needs an image with white background.
        # So we modify the image so that it has a white background

        # Load the base64 img
        base64_data = image_data.split(",")[1]  # take only the data part of the string
        nparr = np.fromstring(
            base64.b64decode(base64_data), np.uint8
        )  # transform the base64 img to an array usable by cv2
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

        # Change transparent pixels to white
        alpha_channel = img[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 254, 255, cv2.THRESH_BINARY)
        color = img[:, :, :3]
        new_img = cv2.bitwise_not(cv2.bitwise_not(color, mask=mask))

        # Encode it back to base64
        _, buffer = cv2.imencode(".png", new_img)
        png_as_text = base64.b64encode(buffer)
        image_data = "data:image/png;base64," + png_as_text.decode("utf-8")

        # Send the image to the api
        pymanotoken = request.cookies.get(jwt_token_cookie_name)
        r = requests.post(
            url="http://{url}/predict".format(url=api_url),
            headers={"x-access-token": pymanotoken},
            json={"imageData": image_data},
        )

        if r.status_code == 401:
            return redirect(url_for("login"))

        if r.status_code == 200:
            prediction = r.text

    return render_template(
        "canvas.html", prediction=prediction, username=get_current_user_name()
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8000)
