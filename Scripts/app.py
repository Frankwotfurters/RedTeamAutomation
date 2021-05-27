from subdomain import subdCode
#from threaded_subdomain import main
from sql_injection import scan_sql_injection
from flask import Flask, redirect, url_for, render_template, request
import clickjackrpa
from admin_scanner import main
import admin_scanner
from sensitivedatarpa import scan_sensitive_data
from linkextractorrpa import scan_link_extract
from linkextractorrpa import print_report
import csrf
import vulncomponents


app = Flask(__name__)

@app.route("/")
def root():
	return redirect(url_for("index"))

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/about-us")
def aboutPage():
	return render_template("about-us.html")

@app.route("/sqli")
def sqliPage():
	print(request.args)
	try:
		error = request.args["error"]
	except:
		return render_template("sqli.html")
	return render_template("sqli.html", error=error)

@app.route("/sqliRun", methods = ['POST'])
def sqliRun():
	target = request.form.get("target")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("sqliRun.html", target=target, results=scan_sql_injection(target))
	else:
		return redirect(url_for("sqliPage", error="Target does not begin with http:// or https://"))

@app.route("/subdomain")
def subdPage():
	print(request.args)
	try:
		error = request.args["error"]
	except:
		return render_template("subdomain.html")
	return render_template("subdomain.html", error=error)

@app.route("/subdomainRun", methods = ['POST'])
def subdRun():
	target = request.form.get("target")
	return render_template("subdomainRun.html", target=target, results=subdCode())

@app.route("/admin-scanner")
def adminScannerPage():
	try:
		error = request.args["error"]
	except:
		return render_template("admin-scanner.html")
	return render_template("admin-scanner.html", error=error)

@app.route("/admin-scannerRun", methods = ['POST'])
def adminScannerRun():
	target = request.form.get("target")
	count = 0
	if target.startswith('http://') or target.startswith('https://'):
		count = count +1
	if target.endswith('/'):
		count = count +1
	if count == 2:
		return render_template("admin-scannerRun.html", target=target, results=main(target))
	else:
		return redirect(url_for("adminScannerPage", error="Please follow the recommended format!"))

@app.route("/clickjack")
def clickjackPage():
	try:
		error = request.args["error"]
	except:
		return render_template("clickjack.html")
	return render_template("clickjack.html", error=error)

@app.route("/clickjackRun", methods = ['POST'])
def clickjackRun():
	#target = request.files['target']
	target = request.form.get("target")
	if target.endswith('.txt'):
		return render_template("clickjackRun.html", target=target, results=clickjackrpa.main(target))
	else:
		return redirect(url_for("clickjackPage", error="Only files with the '.txt' extension are  allowed!"))


@app.route("/sensitive-data")
def sendataPage():
	print(request.args)
	try:
		error = request.args["error"]
	except:
		return render_template("sensitive-data.html")
	return render_template("sensitive-data.html", error=error)

@app.route("/sensitive-dataRun", methods = ['POST'])
def sendataRun():
	target = request.form.get("target")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("sensitive-dataRun.html", target=target, results=scan_sensitive_data(target))
	else:
		return redirect(url_for("sendataPage", error="Target does not begin with http:// or https://"))
	

@app.route("/link-extractor")
def linkextractPage():
	print(request.args)
	try:
		error = request.args["error"]
	except:
		return render_template("link-extractor.html")
	return render_template("link-extractor.html", error=error)

@app.route("/link-extractorRun", methods = ['POST'])
def linkextractRun():
	target = request.form.get("target")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("link-extractorRun.html", target=target, results=scan_link_extract(target), result=print_report(target))
	else:
		return redirect(url_for("linkextractPage", error="Target does not begin with http:// or https://"))

@app.route("/csrf")
def csrfPage():
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
	try:
		error = request.args["error"]
	except:
		return render_template("vuln-components.html")
	return render_template("vuln-components.html", error=error)

@app.route("/vuln-componentsRun", methods = ['POST'])
def vulncompRun():
	target = request.form.get("target")
	if target.startswith('http://') or target.startswith('https://'):
		return render_template("vuln-componentsRun.html", results=vulncomponents.main(target))
	else:
		return redirect(url_for("vulncompPage", error="Target does not begin with http:// or https://"))


if  __name__ == "__main__":
	app.run(debug=True)