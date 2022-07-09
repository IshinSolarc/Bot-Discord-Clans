import discord
import google_api_access

roles_staffs_id: list = [915042701760667688, 916498411556077588, 959441903630315592, 961828824675409950]

staffs: dict = {
        914774637563494440: 'Lunefa',
        270812637242195968: 'IshinSolarc',
        333824903629373443: 'Himura',
        90622406988693504: 'Arcanine',
        433013140557398059: 'Khayows'
        }

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

    async def log(self, message):
        channel = self.get_channel(canais['Logs'])
        await channel.send(message)
        return

    async def on_message(self, message):

        log: str = f'Comando utilizado não está programado para logar.'

        #bot ignora proprias mensagens
        if message.author == self.user:
            return

        if message.content.startswith('!stafflvl'):

                if is_staff(message.author) == False:
                    await message.reply('Você não tem permissão para usar este comando!')

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
                        log = f'{message.author.name} alterou o power de {content[0]} para {content[1]}'
                except:
                    log = f'{message.author.name} tentou alterar o power de {content[0]} para {content[1]} e um erro fatal ocorreu!'

                self.log(log)

                
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
                    await message.reply('Seu nick não está nos padrões do discord Callidus, passe pela identificação.')
                    return

                await message.author.edit(nick = novo_nick)
                await message.reply('LVL atualizado com sucesso!')
                google_api_access.att_value(nick_atual[1], content[0], 'lvl')
                log = f'{message.author.name} alterou o lvl de {nick_atual[1]} para {content[0]}'

            except:
                await message.reply('Seu nick não está nos padrões do discord Callidus, passe pela identificação.')
                log = f'{message.author.name} tentou alterar o lvl de {nick_atual[1]} para {content[0]} e um erro fatal ocorreu!'

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
                    log = f'{message.author.name} alterou o power de {nick_atual[1]} para {content[0]}'
                else:
                    await message.reply(nick_atual[1] + ' é um nome não encontrado na planilha, contate a staff!')
                    log = f'{message.author.name} tentou alterar o power para {content[0]}, porém não estava na planilha!'
            except:
                await message.reply('Um erro fatal ocorreu!')
                log = f'{message.author.name} tentou alterar o power de {nick_atual[1]} para {content[0]} e um erro fatal ocorreu!'
                return

            self.log(log)

        #staff adiciona o usuario a planilha com entradas de nick, classe, lvl, power e clan
        if message.content.startswith('!adduser') and is_staff(message.author) == True:
                
                content = message.content.replace('!adduser ', '')
                content = content.split(' ')
    
                if len(content) != 5:
                    await message.reply('Como usar: !adduser <Nick> <Classe> <LVL> <POWER> <Clan>')
                    return
    
                try:
                    user_discord = message.author.name + '#' + message.author.discriminator
                    retorno = google_api_access.add_user(content[0], content[1], content[2], content[3], content[4], user_discord)
                    if retorno == 'Adicionado com sucesso!':
                        await message.reply('Usuário adicionado com sucesso!')
                        log = f'{message.author.name} adicionou o usuário {content[0]} a planilha!'
                    elif retorno == 'Usuário já existe!':
                        await message.reply('Usuário já existe na planilha!')
                        log = f'{message.author.name} tentou adicionar o usuário {content[0]} a planilha, porém ele já existe!'
                except:
                    await message.reply('Um erro fatal ocorreu!')
                    log = f'{message.author.name} tentou adicionar o usuário {content[0]} a planilha e um erro fatal ocorreu!'
                    return
    
                self.log(log)
            


        #bot indica que está online
        if message.content.startswith('!test'):
            await message.channel.send('To vivo!')
            return
        
        

        


