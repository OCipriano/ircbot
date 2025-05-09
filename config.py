import os
from dotenv import load_dotenv

# Carrega variáveis do ficheiro .env (se existir)
load_dotenv()

# Canais onde o bot deve entrar
CANAIS = os.getenv("CANAIS", "#portugal,#crypto").split(",")

# Dados da ligação IRC
NICK = os.getenv("IRC_NICK", "nickname")
SERVER = os.getenv("IRC_SERVER", "irc.ptnet.org")
PORT = int(os.getenv("IRC_PORT", "6697"))  # SSL (usa 6667 para ligação não segura)
PASSWORD = os.getenv("IRC_PASSWORD", "password")

# Lista de nicks com permissões de administrador
ADMINS = os.getenv("IRC_ADMINS", "admin,admin1").split(",")

# Configuração do Telegram para notificações
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "0123456789:AAAAAAAAAAAAAAAAA-AAAAAAAAAAAAAAAAA")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "0123456789")

# Mensagens de boas-vindas por canal (usa o nome exato do canal)
BOAS_VINDAS = {
    "#portugal": "🌅 Olá {nick}, seja bem-vindo(a) ao canal de Portugal.",
    "#crypto": "💻 Bem-vindo(a), {nick}! Este é o canal de crypto. Fique à vontade para perguntar ou ajudar."
}

# Canais onde devem ser enviados alertas de entradas e saídas
CANAIS_COM_ALERTAS = os.getenv("CANAIS_COM_ALERTAS", ",".join(CANAIS)).split(",")
