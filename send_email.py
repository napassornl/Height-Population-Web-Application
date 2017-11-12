# don't name function email bc there is a built in function called email
from email.mime.text import MIMEText
import smtplib

def send_email(email,height,average_height,count):
    from_email="napassorn@gmail.com"
    from_password="1490511358Kus39"
    to_email=email

    subject="Height Data"
    message="Hi, you height is <strong>%s</strong> cm. <br> Average height of all is <strong>%s</strong> cm and that is calculated out of <strong>%s</strong> of people. <br> Thank you." % (height,average_height,count)
    # MIMEText object which is a special email object
    # that can be passed to the smtplib object. The smtplib
    # object is designed that way so that it sends the message
    # text contained inside MIMEText to another email address
    # MIMEText object has some attributes which are Subject,
    # To, and From and you need to assign your own values to
    # those attributes
    msg=MIMEText(message,"html") # create object where message is read as html text, so can put html syntax
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email
    gmail=smtplib.SMTP('smtp.gmail.com',587) # pass special email server and port #
    gmail.ehlo() # identifies the server as a ESMTP server
    gmail.starttls() # encrypts the connection
    gmail.login(from_email,from_password) # logs into your email account via Python
    gmail.send_message(msg) # sends the MIMEText object
