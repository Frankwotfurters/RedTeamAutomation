import subdomain
import sql_injection
from flask import Flask, redirect, url_for, render_template, request
import clickjackrpa
from admin_scanner import main
import admin_scanner
from sensitivedatarpa import scan_sensitive_data
from linkextractorrpa import scan_link_extract
import csrf
import vulncomponents
from xss import scan_xss
from viewpdf import scan_report
from viewpdfFilter import report_filter

app = Flask(__name__)

@app.route("/")
def root():
	return redirect(url_for("index"))

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/dashboard")
def dashboard():
	pdf = scan_report()

	labels = []
	for scanner in pdf['scanner']:
		if scanner not in labels:
			labels.append(scanner)

	pieValues = []
	for scanner in labels:
		pieValues.append(pdf['scanner'].count(scanner))

	dates = []
	for date in pdf['time1']:
		if date not in dates:
			dates.append(date)
	dates = sorted(dates)

	barValues = []
	for date in dates:
		barValues.append(pdf['time1'].count(date))

	colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

	return render_template("dashboard.html", set=zip(labels, pieValues, colors), dates=dates, barValues=barValues)

@app.route("/about-us")
def aboutPage():
	return render_template("about-us.html")

@app.route("/report")
def reportPage():
	return render_template("pdf.html", results=scan_report()) 

@app.route("/reportFilter", methods = ['POST'])
def reportFilterPage():
	target = request.form.get("target")
	Filterdate = request.form.get("Filterdate")
	if target == "" and Filterdate == "":
		return redirect(url_for("reportPage"))
	else:
		return render_template("pdfFilter.html", target=target, Filterdate=Filterdate, results=report_filter(target, Filterdate))

@app.route("/sqli")
def sqliPage():
	try:
		error = request.args["error"]
	except:
		return render_template("sqli.html")
	return render_template("sqli.html", error=error)

@app.route("/sqliRun", methods = ['POST'])
def sqliRun():
	target = request.form.get("target")
	email = request.form.get("email")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("sqliRun.html", target=target, results=sql_injection.scan_sql_injection(target, email))
	else:
		return redirect(url_for("sqliPage", error="Target does not begin with http:// or https://"))

@app.route("/subdomain")
def subdPage():
	try:
		error = request.args["error"]
	except:
		return render_template("subdomain.html")
	return render_template("subdomain.html", error=error)

@app.route("/subdomainRun", methods = ['POST'])
def subdRun():
	target = request.form.get("target")
	email = request.form.get("email")
	if target.endswith('.txt'):
		return render_template("subdomainRun.html", target=target, results=subdomain.subdCode(target, email))
	else:
		return redirect(url_for("subdPage", error="Only files with the '.txt' extension are  allowed!"))

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
	email = request.form.get("email")
	count = 0
	if target.startswith('http://') or target.startswith('https://'):
		count = count +1
	if target.endswith('/'):
		count = count +1
	if count == 2:
		return render_template("admin-scannerRun.html", target=target, results=main(target, email))
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
	target = request.form.get("target")
	email = request.form.get("email")
	if target.endswith('.txt'):
		return render_template("clickjackRun.html", target=target, results=clickjackrpa.main(target, email))
	else:
		return redirect(url_for("clickjackPage", error="Only files with the '.txt' extension are  allowed!"))

@app.route("/xss")
def xssScannerPage():
	try:
		error = request.args["error"]
	except:
		return render_template("xss.html")
	return render_template("xss.html", error=error)

@app.route("/xssRun", methods = ['POST'])
def xssScannerRun():
	target = request.form.get("target")
	email = request.form.get("email")
	if target.startswith('http://') or target.startswith('https://'):
		return render_template("xssRun.html", target=target, results=scan_xss(target, email))
	else:
		return redirect(url_for("xssScannerPage", error="Please follow the recommended format!"))


@app.route("/sensitive-data")
def sendataPage():
	try:
		error = request.args["error"]
	except:
		return render_template("sensitive-data.html")
	return render_template("sensitive-data.html", error=error)

@app.route("/sensitive-dataRun", methods = ['POST'])
def sendataRun():
	target = request.form.get("target")
	email = request.form.get("email")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("sensitive-dataRun.html", target=target, results=scan_sensitive_data(target, email))
	else:
		return redirect(url_for("sendataPage", error="Target does not begin with http:// or https://"))
	

@app.route("/link-extractor")
def linkextractPage():
	try:
		error = request.args["error"]
	except:
		return render_template("link-extractor.html")
	return render_template("link-extractor.html", error=error)

@app.route("/link-extractorRun", methods = ['POST'])
def linkextractRun():
	target = request.form.get("target")
	email = request.form.get("email")
	if target.startswith('http://') or target.startswith('https://'):
			return render_template("link-extractorRun.html", target=target, results=scan_link_extract(target, email))
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
	max = request.form.get("max")
	email = request.form.get("email")
	if loginPage.startswith('http://') or loginPage.startswith('https://'):
		return render_template("csrfRun.html", target=loginPage, results=csrf.main(creds, loginPage, max, email))
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
	email = request.form.get("email")
	if target.startswith('http://') or target.startswith('https://'):
		return render_template("vuln-componentsRun.html", target=target, results=vulncomponents.main(target, email))
	else:
		return redirect(url_for("vulncompPage", error="Target does not begin with http:// or https://"))


if  __name__ == "__main__":
	app.run()