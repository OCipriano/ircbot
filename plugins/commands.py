from plugins.admin import is_admin  # Verifica se um utilizador tem permissões de administrador
from plugins import seen  # Plugin que regista e consulta a última vez que um utilizador foi visto
from plugins.crypto import get_crypto_price  # Função para obter o preço de criptomoedas

seen.init_db()  # Garante que a base de dados está inicializada

# Função principal que executa o comando com base na mensagem recebida
async def executar_comando(bot, source, comando, args, target):
    canal = target   # O destino da mensagem (canal ou utilizador)

    def sem_permissao():
        bot.message(canal, "🚫 Sem permissão para executar este comando.")

    def uso_comando(correto):
        bot.message(canal, f"ℹ️ Uso correto: {correto}")

    # Usa pattern matching (Python 3.10+) para identificar comandos
    match comando:
        
        # Dá op a um utilizador
        case '!op' | '!up':
            if is_admin(source):
                nick = args[0] if args else source
                await bot.set_mode(canal, '+o', nick)
            else:
                sem_permissao()

        # Remove op
        case '!deop' | '!down':
            if is_admin(source):
                nick = args[0] if args else source
                await bot.set_mode(canal, '-o', nick)
            else:
                sem_permissao()

        # Dá voice
        case '!voice':
            if is_admin(source) and args:
                await bot.set_mode(canal, '+v', args[0])
            else:
                uso_comando("!voice <nick>")

        # Remove voice
        case '!devoice':
            if is_admin(source) and args:
                await bot.set_mode(canal, '-v', args[0])
            else:
                uso_comando("!devoice <nick>")

        # Expulsa um utilizador com motivo
        case '!kick' | '!k':
            if is_admin(source) and len(args) >= 2:
                nick, motivo = args[0], ' '.join(args[1:])
                await bot.kick(canal, nick, motivo)
            else:
                uso_comando("!kick <nick> <motivo>")

        # Bane e expulsa
        case '!ban':
            if is_admin(source) and len(args) >= 2:
                nick, motivo = args[0], ' '.join(args[1:])
                await bot.set_mode(canal, '+b', f'{nick}!*@*')
                await bot.kick(canal, nick, motivo)
            else:
                uso_comando("!ban <nick> <motivo>")

        # Ban + kick (atalho)
        case '!kb':
            if is_admin(source) and len(args) >= 2:
                nick, motivo = args[0], ' '.join(args[1:])
                await bot.set_mode(canal, '+b', f'{nick}!*@*')
                await bot.kick(canal, nick, motivo)
            else:
                uso_comando("!kb <nick> <motivo>")

        # Remove ban
        case '!unban':
            if is_admin(source) and args:
                await bot.set_mode(canal, '-b', f'{args[0]}!*@*')
            else:
                uso_comando("!unban <nick>")

        # Envia convite para o canal
        case '!invite':
            if is_admin(source) and args:
                await bot.invite(args[0], canal)
            else:
                uso_comando("!invite <nick>")

        # Altera o tópico do canal
        case '!topic':
            if is_admin(source) and args:
                await bot.set_topic(canal, ' '.join(args))
            else:
                uso_comando("!topic <novo tópico>")

        # Verifica se o utilizador é admin
        case '!status':
            nick = args[0] if args else source
            nivel = "Administrador" if is_admin(nick) else "Usuário comum"
            bot.message(canal, f"Status de {nick}: {nivel}")

        # Consulta quando foi a última vez que um nick foi visto
        case '!seen':
            if args:
                ultima_vez = seen.get_seen(args[0])
                bot.message(canal, ultima_vez)
            else:
                bot.message(canal, "ℹ️ Uso correto: !seen <nick>")

        # Consulta o preço de uma criptomoeda
        case '!crypto':
            if args:
                resultado = await get_crypto_price(args[0])
                bot.message(canal, resultado)
            else:
                uso_comando("!crypto <símbolo>")

        # Lista de comandos disponíveis com descrição detalhada
        case '!ajuda':
            ajuda = [
                ("🤖 Comandos disponíveis:",""),
                ("!op <nick>", "Dá op a um utilizador (admin apenas)."),
                ("!deop <nick>", "Remove op de um utilizador (admin apenas)."),
                ("!voice <nick>", "Dá voz a um utilizador (admin apenas)."),
                ("!devoice <nick>", "Remove a voz de um utilizador (admin apenas)."),
                ("!kick <nick> <motivo>", "Expulsa um utilizador com motivo (admin apenas)."),
                ("!ban <nick> <motivo>", "Bane e expulsa um utilizador (admin apenas)."),
                ("!kb <nick> <motivo>", "Atalho para ban + kick (admin apenas)."),
                ("!unban <nick>", "Remove um ban (admin apenas)."),
                ("!invite <nick>", "Envia um convite para o canal (admin apenas)."),
                ("!topic <novo tópico>", "Altera o tópico do canal (admin apenas)."),
                ("!status <nick>", "Mostra se o nick é admin ou não."),
                ("!seen <nick>", "Informa a última vez que o nick foi visto."),
                ("!crypto <símbolo>", "Mostra o preço atual de uma criptomoeda.")
            ]
            for comando, descricao in ajuda:
                bot.message(canal, f"{comando} – {descricao}")
         
        # Comando para o bot entrar num canal
        case '!join':
            if is_admin(source):
                if args:
                    novo_canal = args[0]
                    bot.connection.join(novo_canal)
                    bot.message(canal, f"✅ A entrar em {novo_canal}")
                else:
                    uso_comando("!join <#canal>")
            else:
                sem_permissao()

        # Comando para o bot sair de um canal
        case '!part':
            if is_admin(source):
                if args:
                    sair_canal = args[0]
                    bot.connection.part(sair_canal)
                    bot.message(canal, f"👋 A sair de {sair_canal}")
                else:
                    uso_comando("!part <#canal>")
            else:
                sem_permissao()
                
        # Comando desconhecido
        case _:
            bot.message(canal, "❓ Comando desconhecido. Use !ajuda.")