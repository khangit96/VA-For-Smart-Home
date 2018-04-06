import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
# Email you want to send the update from (only works with gmail)
fromEmail = 'tdmuteam2016@gmail.com'
# You can generate an app password here to avoid storing your password in plain text
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = 'tdmuteam'

# Email you want to send the update to
toEmail = 'khangit69@gmail.com'

def sendEmail(imgFileName):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Security Update'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Raspberry pi security camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)
	img = open(imgFileName, 'rb').read()
	msgImg = MIMEImage(img, 'jpg')
	msgRoot.add_header('Content-ID', '<image1>')
	msgRoot.add_header('Content-Disposition', 'inline', filename=imgFileName)
	msgRoot.attach(msgImg)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
