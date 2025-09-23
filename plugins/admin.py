# ================================================================================ #
#                                                                                  #
# Ficheiro:      admin.py                                                          #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Gestão de administradores do bot IRC. Fornece funções para        #
#                verificar se um determinado nick possui permissões de admin,      #
#                com base na lista definida em config.py.                          #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #

from config import ADMINS  # Importa a lista de administradores definida no config.py

# Cria um conjunto com todos os nicks de administradores em minúsculas
# Isto permite que a verificação seja insensível a maiúsculas/minúsculas
# e torna a pesquisa mais rápida do que percorrer uma lista.
ADMINS_LOWER = {admin.lower() for admin in ADMINS}

# Função que verifica se um nick é administrador
# Recebe como argumento o nick (string) e retorna True se estiver na lista,
# caso contrário retorna False.
# Exemplo: is_admin("nickname") → True
def is_admin(nick: str) -> bool:
    return nick.lower() in ADMINS_LOWER
