from flask import Flask, redirect, url_for, render_template
import csrf

app = Flask(__name__)

@app.route("/index")
def index():
	return render_template("index.html", content=["joe", "mama", "hortons"])

@app.route("/sqli")
def sqliPage():
	return "SQLI"

@app.route("/subdomain")
def subdPage():
	return "subdomain"

@app.route("/th-subdomain")
def thsubdPage():
	return "threaded-subdomain"

@app.route("/admin-scanner")
def adminScannerPage():
	return "Admin Scanner"

@app.route("/clickjack")
def clickjackPage():
	return "Clickjack"

@app.route("/xss")
def xssPage():
	return "XSS"

@app.route("/sensitive-data")
def sendataPage():
	return "Sensitive Data Exposure"

@app.route("/link-extract")
def linkextractPage():
	return "Link Extractor"

@app.route("/csrf")
def csrfPage():
	return csrf.main

@app.route("/vuln-components")
def vulncompPage():
	return "Vulnerable Components"

if  __name__ == "__main__":
	app.run(debug=True)