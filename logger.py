import logging

# Configura o logger
logger = logging.getLogger("BotLogger")
logger.setLevel(logging.DEBUG)  # Nível mínimo de logs

# Manipulador para ficheiro de log
file_handler = logging.FileHandler("bot.log", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_format)

# Manipulador para a consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(file_format)

# Adiciona os manipuladores ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
