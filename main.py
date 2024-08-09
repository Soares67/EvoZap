from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PIL import Image
import os
from keys import LINK





class EvoBot:
    def __init__(self):
        self.service = Service(EdgeChromiumDriverManager().install())
        self.browser = webdriver.Edge(service=self.service)
        self.wait = WebDriverWait(self.browser, 20)
        self.current_state = "off"
        self.unread_list = []
        self.qty_unreads = 0
    
    def __screenshot(self):
        """Take a screenshot from current browser screen
        """
        self.browser.save_screenshot("page.png")
    
    def __get_qr(self, qr):
        page = Image.open("page.png")

        qr_position = qr.location
        qr_size = qr.size

        start_x = qr_position["x"]
        start_y = qr_position["y"]
        final_x = (start_x + qr_size["width"])
        final_y = (start_y + qr_size["height"])

        qr_img = page.crop((start_x-50, start_y-50, final_x+50, final_y+50))
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
    
    def open_unreads(self):
        while not "não lidas" in self.browser.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[1]').text:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[2]/button[2]'))).click()
        self.unread_list = self.browser.find_elements(By.CSS_SELECTOR, '.x10l6tqk.xh8yej3.x1g42fcv')
        self.qty_unreads = len(self.unread_list)
    
    def __last_one(self):
        self.unread_list[self.qty_unreads-1].click()

    

bot = EvoBot()
print(bot.current_state)
bot.start()
print(bot.current_state)
print(bot.qty_unreads)
bot.open_unreads()
print(bot.qty_unreads)

# Manter o navegador aberto para depuração
input(">>> ")



    
