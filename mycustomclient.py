import discord
import google_api_access

roles_staffs_id: list = [994996873448398960, 999651297303212092]

canais: dict = {
    'AttLVL' : 995140258389839964,
    'AttPower' : 995140295064817694,
    'Logs' : 995134662991163394
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

        if message.content.startswith('!stafflvl'):

                if is_staff(message.author) == False:
                    await message.reply('Você não tem permissão para usar este comando!')
                    return

                content = message.content.replace('!stafflvl ', '')
                content = content.split(' ')
    
                if len(content) != 2 or content[1].isdigit() == False:
                    await message.reply('Alteração especial para staffs modificarem o lvl sem usar a planilha! Como usar: !stafflvl <Nick> <LVL>')
                    return

                try:
                    retorno = google_api_access.att_value(content[0], content[1], 'lvl')
                    if retorno == False:
                        await message.reply('Nick incorreto ou nick inexistente na planilha!')
                    else:
                        await message.reply('LVL atualizado com sucesso!')
                except:
                    await message.reply('Um erro fatal ocorreu!')
                
                

        #bot atualiza o power de usuario especifico
        if message.content.startswith('!staffpower'):

                if is_staff(message.author) == False:
                    await message.reply('Você não tem permissão para usar este comando!')
                    return
    
                content = message.content.replace('!staffpower ', '')
                content = content.split(' ')
    
                if len(content) != 2 or content[1].isdigit() == False:
                    await message.reply('Alteração especial para staffs modificarem o power sem usar a planilha! Como usar: !staffpower <Nick> <POWER>')
                    return
    
                try:
                    retorno = google_api_access.att_value(content[0], content[1], 'power')
                    if retorno == False:
                        await message.reply('Nick incorreto ou nick inexistente na planilha!')
                    else:
                        await message.reply('Power atualizado com sucesso!')
                except:
                    return
        
        #bot atualiza o level do usuario
        if message.content.startswith('!attlvl') and message.channel.id == canais['AttLVL']: 

            content = message.content.replace('!attlvl ', '')
            content = content.split(' ')

            if len(content) != 1 or content[0].isdigit() == False:
                await message.reply('Como usar: !attlvl <LVL>')
                return
            
            try:
                nick_atual = message.author.display_name.split(' - ')
                novo_nick = content[0] + ' - ' + nick_atual[1]

                if nick_atual[0].isdigit() == False:
                    await message.reply('Seu nick não está nos padrões do discord Snack Opal Taurus, passe pela identificação.')
                    return

                await message.author.edit(nick = novo_nick)
                await message.reply('LVL atualizado com sucesso!')
                google_api_access.att_value(nick_atual[1], content[0], 'lvl')

            except:
                await message.reply('Erro ao atualizar na planilha.')

        #bot atualiza o power do usuario
        if message.content.startswith('!attpower') and message.channel.id == canais['AttPower']:

            content = message.content.replace('!attpower ', '')
            content = content.split(' ')

            if len(content) != 1 or content[0].isdigit() == False:
                await message.reply('Como usar: !attpower <POWER>')
                return

            try:
                nick_atual = message.author.display_name.split(' - ')
                retorno = google_api_access.att_value(nick_atual[1], content[0], 'power')
                if retorno == True:
                    await message.reply('Power atualizado com sucesso!')
                else:
                    await message.reply(nick_atual[1] + ' é um nome não encontrado na planilha, contate a staff!')
            except:
                await message.reply('Um erro fatal ocorreu, seu nick está no padrão do discord?')
                return


        #staff adiciona o usuario a planilha com entradas de nick, classe, lvl, power, clan e discord
        if message.content.startswith('!adduser') and is_staff(message.author):
                
                content = message.content.replace('!adduser ', '')
                content = content.split(' ')
    
                if len(content) != 6:
                    await message.reply('Como usar: !adduser <Nick> <Classe> <LVL> <POWER> <Discord> <Clan>')
                    return

                print(content)
                try:
                    retorno = google_api_access.add_User(content[0], content[1], content[2], content[3], content[4], content[5])
                    if retorno == 'Adicionado com sucesso!':
                        await message.reply('Usuário adicionado com sucesso!')
                    elif retorno == 'Usuário já existe!':
                        await message.reply('Usuário já existe na planilha!')
                except:
                    await message.reply('Um erro fatal ocorreu!')
                    return

        #bot indica que está online
        if message.content.startswith('!test'):
            await message.channel.send('To vivo!')
            return
        
        

        


