# ================================================================================ #
#                                                                                  #
# Ficheiro:      bot.py                                                            #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Bot IRC com comandos de estatísticas, mapas, armas, destaques     #
#                e regras, além de gestão de novos membros e alertas via Telegram. #
#                Inclui reconexão automática, limitação de comandos por utilizador #
#                e suporte a múltiplos canais.                                     #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #
#                                                                                  #
# Funcionalidades principais:                                                      #
#   01. !op <nick>	            - Dá op a um utilizador (admin)                    #
#   02. !deop <nick>	        - Remove op (admin)                                #
#   03. !voice <nick>	        - Dá voz (admin)                                   #
#   04. !devoice <nick>	        - Remove voz (admin)                               #
#   05. !kick <nick> <motivo>	- Expulsa um utilizador (admin)                    #
#   06. !ban <nick> <motivo>	- Bane e expulsa (admin)                           #
#   07. !kb <nick> <motivo>	    - Ban + kick (admin)                               #
#   08. !unban <nick>	        - Remove ban (admin)                               #
#   09. !invite <nick>	        - Convida utilizador (admin)                       #
#   10. !topic <novo tópico>	- Altera tópico (admin)                            #
#   11. !status <nick>	        - Mostra se o nick é admin                         #
#   12. !seen <nick>	        - Última vez que foi visto                         #
#   13. !crypto <símbolo>	    - Preço de criptomoedas                            #
#   14. !ajuda	                - Mostra todos os comandos                         #
#   15. !join <#canal>	        - Bot entra num canal (admin)                      #
#   16. !part <#canal>	        - Bot sai de um canal (admin)                      #
#                                                                                  #
# Observações:                                                                     #
#   - O bot usa asyncio para processamento assíncrono e reconexão automática.      #
#   - Limita comandos por utilizador para prevenir spam.                           #
#   - Integração com Telegram via função enviar_telegram() para notificações.      #
#   - Necessário definir variáveis de configuração em config.py (SERVER, PORT,     #
#     NICK, PASSWORD, CANAIS, etc.).                                               #
#   - Plugins externos (seen, commands, telegram) devem estar implementados.       #
#                                                                                  #
# ================================================================================ #

from logger import logger
import signal
import sys
import asyncio
import ssl
import irc.client
import irc.connection
import threading
import time

# ================================================================================ #
# ------------------ IMPORTA VARIÁVEIS DE CONFIGURAÇÃO E PLUGINS ----------------- #
# ================================================================================ #

from config import SERVER, PORT, NICK, PASSWORD, CANAIS, CANAIS_COM_ALERTAS, BOAS_VINDAS
from plugins.seen import log_seen, init_db
from plugins.commands import executar_comando
from plugins.telegram import enviar_telegram

# ================================================================================ #
# --------------------- CORRIGIR EVENT LOOP APENAS NO WINDOWS -------------------- #
# ================================================================================ #

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ================================================================================ #
# ---------------------------- CLASSE PRINCIPAL DO BOT --------------------------- #
# ================================================================================ #

