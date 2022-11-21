from flask import Flask, request, jsonify, make_response
from modules.crnn_word_predicter import CRNNWordPredicter
import base64
import cv2
import numpy as np
import jwt
import modules.authentication_helper as ah
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
predicter = CRNNWordPredicter()
app.config["SECRET_KEY"] = "cc0c61fdcff911f4fb0e4346d4556bbbc0914097294aa0c0"

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        error = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            error = "Token is missing"
        else:
            try:
                data = jwt.decode(
                    token,
                    app.config["SECRET_KEY"],
                    algorithms=[
                        "HS256",
                    ],
                )
                current_user = ah.get_user(data["public_id"])
                if not current_user:
                    error = "Token is invalid"
            except:
                error = "Token is invalid"
        if error:
            return jsonify({"message": error}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
def check_status():
    """Checks if the API is running"""
    return {"data": "API is running"}


@app.route("/check-token", methods=["GET"])
@token_required
def check_token():
    """Empty method called by the web app to check if the token is valid
    It is mainly called before displaying a page that needs authentication
    """
    return {"data": "Token is valid"}


@app.route("/login", methods=["POST"])
def login():
    """Check the username/password and login the user if succeeded
    """
    username = request.json["username"]
    password = request.json["password"]
    user = ah.login(username, password)
    if not user:
        return "Incorrect username/password", 401
    token = jwt.encode(
        {"public_id": user.public_id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    
    if(not type(token) is str):
        token = token.decode('UTF-8')

    return make_response(jsonify({"token": token, "username" : user.username}), 201)


@app.route("/predict", methods=["POST"])
@token_required
def predict():
    """Make a prediction based on the image given.
    Works correclty only on an image with white background and dark text
    Image with transparent background won't work
    """

    image_data = request.json["imageData"]
    base64_data = image_data.split(",")[1]  # take only the data part of the string
    nparr = np.fromstring(
        base64.b64decode(base64_data), np.uint8
    )  # transform the base64 img to an array usable by cv2
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    prediction = predicter.predict_from_img(img)

    return prediction

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
