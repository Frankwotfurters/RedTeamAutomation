from flask import Flask, redirect, url_for, render_template
import csrf

app = Flask(__name__)

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/sqli")
def sqliPage():
	return render_template("sqli.html")

@app.route("/subdomain")
def subdPage():
	return render_template("subdomain.html")

@app.route("/th-subdomain")
def thsubdPage():
	return render_template("th-subdomain.html")

@app.route("/admin-scanner")
def adminScannerPage():
	return render_template("admin-scanner.html")

@app.route("/clickjack")
def clickjackPage():
	return render_template("clickjack.html")

@app.route("/xss")
def xssPage():
	return render_template("xss.html")

@app.route("/sensitive-data")
def sendataPage():
	return render_template("sensitive-data.html")

@app.route("/link-extractor")
def linkextractPage():
	return render_template("link-extractor.html")

@app.route("/csrf")
def csrfPage():
	return render_template("csrf.html")

@app.route("/vuln-components")
def vulncompPage():
	return render_template("vuln-components.html")

if  __name__ == "__main__":
	app.run(debug=True)