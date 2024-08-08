from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from keys import LINK





class EvoBot:
    def __init__(self):
        self.service = Service(EdgeChromiumDriverManager().install())
        self.browser = webdriver.Edge(service=self.service)
        self.wait = WebDriverWait(self.browser, 20)
        self.current_state = "off"
        self.qty_nl = 0
    
    def __screenshot(self):
        """Take a screenshot from current browser screen
        """
        self.browser.save_screenshot("page.png")
    
    def __access(self):
        self.browser.get(LINK)
    
    def __auth(self):
        try:
            if self.wait.until_not(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'))):
                self.current_state = "on"
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
    
    def __wait_auth(self):
        while self.current_state == "off":
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')))
            self.__screenshot()
            print("Scan to continue...")
            self.__auth()
    
    def start(self):
        try:
            self.__access()
            self.__wait_auth()
        except Exception as e:
            print(f"Erro ao iniciar o bot: {e}")

bot = EvoBot()
print(bot.current_state)
bot.start()
print(bot.current_state)

# Manter o navegador aberto para depuração
input(">>> ")



    
