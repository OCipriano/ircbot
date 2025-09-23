# ================================================================================ #
#                                                                                  #
# Ficheiro:      config.py                                                         #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Configurações de logging para o bot IRC. Define o formato e o     #
#                destino das mensagens de log (ficheiro e consola).                #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #

import logging

# Cria um logger com o nome "BotLogger"
logger = logging.getLogger("BotLogger")

# Define o nível mínimo de mensagens a registar (DEBUG = mostra tudo)
logger.setLevel(logging.DEBUG)

# ================================================================================ #
# ------------------------------- LOG PARA FICHEIRO ------------------------------ #
# ================================================================================ #

# Cria um manipulador para escrever logs num ficheiro (bot.log)
# encoding='utf-8' garante suporte a caracteres especiais
file_handler = logging.FileHandler("bot.log", encoding='utf-8')

# Define que este manipulador regista todas as mensagens a partir de DEBUG
file_handler.setLevel(logging.DEBUG)

# Define o formato das mensagens de log:
# Exemplo → 2025-07-23 14:35:12 - INFO - Ligado ao servidor
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_format)

# ================================================================================ #
# ------------------------------- LOG PARA CONSOLA ------------------------------- #
# ================================================================================ #

# Cria um manipulador para mostrar logs diretamente na consola/terminal
console_handler = logging.StreamHandler()

# Este manipulador só mostra mensagens a partir de INFO (ignora DEBUG)
console_handler.setLevel(logging.INFO)

# Usa o mesmo formato definido acima
console_handler.setFormatter(file_format)

# ================================================================================ #
# -------------------------------- ATIVAR LOGGING -------------------------------- #
# ================================================================================ #

# Adiciona os dois manipuladores (ficheiro + consola) ao logger principal
logger.addHandler(file_handler)
logger.addHandler(console_handler)
