# ================================================================================ #
#                                                                                  #
# Ficheiro:      telegram.py                                                       #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Integração do bot com o Telegram. Responsável por enviar          #
#                notificações e alertas (entradas/saídas, erros, avisos) para      #
#                o chat configurado, usando a API oficial de bots do Telegram.     #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #

import requests
from logger import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Cria uma sessão HTTP persistente (em vez de abrir uma ligação nova a cada pedido),
# o que melhora a performance quando há muitos envios de mensagens.
session = requests.Session()
session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

# ================================================================================ #
# ------------------ MENSAGEM PARA TELEGRAM USANDO API DOS BOTS ------------------ #
# ================================================================================ #

def enviar_telegram(mensagem):
    """
    Envia uma mensagem para o Telegram usando a API de bots.
    """
    # Verifica se o token e o chat ID foram configurados
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Token ou Chat ID do Telegram não estão definidos.")
        return

    # Endpoint da API oficial do Telegram para envio de mensagens
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Dados do pedido: para quem enviar, texto, formato e opções
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,     # ID do utilizador/grupo de destino
        "text": mensagem,                # Mensagem propriamente dita
        "parse_mode": "HTML",            # Permite usar formatação HTML
        "disable_web_page_preview": True # Impede mostrar pré-visualizações de links
    }

    try:
        # Log detalhado antes de enviar
        logger.debug(f"Enviando para Telegram: {mensagem}")
        
        # Envia a mensagem via POST com timeout de 5 segundos
        response = session.post(url, data=payload, timeout=5)

        # Verifica se o envio foi bem-sucedido
        if response.ok:
            logger.info("✅ Mensagem enviada para o Telegram com sucesso.")
        else:
            logger.error(f"❌ Erro ao enviar mensagem para o Telegram. "
                         f"Status: {response.status_code}, Detalhes: {response.text}")

    except requests.RequestException as e:
        # Captura qualquer erro de rede ou exceção do requests
        logger.exception(f"[Telegram] Exceção ao tentar enviar mensagem: {e}")
