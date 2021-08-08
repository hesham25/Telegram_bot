import json, os, time
import telegram
from telegram.ext import Updater, CommandHandler
from scraper_api import ScraperAPIClient



class BOT():

    def __init__(self, API_KEY):
        self.ADMIN_LIST = [<chat id>]   # Admin chat ID
        self.API_KEY = API_KEY
        self.settings = json.load(open((os.getcwd() + './data/settings.json'), 'r'))
        self.TOKEN = '<telegram token>'
        self.bot = telegram.Bot(self.TOKEN_1)
        self.discount_rate = self.settings['discount']
        self.raise_rate    = self.settings['raise']
        self.log_condition = self.settings['log']
        self.new_product   = self.settings['new']


    def send_message_to_bot(self, chat_id, text):
        while True:
            try : self.bot.send_message(chat_id=chat_id, text=text) ; break
            except Exception as e : print(e); time.sleep(1)
    

    def help_(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            self.send_message_to_bot(chat_id, "Aşka Yürek Gerek Anlasana")
            print("Aşka Yürek Gerek Anlasana")

    def update_discount(self, update, context):
        discount_rate = self.discount_rate
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            try : command, new_discount_rate = (update.message.text).split(" ")
            except ValueError:
                self.send_message_to_bot(chat_id, text="Girdi Yanlış Formatta Girildi!")
                return 0
            if new_discount_rate.isnumeric:
                try :   new_discount_rate = int(new_discount_rate)
                except ValueError:
                    self.send_message_to_bot( self.bot_1_cht_id , text="İndirim Oranı Yanlış Formatta Girildi.")
                    print("İndirim Oranı Yanlış Formatta Girildi.")
                    return 0

                if new_discount_rate == 0:
                    self.send_message_to_bot(chat_id, text="İndirim Oranı 0 olamaz.")
                    print("İndirim Oranı 0 olamaz.")
                    return 0
            else:
                self.send_message_to_bot(chat_id, text="İndirim Oranı Yanlış Formatta Girildi.")
                print("İndirim Oranı Yanlış Formatta Girildi.")
                return 0
            text=f"{discount_rate} Olan İndirim Oranı {new_discount_rate} Oranına Güncellenmiştir."
            self.send_message_to_bot(chat_id , text)
            print(text)
            self.settings['discount'] = new_discount_rate
            json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))

    def update_raise(self, update, context):
        raise_rate = self.raise_rate
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            try : command, new_raise_rate = (update.message.text).split(" ")
            except ValueError:
                self.send_message_to_bot(chat_id, text="Girdi Yanlış Formatta Girildi!")
                return 0
            if new_raise_rate.isnumeric:
                try:  new_raise_rate = int(new_raise_rate)
                except ValueError:
                    self.send_message_to_bot(chat_id, text="zam Oranı Yanlış Formatta Girildi.")
                    return 0
                if new_raise_rate == 0:
                    self.send_message_to_bot(chat_id, text="zam Oranı 0 olamaz.")
                    return 0
            else:
                self.send_message_to_bot(chat_id, text="zam Oranı Yanlış Formatta Girildi.")
                return 0
            text=f"{raise_rate} Olan zam Oranı {new_raise_rate} Oranına Güncellenmiştir."
            self.send_message_to_bot(chat_id, text)
            print(text)
            self.raise_rate = new_raise_rate
            self.settings['raise'] = new_raise_rate
            json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))

    def log_updater(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            try : command, new_log_type = (update.message.text).split(" ")
            except (ValueError, AttributeError):
                self.send_message_to_bot(chat_id, text="Girdi Yanlış Formatta Girildi!")
                return 0
            if new_log_type.lower() == "on":
                self.send_message_to_bot(chat_id, text="Log değiştirildi. ON")
                self.settings['log'] = True
                print("Log değiştirildi. ON")
                json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))

            elif new_log_type.lower() == "off":
                self.send_message_to_bot(chat_id, text="Log değiştirildi. OFF")
                print("Log değiştirildi. OFF")
                self.settings['log'] = False
                json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))

            elif new_log_type.lower() != "on" or new_log_type.lower() != "off":
                self.send_message_to_bot(chat_id, text = "Girdi Yanlış Formatta Girildi!")

    def new_producs_alert(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            try : command, alert = (update.message.text).split(" ")
            except ValueError:
                self.send_message_to_bot(chat_id, "Girdi Yanlış Formatta Girildi!")
                return 0

            if alert.lower() == "on":
                self.send_message_to_bot(chat_id, "Yeni Ürünler uyarısı. ON")
                print("Yeni Ürünler uyarısı. ON")
                self.settings['new'] = True
                json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))
                
            elif alert.lower() == "off":
                self.send_message_to_bot(chat_id, "Yeni Ürünler uyarısı. OFF")
                print("Yeni Ürünler uyarısı. OFF")
                self.settings['new'] = False
                json.dump(self.settings, open((os.getcwd()+'./data/settings.json'), 'w'))

    def API_info(self, update, context):
        chat_id = update.effective_chat.id
        if chat_id in self.ADMIN_LIST:
            api = update.message.text.lower()
            if api == "/api":
                requestLimit = int(ScraperAPIClient(self.API_KEY).account()['requestLimit'])
                requestCount = int(ScraperAPIClient(self.API_KEY).account()['requestCount'])
                msg = f'API INFO {ScraperAPIClient(self.API_KEY).account()}\nRemaining API requests {requestLimit - requestCount}'
                self.send_message_to_bot(chat_id, msg)
                print(msg)
            else :
                self.send_message_to_bot(chat_id, "Girdi Yanlış Formatta Girildi!")
                return 0

    # Manage commands from Bot_1
    def bot_managment(self):
        while True:
            print(f"BOT Hepsiburada1_bot Started")
            try:
                updater = Updater(self.TOKEN, use_context=True)
                dp = updater.dispatcher    
                dp.add_handler(CommandHandler('help', self.help_))
                dp.add_handler(CommandHandler('discount', self.update_discount))
                dp.add_handler(CommandHandler('raise', self.update_raise))
                dp.add_handler(CommandHandler('new', self.new_producs_alert))
                dp.add_handler(CommandHandler('log', self.log_updater))
                dp.add_handler(CommandHandler('api', self.API_info))
                updater.start_polling()
                updater.idle()
            except Exception as e:
                print(f"exception {e}")

API_KEY = ''
if __name__ == '__main__':
    bot = BOT(API_KEY)
    bot.bot_managment()
