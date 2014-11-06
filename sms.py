import logger
from twilio.rest import TwilioRestClient
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC41688867b00916213b4397a82ebfdc09"
auth_token  = "c7de20e3efb2dba4e18c2ee6af6662b1"
client = TwilioRestClient(account_sid, auth_token)

telefonos= ['+524641074694', '+524641363357']

def MSG(msg):
	try:
		for numero in telefonos:
			message = client.messages.create(body=str(msg),
			to=str(numero), # Replace with your phone number
			from_="+14804055025") # Replace with your Twilio number
	except:
		logger.error("No se pudo enviar el msn con el texto: " + str(msg))