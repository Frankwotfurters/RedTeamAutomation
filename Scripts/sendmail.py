import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
attachment = "/media/sf_Scripts/Clickjacking_07-06-2021232118.pdf"
receiver = "1905670D@student.tp.edu.sg"
scanner = "CSRF"
target = "https://www.google.com"

def main(scanner, target, attachment, receiver):
	try:
		# Craft message (obj)
		msg = MIMEMultipart()

		# message = f'{message}\nSend from Hostname: hostname'
		msg['Subject'] = f'{scanner} Scan complete!'
		msg['From'] = 'RPA Integrated RTA'
		msg['To'] = receiver
		msg.attach(MIMEText(f"{scanner} Scan on {target} complete! \nPlease check the attached PDF report for more details!"))

		# Attach PDF report
		with open(attachment, "rb") as f:
			attach = MIMEApplication(f.read(),_subtype="pdf")
		attach.add_header('Content-Disposition','attachment',filename=str(attachment))
		msg.attach(attach)

		# message = "From: RPA Integrated RTA\nTo: " + ", " + receiver + "\nSubject: Scan complete!\n\nScan complete! Please check the attached PDF report for more details!\n"
		# Start smtp session
		server = smtplib.SMTP('smtp.gmail.com')
		server.ehlo()
		server.starttls()
		server.login('rpaxrta@gmail.com', 'rpaintegratedrta')

		# Send mail
		server.sendmail('rpaxrta@gmail.com', receiver, msg.as_string())
		print(f"Email sent to {receiver}!")
		logging.info(f"Email sent to {receiver}!")

		# Cleanup
		server.close()

	except Exception as e:
		# Error handling
		print("Email not sent!")
		logging.info("Email not sent!")
		print(e)
		logging.info(e)

if __name__ == '__main__':
	main(scanner, target, attachment, receiver)