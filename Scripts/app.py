from flask import Flask, redirect, url_for, render_template
import csrf

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html", content=["joe", "mama", "hortons"])

@app.route("/<name>")
def user(name):
	return f"Hello {name}"

@app.route("/csrf")
def csrfPage():
	return csrf.main()

if  __name__ == "__main__":
	app.run()