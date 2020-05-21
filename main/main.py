import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import secrets


# set the subject of the email you want to send
subject='final test'

def read_template(filename):

    # Returns a Template object comprising the contents of the 
    # file specified by filename.
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main(filename='contacts.txt'):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    # start smtp using tls
    s.starttls()
    # log into your account
    s.login(secrets.MY_ADDRESS, secrets.PASSWORD)

    # open contacts file
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        # read single lines in the contactd file
        for line in contacts_file.readlines():
            # split the line into two
            line=line.split()
            emails=line[-1]
            # now remove email so that you are left with names only
            line=line[:-1]
            names=''
            for name in line:
                names+=name+' '
            # remove trailing whitespaces
            personal_names=names.strip().capitalize()
            email_name=emails.lower()
            # also for every line send an email
            print(r'Sending email to:{} with address:{}'.format(personal_names,email_name))
        
            send_mail(s,personal_names,email_name)
        
        # close the smtp connection after it is done 
        s.quit()
        # close the open contacts file after it is done
        contacts_file.close()
                
# a function to send an email to every adress line in contacts
def send_mail(s,name,email):

    msg = MIMEMultipart()       
    # create a message
    message_template = read_template('message.txt')
    # add the name of the person to be sent the email
    message = message_template.substitute(Name_of_human=name,My_name=secrets.MY_NAME)
    
    # setup the parameters of the message
    msg['From']= secrets.MY_NAME
    msg['To']=email
    msg['Subject']=subject
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # Attach the pdf to the msg going by e-mail
    path_to_pdf='adams-douglas-the-hitchhikers-guide-to-the-galaxy.pdf'
    with open(path_to_pdf, "rb") as f:
        #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename=str(path_to_pdf))
    msg.attach(attach)
    # send the message via the server set up earlier.
    try:
        s.send_message(msg)
        if True:
            print('email sent successfully ✓✓')       
    except:
        print(r'Failed sending email to:{} with address:{}'.format(name,email))
    del msg

if __name__=='__main__':
    main()


