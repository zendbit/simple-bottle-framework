# mailer extensions
# handle mail function

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import traceback

class Mailer():
    '''
        list of mail address
        with properties to connect to smtp server
        
        maillist = {
        'admin':{
            'username':'',
            'password':'',
            'sender':'',
            'smtp_server':'',
            'port':''},
        'helpdesk':{
            'username':'',
            'password':'',
            'sender':'',
            'smtp_server':'',
            'port':''}}
    '''
    def __init__(self, maillist):
        self.maillist = maillist
        
    # send email using gmail
    # data should in dictionary format
    # data = {'usemail':'maillist', 'to':'to', 'subject':'subject', 'text':'text', 'attach':('attachment1', attachment2, attachment3, attachment...)}
    def send_email(self, data):
        to = data.get('to')
        subject = data.get('subject')
        text = data.get('text')
        attach = data.get('attach')
        usemail = data.get('usemail')
        username = self.maillist.get(usemail).get('username')
        password = self.maillist.get(usemail).get('password')
        smtp_server = self.maillist.get(usemail).get('smtp_server')
        port = self.maillist.get(usemail).get('port')
        sender = self.maillist.get(usemail).get('sender')
        # validate require value
        if username and password and to and subject and text and smtp_server and port and sender:
            msg = MIMEMultipart()
        
            msg['From'] = sender
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(text, 'html'))
            
            # if attachment
            if attach and len(attach):
                
                for attachment in attach:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(open(attach, 'rb').read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(attachment))
                    msg.attach(part)
            
            mailServer = smtplib.SMTP(smtp_server, port)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(username, password)
            mailServer.sendmail(sender, to, msg.as_string())
            mailServer.quit()

    # get mail template
    # data is pair of key and value
    # key is data {'string to replace', 'replace string'}
    def get_email_template(self, template_file, data=None):
        if os.path.isfile(template_file):
            f = open(template_file, 'r')
            template = ''.join(f.readlines())
            f.close()
            
            # check replace data
            if data and len(data):
                for key in data:
                    template = template.replace('{' + key + '}', data.get(key))
                
            return template
            
        return None
        
    # specific send email purpose
    #############################
    # send activation code
    # data = {'usemail':'', template_data:{template:'', data:{}}, 'to':'to', 'subject':'subject'}
    def send_email_use_template(self, data):
        template_data = data.get('template_data')
        html = self.get_email_template(template_data.get('template'), template_data.get('data'))
        data['text'] = html
        self.send_email(data)
