import aiohttp
import asyncio

async def get_crypto_price(symbol):
    try:
        async with aiohttp.ClientSession() as session:
            # Tentar obter o preço em EUR
            url_price_eur = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}EUR"
            async with session.get(url_price_eur, timeout=10) as res:
                data = await res.json()
                if 'price' in data:
                    return f"💶 {symbol.upper()}: {float(data['price']):.8f} EUR"

            # Se não existir em EUR, tentar USD
            url_price_usd = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
            async with session.get(url_price_usd, timeout=10) as res:
                data = await res.json()
                if 'price' in data:
                    return f"💲 {symbol.upper()}: {float(data['price']):.8f} USD"

            return f"⚠️ Moeda '{symbol.upper()}' não encontrada."

    except asyncio.TimeoutError:
        return "⏳ Timeout ao contactar a Binance. Tente novamente mais tarde."
    except aiohttp.ClientError:
        return "❌ Erro de rede ao tentar contactar a Binance."
    except Exception as e:
        return f"⚠️ Ocorreu um erro: {e}"