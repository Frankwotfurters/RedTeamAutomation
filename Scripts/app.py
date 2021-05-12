from subdomain import subdCode
from sql_injection import scan_sql_injection
from flask import Flask, redirect, url_for, render_template, request
import csrf

app = Flask(__name__)

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/about-us")
def aboutPage():
	return render_template("about-us.html")

@app.route("/sqli")
def sqliPage():
	return render_template("sqli.html")

@app.route("/sqliRun", methods = ['POST'])
def sqliRun():
	target = request.form.get("target")
	return render_template("sqliRun.html", target=target, results=scan_sql_injection(target))

@app.route("/subdomain")
def subdPage():
	return render_template("subdomain.html")

@app.route("/subdomainRun", methods = ['POST'])
def subdRun():
	target = request.form.get("target")
	return render_template("sqliRun.html", target=target, results=subdCode())

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

@app.route("/csrfRun", methods = ['POST'])
def csrfRun():
	target = request.form.get("target")
	return render_template("csrfRun.html", target=target, results=csrf.main())

@app.route("/vuln-components")
def vulncompPage():
	return render_template("vuln-components.html")

if  __name__ == "__main__":
	app.run(debug=True)