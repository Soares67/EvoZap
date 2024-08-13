from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PIL import Image
import os
from time import sleep
from keys import LINK
import random as rd





class EvoBot:
    def __init__(self):
        self.service = Service(EdgeChromiumDriverManager().install())
        self.browser = webdriver.Edge(service=self.service)
        self.browser.set_window_size(1051,797)
        self.wait = WebDriverWait(self.browser, 20)
        self.current_state = "off"
        self.unread_list = []
        self.qty_unreads = 0
        self.sleeper = lambda: sleep(rd.uniform(2.1, 5.2))
        self.commands = {"/start": "Hello! Welcome!", "/finish": "Finishing...."}

    def __screenshot(self):
        """Take a screenshot from current browser screen
        """
        self.browser.save_screenshot("page.png")
    
    def __get_qr(self, qr):
        page = Image.open("page.png")

        qr_position = qr.location
        qr_size = qr.size

        start_x = qr_position["x"] + 190
        start_y = qr_position["y"] + 120
        final_x = ((start_x + qr_size["width"]))
        final_y = (start_y + qr_size["height"])

        offset = 50

        qr_img = page.crop((start_x-offset, start_y-offset-offset, final_x+offset, final_y+offset))
        qr_img.save("qr.png")
    
    def __del_imgs(self):
        try:
            os.remove("qr.png")
            os.remove("page.png")
        except:
            pass
    
    def __access(self):
        self.browser.get(LINK)  
    
    def __auth(self):
        try:
            if self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]'))):
                self.current_state = "on"
                self.__del_imgs()
        except Exception:
            pass
    
    def __reloader(self):
        try:
            if self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/span/button'):
                return True
        except:
            return False

    def __wait_auth(self):
        while self.current_state == "off":
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')))
            if self.__reloader():
                self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/span/button').click()
            
            qr = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')))
            self.__screenshot()
            self.__get_qr(qr)
            print("Escaneie para continuar...")
            self.__auth()
    
    def start(self):
        try:
            self.__access()
            self.__wait_auth()
        except Exception:
            pass
    
    def refresh_unreads(self):
        self.sleeper()
        self.unread_list = self.browser.find_elements(By.CSS_SELECTOR, '.x10l6tqk.xh8yej3.x1g42fcv')
        self.qty_unreads = len(self.unread_list)

    def open_unreads(self):
        self.sleeper()
        while not "não lidas" in self.browser.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[1]').text:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[2]/button[2]'))).click()
    
    def __close_chat(self):
        self.sleeper()
        self.browser.find_element(By.XPATH, '//*[@id="main"]/header/div[3]/div/div[3]/div/div').click()
        self.sleeper()
        self.browser.find_element(By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/div/li[3]/div').click()

    def __is_spam(self, message_list: list):
        count = 0
        for message in message_list:
            if message.startswith("/"):
                count += 1
        if count > 1:
            return True
        else:
            return False
    
    def __link_message(self, elements_list: list, message_index: int):
        actions = webdriver.ActionChains(self.browser)  # ActionChains

        actions.move_to_element(elements_list[message_index]).perform()

        viewbox = self.browser.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[32]/div/div/div[1]/div[1]/span[2]/div/div/span/svg')
        for i in viewbox:
            print(i)

    def enter_chat(self):
        self.sleeper()
        self.unread_list[self.qty_unreads-1].click()

        lista_mensagens = self.browser.find_elements(By.CSS_SELECTOR, '[class*="message"]')  # Lista de mensagens da conversa
        lista_nr = []  # lista de conversas não respondidas
        last = None
        for i, mensagem in enumerate(lista_mensagens):
            if "message-out" in mensagem.get_attribute("class"):
                last = i  # índice da última mensagem enviada

        try:
            lista_nr.extend(lista_mensagens[last+1:])  # Lista das mensagens não respondidas (a partir da última mensagem enviada)
        except:
            lista_nr = lista_mensagens  # Se não houver mensagens enviadas, mas houver recebidas ela será a própria lista de mensagens
                

        print(len(lista_nr), "Mensagens não lidas")  # Mensagens não respondidas
        lista_mensagens = [i.find_element(By.CSS_SELECTOR, '._ao3e.selectable-text.copyable-text').text for i in lista_nr]  # texto das mensagens não respondidas
        lista_elementos = [i.find_element(By.CSS_SELECTOR, '._ao3e.selectable-text.copyable-text') for i in lista_nr]  # Elementos das mensagens não lidas

        if self.__is_spam(lista_mensagens):
            warn = "Please, don't spam commands."
            res = self.gen_response(lista_mensagens[0])
            self.send_response(warn)
            self.__link_message(lista_elementos, 0)
            self.send_response(res)
        else:
            msg = "\n".join(lista_mensagens)  # Todas as mensagens não respondidas agrupadas em uma string
            print(msg)

            res = self.gen_response(msg)
            self.send_response(res)

        self.__close_chat()
        self.sleeper()
        self.refresh_unreads()

    def __identify_msgtype(self, message):
        if message.startswith("/"):
            return "cmd"
        else:
            return "nrml"
    
    def gen_response(self, message):
        if self.__identify_msgtype(message) == "cmd":
            if message in self.commands.keys():
                return self.commands[message]
            else:
                return "Uknown command."
        else:
            return "Hello, World!"
    
    def send_response(self, response):
        actions = webdriver.ActionChains(self.browser)  # ActionChains

        res = response

        res_entry = self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')  # Entry
        res_entry.click()
        self.sleeper()
        actions.key_down(Keys.LEFT_CONTROL).send_keys("a").key_up(Keys.LEFT_CONTROL).perform()  # Seleciona todo o texto do entry
        actions.send_keys(Keys.BACKSPACE).perform()
        res_entry.send_keys(res)  # Texto que será enviado
        self.sleeper()
        self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()


    

bot = EvoBot()
print(bot.current_state)
bot.start()
print(bot.current_state)

print(bot.qty_unreads)
bot.open_unreads()
print(bot.qty_unreads)

while True:
    bot.refresh_unreads()
    if len(bot.unread_list) > 0:
        bot.enter_chat()
    input(">>>>")
    bot.sleeper()



    
