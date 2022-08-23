from __future__ import print_function

from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SERVICE_ACCOUNT_FILE = 'gapi-key.json'

my_credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

MY_SHEET = '1sM7McY5Uknrbk773P-2nsr3gbxWGnJ6-FopIvAQYPFo' #[ID planilha]

service = build('sheets', 'v4', credentials=my_credentials)

THE_RANGE = 'Players!A4:F200'

lista_clans = []

sheet = service.spreadsheets()

#Atualiza o level ou power do usuario, recebe o nick, o valor e o tipo de atributo
#retorna True se usuario existe, False se não existe

def att_value(nick, value, type):
    result = sheet.values().get(spreadsheetId=MY_SHEET, range=(THE_RANGE)).execute()
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
                sheet.values().update(spreadsheetId = MY_SHEET, range=(THE_RANGE), valueInputOption='USER_ENTERED', body={'values': values}).execute()
                print('Atualizado com sucesso!')
            except:
                print('Erro ao atualizar valor')
            return True
    return False

def add_User(nick, classe, lvl, power, id_discord, clan):
    result = sheet.values().get(spreadsheetId = MY_SHEET, range=(THE_RANGE)).execute()
    values = result.get('values', [])
    
    for row in values:
        if row != []:
            if row[0].lower() == nick.lower():
                print('Usuario ja existe!')
                return 'Usuário já existe!'

    values.append([nick, classe, lvl, power, id_discord, clan])

    try:
        sheet.values().update(spreadsheetId = MY_SHEET, range=(THE_RANGE), valueInputOption='USER_ENTERED', body={'values': values}).execute()
        return 'Adicionado com sucesso!'
    except:
        return 'Erro à adicionar usuario'