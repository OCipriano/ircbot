# ================================================================================ #
#                                                                                  #
# Ficheiro:      crypto.py                                                         #
# Autor:         NunchuckCoder                                                     #
# Versão:        1.0                                                               #
# Data:          Julho 2025                                                        #
# Descrição:     Módulo para consulta de preços de criptomoedas em tempo real,     #
#                utilizando a API pública da Binance. Dá suporte a pares EUR e     #
#                USD (via USDT). Retorna mensagens formatadas para o bot IRC.      #
# Licença:       MIT License                                                       #
#                                                                                  #
# ================================================================================ #

import aiohttp     # Biblioteca assíncrona para requests HTTP
import asyncio     # Usada para gestão de timeouts e exceções assíncronas

# Função assíncrona para obter o preço de uma criptomoeda
# symbol -> ticker da moeda (ex: BTC, ETH)
async def get_crypto_price(symbol):
    try:
        async with aiohttp.ClientSession() as session:
            # Primeiro tenta obter o preço no par com EUR
            url_price_eur = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}EUR"
            async with session.get(url_price_eur, timeout=10) as res:
                data = await res.json()
                if 'price' in data:
                    return f"💶 {symbol.upper()}: {float(data['price']):.8f} EUR"

            # Se não existir par em EUR, tenta no par USDT (equivalente a USD)
            url_price_usd = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
            async with session.get(url_price_usd, timeout=10) as res:
                data = await res.json()
                if 'price' in data:
                    return f"💲 {symbol.upper()}: {float(data['price']):.8f} USD"

            # Se nenhum dos pares for encontrado, devolve aviso
            return f"⚠️ Moeda '{symbol.upper()}' não encontrada."

    # --- Tratamento de erros específicos ---
    except asyncio.TimeoutError:
        return "⏳ Timeout ao contactar a Binance. Tente novamente mais tarde."
    except aiohttp.ClientError:
        return "❌ Erro de rede ao tentar contactar a Binance."
    except Exception as e:
        # Captura qualquer erro inesperado (ex.: resposta inválida)
        return f"⚠️ Ocorreu um erro: {e}"
