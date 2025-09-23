# ================================================================================ #
#                                                                                  #
# Ficheiro:      config.py                                                         #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Configurações do bot IRC: ligação ao servidor, canais, admins,    #
#                integração com Telegram e mensagens de boas-vindas.               #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #

import os
from dotenv import load_dotenv

# ================================================================================ #
# ------------------------ CARREGAR VARIÁVEIS DE AMBIENTE ------------------------ #
# ================================================================================ #

load_dotenv()

# Canais onde o bot deve entrar
CANAIS = os.getenv("CANAIS", "#portugal,#crypto").split(",")

# ================================================================================ #
# ----------------------------- DADOS DA LIGAÇÃO IRC ----------------------------- #
# ================================================================================ #

# Nickname que o bot vai usar no servidor IRC
NICK = os.getenv("IRC_NICK", "nickname")

# Endereço do servidor IRC
SERVER = os.getenv("IRC_SERVER", "irc.ptnet.org")

# Porta de ligação (6697 = SSL/TLS; 6667 = não segura)
PORT = int(os.getenv("IRC_PORT", "6697"))

# Palavra-passe para identificação no NickServ (se configurada)
PASSWORD = os.getenv("IRC_PASSWORD", "password")

# ================================================================================ #
# ----------------------------- PERMISSÕES DE ADMIN ------------------------------ #
# ================================================================================ #

# Lista de utilizadores (nicks) com permissões administrativas no bot
ADMINS = os.getenv("IRC_ADMINS", "admin,admin1").split(",")

# ================================================================================ #
# --------------------------- CONFIGURAÇÃO DO TELEGRAM --------------------------- #
# ================================================================================ #

# Token do bot Telegram (necessário para enviar mensagens)
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "0123456789:AAAAAAAAAAAAAAAAA-AAAAAAAAAAAAAAAAA"
)

# Chat ID ou grupo para onde o bot enviará notificações
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "0123456789")

# ================================================================================ #
# --------------------------- MENSAGENS DE BOAS-VINDAS --------------------------- #
# ================================================================================ #

# Dicionário com mensagens personalizadas por canal
# {nick} será substituído pelo nome do utilizador que entrou
BOAS_VINDAS = {
    "#portugal": "🌅 Olá {nick}, seja bem-vindo(a) ao canal de Portugal.",
    "#crypto": "💻 Bem-vindo(a), {nick}! Este é o canal de crypto. Fique à vontade para perguntar ou ajudar."
}

# ================================================================================ #
# ----------------------- CANAIS COM ALERTAS PARA TELEGRAM ----------------------- #
# ================================================================================ #

# Lista de canais onde devem ser enviados alertas de entradas/saídas para o Telegram
# Por defeito, usa os mesmos canais definidos em CANAIS
CANAIS_COM_ALERTAS = os.getenv("CANAIS_COM_ALERTAS", ",".join(CANAIS)).split(",")
