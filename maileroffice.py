import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

username = "svcSMTP-Cloud@spc.int"
password = "m9Td#(fOVNcQj#z"
mail_from = "svcSMTP-Cloud@spc.int"
mail_to = "divesha@spc.int"
mail_subject = "Tailored Wave Forecast TV"
mail_body = "Talofa! <br/>"
mail_body += "<span style='background-color:#51b73b; color:#FFF; font-weight:bold;'> &nbsp; &nbsp; &nbsp; &nbsp;BETA MODE &nbsp; &nbsp; &nbsp; &nbsp;</span> <br/>"
mail_body+="Kindly attaching High resolution wave forecast for locations around Tuvalu. <br/><br/>"
mail_body+="<i>*** This is an automatically generated email, please do not reply ...</i><br/>"
mail_body+="Tuvalu Met Service"


def send_email(documents, receipients):
    exampleCombinedString = ','.join(receipients)
    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=exampleCombinedString
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'html'))

    for x in documents:
        with open(x, "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition','attachment',filename=str(x))
            mimemsg.attach(attach)

    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()


