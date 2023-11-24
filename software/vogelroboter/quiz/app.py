from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    st="""
    <h1>Vögelroboter!</h1>"
    <img src="/img/Northern-Lapwing-Vanellus-vanellus_crop.jpg">
    """
    return st
