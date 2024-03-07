from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging
import time
TOKEN = "СЮДА_ВВЕСТИ_ВАШ_ТОКЕН_ТГ"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

CRYPTA = ["BTC", "ETH", "BNB", "DOGE", "SHIB", "DOT", "TRX", "UNI", "LTC", "ADA"]
CRYPTOS = ["bitcoin", "ethereum", "binancecoin", "cardano", "dogecoin", "shiba-inu", "polkadot", "tron", "uniswap", "litecoin"]        
CURRENCIES = ["USD", "RUB"]

bot_messages_ids = []  # Список для хранения идентификаторов сообщений бота

def get_crypto_price(crypto, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency.lower()}"
    response = requests.get(url).json()
    price = response.get(crypto, {}).get(currency.lower(), 'Временно недоступно')
    return price
    
def start(update, context):
    time.sleep(0.2)  
    choice_crypto(update, context)

def choice_crypto(update, context):
    time.sleep(0.2)   
    keyboard = [CRYPTA[i:i + 5] for i in range(0, len(CRYPTA), 5)]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, row_width=5)
    message = update.message.reply_text('Выберите криптовалюту:', reply_markup=markup)
    
    bot_messages_ids.append(message.message_id) 

def handle_message(update, context):
    text = update.message.text.lower()
    message = ""
    if text.lower() == "btc": 
        text = "bitcoin"  
    elif text.lower() == "eth": 
        text = "ethereum"  
    elif text.lower() == "bnb":  
        text = "binancecoin"  
    elif text.lower() == "ada":  
        text = "cardano" 
    elif text.lower() == "doge":  
        text = "dogecoin"       
    elif text.lower() == "shib":
        text = "shiba-inu"
    elif text.lower() == "dot":
        text = "polkadot"
    elif text.lower() == "trx":
        text = "tron"
    elif text.lower() == "uni":
        text = "uniswap"
    elif text.lower() == "ltc":
        text = "litecoin"                          
    if text in [crypto.lower() for crypto in CRYPTOS]:
        for currency in CURRENCIES:
            price = get_crypto_price(text, currency)
            currency_symbolu = "$" if currency == "USD" else ""
            currency_symbolr = "₽" if currency == "RUB" else ""
            priceusd = f"{currency_symbolu}{price}"
            pricerub = f"{price}{currency_symbolr}"
            if currency == "USD":
              if price == 'Временно недоступно':
                message += f"Цена {text}:\n"
                message += f"USD:  временно недоступно\n"
              else:
                message += f"Цена {text}:\n"
                message += f"USD:  {priceusd}\n"
            else:
              if price == 'Временно недоступно':
                message += f"RUB:  временно недоступно\n"
              else:
                 message += f"RUB:  {pricerub}\n"
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=bot_messages_ids[-1])
        bot_messages_ids.pop()
        update.message.reply_text(message) 
        time.sleep(1) 
        choice_crypto(update, context) 


    else:
        message = f"Извините, криптовалюта '{text}' не найдена среди представленных мной вариантов.\nПожалуйста, используйте клавиатуру для выбора."
        update.message.reply_text(message)
        time.sleep(1) 
        choice_crypto(update, context) 

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("choice_crypto", choice_crypto))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
