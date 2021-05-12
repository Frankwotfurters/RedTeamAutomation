from subdomain import subdCode
from threaded_subdomain import thsubdRun
from sql_injection import scan_sql_injection
from flask import Flask, redirect, url_for, render_template, request
import csrf
import clickjackrpa
from admin_scanner import main

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
	return render_template("subdomainRun.html", target=target, results=subdCode())

@app.route("/th-subdomain")
def thsubdPage():
	return render_template("th-subdomain.html")

@app.route("/th-subdomainRun", methods = ['POST'])
def thsubdRun():
	target = request.form.get("target")
	domain = request.form.get("target2")
	outputFile = request.form.get("target3")
	return render_template("th-subdomainRun.html", target=target, domain=domain, outputFile=outputFile, results=thsubdRun())

@app.route("/admin-scanner")
def adminScannerPage():
	return render_template("admin-scanner.html")

@app.route("/admin-scannerRun", methods = ['POST'])
def adminScannerRun():
	target = request.form.get("target")
	return render_template("admin-scannerRun.html", target=target, results=main(target))

@app.route("/clickjack")
def clickjackPage():
	return render_template("clickjack.html")

@app.route("/clickjackRun", methods = ['POST'])
def clickjackRun():
	target = request.files['target']
	return render_template("clickjackRun.html", target=target, results=clickjackrpa.main(target))

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
	print(request.args)
	try:
		error = request.args["error"]
	except:
		return render_template("csrf.html")
	return render_template("csrf.html", error=error)

@app.route("/csrfRun", methods = ['POST'])
def csrfRun():
	creds = [request.form.get("userID"), request.form.get("password")]
	loginPage = request.form.get("target")
	if loginPage.startswith('http://') or loginPage.startswith('https://'):
		return render_template("csrfRun.html", results=csrf.main(creds, loginPage))
	else:
		return redirect(url_for("csrfPage", error="Target does not begin with http:// or https://"))

@app.route("/vuln-components")
def vulncompPage():
	return render_template("vuln-components.html")

if  __name__ == "__main__":
	app.run(debug=True)