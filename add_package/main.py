import gspread
from logic import route_ok, package_ok
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('./client_secret_656259280327-i9iibttp2aamulak49ap9p4dhof0uvhi.apps.googleusercontent.com.json', scope)
client = gspread.authorize(creds)

sheet = client.open("test").get_worksheet(0)

data = sheet.get_all_values()
print(data)
