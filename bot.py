from logger import logger
import signal
import sys
import asyncio
import ssl
import irc.client
import irc.connection
import threading
import time

from config import SERVER, PORT, NICK, PASSWORD, CANAIS, CANAIS_COM_ALERTAS, BOAS_VINDAS
from plugins.seen import log_seen, init_db
from plugins.commands import executar_comando
from plugins.telegram import enviar_telegram

# Compatibilidade com Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class IRCBot:
    def __init__(self):
        logger.info("Inicializando o bot IRC.")
        self.reactor = irc.client.Reactor()
        self.user_commands = {}
        self.running = True

        self.loop = asyncio.get_event_loop()
        self._connect()

    def _connect(self):
        factory = irc.connection.Factory(
            wrapper=lambda sock: ssl.create_default_context().wrap_socket(sock, server_hostname=SERVER)
        )
        self.connection = self.reactor.server().connect(SERVER, PORT, NICK, connect_factory=factory)

        self.connection.add_global_handler("welcome", self.on_welcome)
        self.connection.add_global_handler("pubmsg", self.on_pubmsg)
        self.connection.add_global_handler("privmsg", self.on_privmsg)
        self.connection.add_global_handler("join", self.on_join)
        self.connection.add_global_handler("part", self.on_part)
        self.connection.add_global_handler("nicknameinuse", self.on_nickname_in_use)
        self.connection.add_global_handler("disconnect", self.on_disconnect)

    def on_nickname_in_use(self, connection, event):
        logger.info("Nickname já está em uso.")
        connection.nick(NICK + "_")

    def on_welcome(self, connection, event):
        logger.info("Ligado com sucesso ao servidor.")
        connection.privmsg("NickServ", f"IDENTIFY {NICK} {PASSWORD}")
        for canal in CANAIS:
            logger.info(f"A entrar no canal: {canal}")
            connection.join(canal)
        enviar_telegram("✅ O bot ligou-se com sucesso ao IRC.")

    def on_disconnect(self, connection, event):
        logger.warning("Desconectado do servidor.")
        try:
            enviar_telegram("⚠️ O bot foi desconectado do servidor IRC.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação para Telegram: {e}")
        asyncio.create_task(self.reconectar())

    async def reconectar(self, tentativas=5):
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

    def on_pubmsg(self, connection, event):
        source = event.source.nick
        target = event.target
        message = event.arguments[0]
        logger.debug(f"Mensagem pública de {source} em {target}: {message}")

        log_seen(source)
        
        if self.user_commands.get(source, 0) >= 5:
            logger.warning(f"{source} excedeu o limite de comandos.")
            return

        if message.startswith("!"):
            self.user_commands[source] = self.user_commands.get(source, 0) + 1
            asyncio.create_task(self.reset_user_command_count(source))
            partes = message.split()
            comando = partes[0].lower()
            args = partes[1:]
            logger.info(f"Comando recebido: {comando} de {source} em {target} com args: {args}")
            asyncio.create_task(executar_comando(self, source, comando, args, target))

    async def reset_user_command_count(self, user, delay=60):
        await asyncio.sleep(delay)
        self.user_commands.pop(user, None)

    def on_privmsg(self, connection, event):
        source = event.source.nick
        message = event.arguments[0]
        target = source
        logger.debug(f"Mensagem privada de {source}: {message}")

        if message.startswith("!"):
            partes = message.split()
            comando = partes[0].lower()
            args = partes[1:]
            logger.info(f"Comando privado recebido: {comando} de {source} com args: {args}")
            asyncio.create_task(executar_comando(self, source, comando, args, target))

    def on_join(self, connection, event):
        nick = event.source.nick
        canal = event.target
        logger.debug(f"{nick} entrou no canal {canal}")

        if canal in BOAS_VINDAS and nick != NICK:
            try:
                mensagem = BOAS_VINDAS[canal].format(nick=nick)
                self.message(canal, mensagem)
                logger.debug(f"Enviado mensagem de boas-vindas para {nick} em {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

        if canal in CANAIS_COM_ALERTAS and nick != NICK:
            try:
                enviar_telegram(f"👤 <b>{nick}</b> entrou no canal <b>{canal}</b>.")
                logger.debug(f"Enviado alerta para Telegram: {nick} entrou em {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

    def on_part(self, connection, event):
        nick = event.source.nick
        canal = event.target
        logger.debug(f"{nick} saiu do canal {canal}")

        if nick == NICK:
            try:
                enviar_telegram(f"👋 O bot saiu do canal <b>{canal}</b>.")
                logger.debug(f"O bot saiu do canal {canal}")
            except Exception as e:
                logger.error(f"Erro ao enviar alerta para Telegram: {e}")

    def message(self, target, text):
        try:
            logger.info(f"Enviando mensagem para {target}: {text}")
            self.connection.privmsg(target, text)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {target}: {e}")
        
    def stop(self):
        logger.info("Encerrando o bot...")
        self.running = False
        try:
            self.connection.quit("Bot encerrado.")
        except Exception as e:
            logger.error(f"Erro ao encerrar conexão IRC: {e}")

    async def start(self):
        logger.info("Iniciando o loop do bot.")
        while self.running:
            self.reactor.process_once(timeout=0.2)
            await asyncio.sleep(0.1)

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

async def main():
    bot = IRCBot()

    def desligar_graciosamente(signalnum, frame):
        logger.info("Sinal de encerramento recebido.")
        try:
            enviar_telegram("⚠️ O bot foi encerrado manualmente ou pelo sistema.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação para Telegram: {e}")
        bot.stop()

    signal.signal(signal.SIGINT, desligar_graciosamente)
    signal.signal(signal.SIGTERM, desligar_graciosamente)

    logger.info("Bot em execução. Pressiona CTRL+C para sair.")
    await bot.start()

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
