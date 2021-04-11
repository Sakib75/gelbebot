import pandas as pd
import os
import smtplib
from email.message import EmailMessage

sender = "leadgensakib@gmail.com"
receiver = "SJ.Immobilie@gmail.comm"
password = "sakib7575"

   
   

def Check_Dif(city):
	try:
		df2 = pd.read_csv(f'{city}_old.csv')
		df1 = pd.read_csv(f'{city}.csv')
	except:
		return None

	dif_list = [x for x in list(df1['heading'].unique()) if x not in list(df2['heading'].unique())]
	print(dif_list)
	if(len(dif_list)):

	dfdif = df1[(df1['heading'].isin(dif_list))]

	if(not dfdif.empty):
		diff = True
	else:
		diff = False

	return {'Diff':diff,'df' : dfdif}




def SendMail():
	new = Check_Dif('Essen')
	if(new['diff']):

		df_test = new['df'].reset_index()[['heading','website','status']].fillna('')

		html = """\
		<html>
		  <head>
		  
		  </head>
		  <body>

		  <center><h1> {0} New item found! </h1> </br>
		    {1}
		    </center>
		  </body>
		</html>
		""".format(len(df_test),df_test.to_html(classes='df'))

		msg = EmailMessage()
		msg['Subject'] = 'Update for today!'
		msg['From'] = sender
		msg['To'] = receiver
		msg.set_content('There are two new listing found!')
		msg.add_alternative(html,subtype='html')

		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			smtp.login(sender,password)
			smtp.send_message(msg)
