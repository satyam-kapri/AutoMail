import smtplib
import pandas as pd
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# ----------------------------------------------------------
my_name = "Satyam Kapri"

# -----------------------------------------------------------
def processexcel(excelfile,message,subject,attachment,my_email,my_password):
      server=""
      for i in range(3):
         try:
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(my_email,my_password)
            print("connection done")
            break
         except:
            print("smtp connection failed")
      #---------------------------------------------------------
      email_list = pd.read_excel(excelfile)
      # -----------------------------------------------
      pattern = r"\{(.+?)\}"
      matches = re.findall(pattern, message)
     # ---------------------------------------------------
      all_names = email_list['name']
      all_emails = email_list['email']
      #  -----------------------------------------------
      # ------------------------------------------------
      for idx in range(len(all_emails)):
         # ----------------------------------
         if all_names[idx]!=None:
            name = all_names[idx]
         email = all_emails[idx]
         # ---------------------------------------------
         personalizedmsg=message        
         for i in matches:
             personalizedmsg= personalizedmsg.replace("{"+i+"}",str(email_list[i][idx]))
          # ------------------------------------------------
         msgtosend = MIMEMultipart()
         msgtosend['From'] =my_email
         msgtosend['To'] = email
         msgtosend['Subject']=subject
         
         if attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment}"
            )
            msgtosend.attach(part)
         msgtosend.attach(MIMEText(personalizedmsg, 'html'))
       
         print("sending...")
         try:
            server.send_message(msgtosend)
            print('Email to {} successfully sent!\n'.format(email))
         except Exception as e:
            print('Email to {} could not be sent :( because {}\n'.format(email, str(e)))
      server.quit()

# csv="uploads/Book1.xlsx"
# attach="uploads/8086_Microprocessor_LDTmJhx.pdf"