class IRCBot:
    def __init__(self):
        logger.info("Inicializando o bot IRC.")
        self.reactor = irc.client.Reactor()
        self.user_commands = {}
        self.running = True

        self.loop = asyncio.get_event_loop()
        self._connect()

    # ============================================================================ #
    # ---- Cria a ligação segura ao servidor IRC e associa handlers a eventos ---- #
    # ============================================================================ #
    
    def _connect(self):
        factory = irc.connection.Factory(
            wrapper=lambda sock: ssl.create_default_context().wrap_socket(sock, server_hostname=SERVER)
        )
        self.connection = self.reactor.server().connect(SERVER, PORT, NICK, connect_factory=factory)

        # ======================================================================== #
        # ----------------------- Associa eventos a funções ---------------------- #
        # ======================================================================== #
        
        self.connection.add_global_handler("welcome", self.on_welcome)
        self.connection.add_global_handler("pubmsg", self.on_pubmsg)
        self.connection.add_global_handler("privmsg", self.on_privmsg)
        self.connection.add_global_handler("join", self.on_join)
        self.connection.add_global_handler("part", self.on_part)
        self.connection.add_global_handler("nicknameinuse", self.on_nickname_in_use)
        self.connection.add_global_handler("disconnect", self.on_disconnect)

    # ============================================================================ #
    # ---------------------- Handler para nickname já em uso --------------------- #
    # ============================================================================ #
    
    def on_nickname_in_use(self, connection, event):
        logger.info("Nickname já está em uso.")
        connection.nick(NICK + "_")

    # ============================================================================ #
    # ----------------- Handler quando o bot se liga com sucesso ----------------- #
    # ============================================================================ #
    
    def on_welcome(self, connection, event):
        logger.info("Ligado com sucesso ao servidor.")
        # Identifica-se no NickServ
        connection.privmsg("NickServ", f"IDENTIFY {NICK} {PASSWORD}")
        # Junta-se a todos os canais definidos
        for canal in CANAIS:
            logger.info(f"A entrar no canal: {canal}")
            connection.join(canal)
        # Notifica via Telegram
        enviar_telegram("✅ O bot ligou-se com sucesso ao IRC.")

    # ============================================================================ #
    # -------------------- Handler quando o bot é desconectado ------------------- #
    # ============================================================================ #
    
    def on_disconnect(self, connection, event):
        logger.warning("Desconectado do servidor.")
        try:
            enviar_telegram("⚠️ O bot foi desconectado do servidor IRC.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação para Telegram: {e}")
        # Tenta reconectar de forma assíncrona
        asyncio.create_task(self.reconectar())

    # ============================================================================ #
    # ------------- Função assíncrona para reconectar automaticamente ------------ #
    # ============================================================================ #
    
    async def reconectar(self, tentativas=5):  # Espera 5 segundos entre tentativas
        for tentativa in range(tentativas):
            await asyncio.sleep(5)
            logger.info(f"Tentativa de reconexão {tentativa + 1} de {tentativas}...")
            try:
                self._connect()
                logger.info("Reconectado com sucesso.")
                return
            except Exception as e:
                logger.error(f"Erro ao tentar reconectar: {e}")
        enviar_telegram("❌ Falha ao reconectar após várias tentativas.")

    # ============================================================================ #
    # ---------------------- Handler para mensagens públicas --------------------- #
    # ============================================================================ #
    
    def on_pubmsg(self, connection, event):
        source = event.source.nick  # Nick do utilizador
        target = event.target       # Canal da mensagem
        message = event.arguments[0]
        logger.debug(f"Mensagem pública de {source} em {target}: {message}")

        log_seen(source)  # Regista que este nick falou recentemente
        
        # Limita a 5 comandos por minuto
        if self.user_commands.get(source, 0) >= 5:
            logger.warning(f"{source} excedeu o limite de comandos.")
            return

        # Se for comando, executa
        if message.startswith("!"):
            self.user_commands[source] = self.user_commands.get(source, 0) + 1
            asyncio.create_task(self.reset_user_command_count(source))  # Reset após 60s
            partes = message.split()
            comando = partes[0].lower()
            args = partes[1:]
            logger.info(f"Comando recebido: {comando} de {source} em {target} com args: {args}")
            asyncio.create_task(executar_comando(self, source, comando, args, target))

    # ============================================================================ #
    # --------- Reseta o contador de comandos do utilizador após um delay -------- #
    # ============================================================================ #
    
    async def reset_user_command_count(self, user, delay=60):
        await asyncio.sleep(delay)
        self.user_commands.pop(user, None)

    # ============================================================================ #
    # ---------------------- Handler para mensagens privadas --------------------- #
    # ============================================================================ #
    
    def on_privmsg(self, connection, event):
        source = event.source.nick
        message = event.arguments[0]
        target = source  # Responde na própria mensagem
        logger.debug(f"Mensagem privada de {source}: {message}")

        if message.startswith("!"):
            partes = message.split()
            comando = partes[0].lower()
            args = partes[1:]
            logger.info(f"Comando privado recebido: {comando} de {source} com args: {args}")
            asyncio.create_task(executar_comando(self, source, comando, args, target))

    # ============================================================================ #
    # ---------------------- Handler para entrada em canais ---------------------- #
    # ============================================================================ #
    
    def on_join(self, connection, event):
        nick = event.source.nick
        canal = event.target
        logger.debug(f"{nick} entrou no canal {canal}")

        # Boas-vindas personalizadas
        if canal in BOAS_VINDAS and nick != NICK:
            try:
                mensagem = BOAS_VINDAS[canal].format(nick=nick)
                self.message(canal, mensagem)
                logger.debug(f"Enviado mensagem de boas-vindas para {nick} em {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

        # Alertas via Telegram
        if canal in CANAIS_COM_ALERTAS and nick != NICK:
            try:
                enviar_telegram(f"👤 <b>{nick}</b> entrou no canal <b>{canal}</b>.")
                logger.debug(f"Enviado alerta para Telegram: {nick} entrou em {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

    # ============================================================================ #
    # ----------------------- Handler para saída de canais ----------------------- #
    # ============================================================================ #
    
    def on_part(self, connection, event):
        nick = event.source.nick
        canal = event.target
        logger.debug(f"{nick} saiu do canal {canal}")

        # Notifica se o bot saiu
        if nick == NICK:
            try:
                enviar_telegram(f"👋 O bot saiu do canal <b>{canal}</b>.")
                logger.debug(f"O bot saiu do canal {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

    # ============================================================================ #
    # ----------- Função para enviar mensagem a um canal ou utilizador ----------- #
    # ============================================================================ #
    
    def message(self, target, text):
        try:
            logger.info(f"Enviando mensagem para {target}: {text}")
            self.connection.privmsg(target, text)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {target}: {e}")
        
    # ============================================================================ #
    # ---------------------------- Para encerrar o bot --------------------------- #
    # ============================================================================ #
    
    def stop(self):
        logger.info("Encerrando o bot...")
        self.running = False
        try:
            self.connection.quit("Bot encerrado.")
        except Exception as e:
            logger.error(f"Erro ao encerrar conexão IRC: {e}")

    # ============================================================================ #
    # ------------------------- Loop principal assíncrono ------------------------ #
    # ============================================================================ #
    
    async def start(self):
        logger.info("Iniciando o loop do bot.")
        while self.running:
            self.reactor.process_once(timeout=0.2)  # Processa eventos IRC
            await asyncio.sleep(0.1)

    # ============================================================================ #
    # ------------------------ Funções administrativas IRC ----------------------- #
    # ============================================================================ #
    
    async def set_mode(self, canal, modo, nick):
        logger.info(f"Definindo modo {modo} para {nick} em {canal}")
        self.connection.mode(canal, f"{modo} {nick}")

    async def kick(self, canal, nick, motivo=""):
        logger.info(f"Expulsando {nick} de {canal} com motivo: {motivo}")
        self.connection.kick(canal, nick, motivo)

    async def invite(self, nick, canal):
        logger.info(f"Enviando convite para {nick} para o canal {canal}")
        self.connection.invite(nick, canal)

    async def set_topic(self, canal, topico):
        logger.info(f"Definindo tópico de {canal} para: {topico}")
        self.connection.topic(canal, topico)

# ================================================================================ #
# -------------------------- FUNÇÃO PRINCIPAL ASSÍNCRONA ------------------------- #
# ================================================================================ #

async def main():
    bot = IRCBot()

    # ============================================================================ #
    # ------ Função para encerrar graciosamente ao receber SIGINT ou SIGTERM ----- #
    # ============================================================================ #
    
    def desligar_graciosamente(signalnum, frame):
        logger.info("Sinal de encerramento recebido.")
        try:
            enviar_telegram("⚠️ O bot foi encerrado manualmente ou pelo sistema.")
            time.sleep(1)  # Dá tempo para a mensagem sair antes do encerramento
        except Exception as e:
            logger.error(f"Erro ao enviar notificação para Telegram: {e}")
        bot.stop()
        sys.exit(1)

    signal.signal(signal.SIGINT, desligar_graciosamente)
    signal.signal(signal.SIGTERM, desligar_graciosamente)

    logger.info("Bot em execução. Pressiona CTRL+C para sair.")
    await bot.start()

# ================================================================================ #
# ---------------------------------- ENTRY POINT --------------------------------- #
# ================================================================================ #

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Erro inesperado.")
        try:
            enviar_telegram(f"❌ Ocorreu um erro inesperado no bot: {e}. Verifica o log para mais detalhes.")
        except:
            pass
        sys.exit(1)
