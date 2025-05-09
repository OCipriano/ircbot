import requests
from logger import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Criar uma sessão persistente (melhora performance em múltiplos envios)
session = requests.Session()
session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

def enviar_telegram(mensagem):
    """
    Envia uma mensagem para o Telegram usando a API de bots.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Token ou Chat ID do Telegram não estão definidos.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        logger.debug(f"Enviando para Telegram: {mensagem}")
        response = session.post(url, data=payload, timeout=5)

        if response.ok:
            logger.info("✅ Mensagem enviada para o Telegram com sucesso.")
        else:
            logger.error(f"❌ Erro ao enviar mensagem para o Telegram. "
                         f"Status: {response.status_code}, Detalhes: {response.text}")

    except requests.RequestException as e:
        logger.exception(f"[Telegram] Exceção ao tentar enviar mensagem: {e}")
