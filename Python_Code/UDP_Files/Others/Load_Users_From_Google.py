import gspread
from oauth2client.service_account import  ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('SalsaBeats.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Encuesta Creatividad (respuestas)').sheet1

users = sheet.get_all_records()
print(users)