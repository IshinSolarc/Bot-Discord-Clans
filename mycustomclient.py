import discord
import google_api_access

roles_staffs_id = [915042701760667688, 916498411556077588, 959441903630315592, 961828824675409950]

staffs = {
        914774637563494440: 'Lunefa',
        270812637242195968: 'IshinSolarc',
        333824903629373443: 'Himura',
        90622406988693504: 'Arcanine',
        433013140557398059: 'Khayows'
        }


def is_staff(member):
    for role in member.roles:
        if role.id in roles_staffs_id:
            return True
    return False

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logado como {self.user}!')

    async def on_message(self, message):

        #bot ignora proprias mensagens
        if message.author == self.user:
            return

        #bot atualiza o level do usuario
        if message.content.startswith('!attlvl') and message.channel.id == 981655532203044966: 

            content = message.content.replace('!attlvl ', '')
            content = content.split(' ')

            if len(content) != 1 or content[0].isdigit() == False:
                await message.reply('Como usar: !attlvl <LVL>')
                return

            if message.author.id in staffs:
                nick = staffs[message.author.id]
                lvl = content[0]
                if google_api_access.att_value(nick, lvl, 'lvl'):
                    await message.reply('Atualizado com sucesso!')
                return
                
            
            try:
                nick_atual = message.author.display_name.split(' - ')
                novo_nick = content[0] + ' - ' + nick_atual[1]

                if nick_atual[0].isdigit() == False:
                    await message.reply('Seu nick não está nos padrões do discord MADBUNNY, passe pela identificação.')
                    return

                await message.author.edit(nick = novo_nick)
                await message.reply('LVL atualizado com sucesso!')
                google_api_access.att_value(nick_atual[1], content[0], 'lvl')

            except:
                await message.reply('Seu nick não está nos padrões do discord MADBUNNY, passe pela identificação.')

        #bot atualiza o power do usuario
        if message.content.startswith('!attpower') and message.channel.id == 982118609004421180:

            content = message.content.replace('!attpower ', '')
            content = content.split(' ')

            if len(content) != 1 or content[0].isdigit() == False:
                await message.reply('Como usar: !attpower <POWER>')
                return

            if message.author.id in staffs:
                nick = staffs[message.author.id]
                power = content[0]
                if google_api_access.att_value(nick, power, 'power'):
                    await message.reply('Atualizado com sucesso!')
                return

            try:
                nick_atual = message.author.display_name.split(' - ')
                retorno = google_api_access.att_value(nick_atual[1], content[0], 'power')
                if retorno == True:
                    await message.reply('Power atualizado com sucesso!')
                else:
                    await message.reply(nick_atual[1] + ' é um nome não encontrado na planilha, contate a staff!')
            except:
                return

        #bot identifica o usuario e adiciona na planilha
        if message.content.startswith('!adduser') and message.channel.id == 982118609004421180:
            



        #bot indica que está online
        if message.content.startswith('!test'):
            await message.channel.send('To vivo!')
        
        

        


