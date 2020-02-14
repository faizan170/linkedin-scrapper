import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from win32api import GetSystemMetrics


class BsHelper():
    def __init__(self, path):
        self.browser = webdriver.Chrome(path)
        self.browser.set_window_size(GetSystemMetrics(0), GetSystemMetrics(1))


    def perfromClick(self, data):
        try:
            button = self.browser.find_element_by_xpath(data)
            button.click()
            return True
        except:
            return False

    def scrollAndLoadContent(self):
        SCROLL_PAUSE_TIME = 5
        # Get scroll height
        totalHeight = self.browser.execute_script("return document.body.scrollHeight")
        for i in range(1,int(totalHeight/600)):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo({}, {});".format((700*i) - 700, 700 * i))

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            
        time.sleep(5)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scrollAndClick(self):
        SCROLL_PAUSE_TIME = 4
        # Get scroll height
        totalHeight = self.browser.execute_script("return document.body.scrollHeight")
        
        clicks = [False, False, False]
        data = ["//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid']",
                "//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']",
                "//a[@class='lt-line-clamp__more']"]
        for i in range(1,int(totalHeight/600)):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo({}, {});".format((700*i) - 700, 700 * i))

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            for i in range(3):
                if clicks[i] == False:
                    clicks[i] = self.perfromClick(data[i])
        time.sleep(5)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        clicks[2] = self.perfromClick(data[2])
        #print(clicks)


    def loginLinkedin(self, email, password):
        self.browser.get('https://www.linkedin.com/uas/login')


        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(email)

        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(password)

        elementID.submit()


    def getProfileSearch(self, link):
        self.browser.get(link)
        
        SCROLL_PAUSE_TIME = 5
        for i in range(1,5):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, {});".format(400 * i))

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)


        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def getProfilePage(self, link):
        self.browser.get(link)
        self.scrollAndLoadContent()
        self.scrollAndClick()
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        return soup
