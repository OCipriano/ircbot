<h1 align="center">IRC Bot com Integração Telegram e Plugins</h1>
<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/JSON-000?style=for-the-badge&logo=json&logoColor=fff" />
  <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/Notepad++-90E59A.svg?style=for-the-badge&logo=notepad%2b%2b&logoColor=black" />
  <img src="https://img.shields.io/badge/-Raspberry_Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi" />
  <img src="https://img.shields.io/badge/status-active-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
</p>
<p align="center">
Este projeto é um bot IRC modular com funcionalidades extensíveis através de plugins, integração com o Telegram e suporte a comandos, logging e gestão de estado de utilizadores.
</p>

---

### 🔧 Funcionalidades Principais

	• Conexão segura via SSL a servidores IRC
	• Entrada automática em canais definidos
	• Autenticação via NickServ
	• Reconexão automática em caso de falha
	• Comandos personalizados acessíveis por chat
	• Plugins modulares para extensão de funcionalidades
	• Notificações para Telegram
	• Sistema de permissões por administradores
	• Limite de uso de comandos por utilizador para evitar spam
	• Suporte a comandos privados e públicos
	• Boas-vindas personalizadas e alertas de entrada/saída enviados para o Telegram
	• Logging detalhado para consola e ficheiro

### 📁 Estrutura do Projeto

```
projeto/
    ├── bot.py                 # Ponto de entrada do bot
    ├── config.py              # Configurações gerais e variáveis de ambiente
    ├── logger.py              # Configuração do sistema de logging
    ├── requirements.txt       # Dependências Python
    ├── .env                   # Variáveis de ambiente (ignorado pelo Git)
    ├── plugins/               # Diretório de plugins
        ├── admin.py           # Comandos administrativos
        ├── commands.py        # Gestião de comandos gerais
        ├── crypto.py          # Informações sobre criptomoedas
        ├── misc.py            # Funcionalidades diversas
        ├── seen.py            # Rastreio de atividade de utilizadores
        ├── telegram.py        # Integração com Telegram
        └── __init__.py        # Define o módulo de plugins
```

### 🚀 Começar

1. Clonar o repositório

	```bash
	git clone https://github.com/ocipriano/bot_irc.git
	cd bot_irc
	```

2. Criar e configurar o .env

	```env
	IRC_NICK=TeuNick
	IRC_SERVER=irc.ptnet.org
	IRC_PORT=6697
	IRC_PASSWORD=senhaNickServ
	CANAIS=#portugal,#crypto
	IRC_ADMINS=admin1,admin2

	TELEGRAM_BOT_TOKEN=teu_token
	TELEGRAM_CHAT_ID=teu_chat_id
	CANAIS_COM_ALERTAS=#portugal,#crypto
	```

3. Instalar dependências

	```bash
	pip install -r requirements.txt
	```

4. Executar o bot

	```bash
	python bot.py
	```

### 📌 Comandos

| Comando                 | Descrição                     |
| ----------------------- | ----------------------------- |
| `!op <nick>`            | Dá op a um utilizador (admin) |
| `!deop <nick>`          | Remove op (admin)             |
| `!voice <nick>`         | Dá voz (admin)                |
| `!devoice <nick>`       | Remove voz (admin)            |
| `!kick <nick> <motivo>` | Expulsa um utilizador (admin) |
| `!ban <nick> <motivo>`  | Bane e expulsa (admin)        |
| `!kb <nick> <motivo>`   | Ban + kick (admin)            |
| `!unban <nick>`         | Remove ban (admin)            |
| `!invite <nick>`        | Convida utilizador (admin)    |
| `!topic <novo tópico>`  | Altera tópico (admin)         |
| `!status <nick>`        | Mostra se o nick é admin      |
| `!seen <nick>`          | Última vez que foi visto      |
| `!crypto <símbolo>`     | Preço de criptomoedas         |
| `!ajuda`                | Mostra todos os comandos      |
| `!join <#canal>`        | Bot entra num canal (admin)   |
| `!part <#canal>`        | Bot sai de um canal (admin)   |


### 📈 Logs

	Todos os eventos importantes são gravados em:

	bot.log

### ✅ Requisitos

	• Python 3.8+
	• Acesso a servidor IRC com SSL
	• Bot Telegram e chat ID (opcional)
	
### 🚫 Avisos

	• Não partilhes o ficheiro .env com terceiros.
	• Usa um nick autorizado no servidor IRC.

## Contribuição

	Contribuições são bem-vindas! Se quiseres contribuir para o projeto, abre um pull request ou envia um issue.

	Passos para contribuir:
	• Cria um fork do repositório.
	• Cria uma branch para a tua feature (git checkout -b minha-feature).
	• Comita as tuas alterações (git commit -am 'Adiciona nova feature').
	• Faz push para a tua branch (git push origin minha-feature).
	• Cria um pull request.
	
### 📜 Licença

	Projeto livre para uso pessoal e educacional. Para fins comerciais, contactar o autor.
