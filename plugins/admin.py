from config import ADMINS  # Importa a lista de administradores definida no config.py

# Prepara um conjunto de administradores em minúsculas para busca rápida
ADMINS_LOWER = {admin.lower() for admin in ADMINS}

# Verifica se o nick pertence à lista de administradores (case-insensitive)
def is_admin(nick: str) -> bool:
    return nick.lower() in ADMINS_LOWER
