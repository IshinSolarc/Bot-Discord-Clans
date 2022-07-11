from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SERVICE_ACCOUNT_FILE = 'gapi-key.json'

my_credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

MY_SHEET = '1gWjLgRjgnwJ5kubsd3xxGj6MSfUr8esfaZp-synbgI4' #[ID planilha]


service = build('sheets', 'v4', credentials=my_credentials)

lista_clans = ['MﾑDBunny', 'BUNNY', 'M4D']

sheet = service.spreadsheets()

#Atualiza o level ou power do usuario, recebe o nick, o valor e o tipo de atributo
#retorna True se usuario existe, False se não existe

def att_value(nick, value, type):

    for clan in lista_clans:
        result = sheet.values().get(spreadsheetId = MY_SHEET, range=(clan + '!A4:E53')).execute()
        values = result.get('values', [])
        for row in values:
            if row == []:
                continue
            if row[0].lower() == nick.lower():
                if type == 'lvl':
                    try:
                        row[2] = value
                    except:
                        row.insert(2, value)
                elif type == 'power':
                    try:
                        row[3] = value
                    except:
                        row.insert(3, value)

                print('Atualizando valor: ' + value + ' do tipo ' + type + ' no nick: ' + nick)
                try:
                    sheet.values().update(spreadsheetId = MY_SHEET, range=(clan + '!A4:E53'), valueInputOption='USER_ENTERED', body={'values': values}).execute()
                    print('Atualizado com sucesso!')
                except:
                    print('Erro ao atualizar valor')
                return True
    return False

def add_User(nick, classe, lvl, power, clan, id_discord):

    result = sheet.values().get(spreadsheetId = MY_SHEET, range=(f'{clan}!A4:D502')).execute()
    values = result.get('values', [])
    for row in values:
        if row == []:
            continue
        if row[0].lower() == nick.lower():
            return 'Usuario já existe'

    values.append([nick, classe, lvl, power, id_discord])
    try:
        sheet.values().update(spreadsheetId = MY_SHEET, range=(clan + '!A4:E53'), valueInputOption='USER_ENTERED', body={'values': values}).execute()
        return 'Adicionado com sucesso!'
    except:
        return 'Erro à adicionar usuario'