from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time

class InstaFollower():

    def __init__(self, account):
        """Initializes instagram follower bot with account as argument."""

        # retrieve msedge driver executable
        msedge_driver_path = "C:\Development\msedgedriver.exe"
        self.driver = webdriver.Edge(executable_path=msedge_driver_path)

        # set members
        self.account = account

        # accounts not to unfollow
        self.accounts_list = [
            # ACCOUNTS NOT TO UNFOLLOW IN STRING #
        ]

    
    def login(self, password):
        """Logs into account with specified password."""

        # login process
        self.driver.get("https://www.instagram.com/")

        time.sleep(5)

        self.driver.find_element_by_name('username').send_keys(self.account)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()


    def find_followers(self, account):
        """Searches account specified as argument."""

        # searching process
        time.sleep(5)
        self.driver.get(f'https://www.instagram.com/{account}')

        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        
        time.sleep(2)
        self.to_scroll = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')

        
    def follow(self):
        """Follows all followers seen in object found in find_followers."""

        for i in range(5):
            time.sleep(4)

            buttons = [button for button in self.driver.find_elements_by_css_selector('.isgrP li button') if button.text.lower() != "following" and button.text.lower() != "requested"]

            for button in buttons:
                time.sleep(1)
                button.click()

            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.to_scroll)

        
    def unfollow(self):

        time.sleep(5)
        # self.driver.maximize_window()

        self.driver.get(f"https://www.instagram.com/{self.account}")
        time.sleep(5)

        # no_following = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text)

        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(5)

        buttons_pressed = 0     # this is to record the unfollowed accounts
        buttons_passed = 0      # this is to record the number of accounts passed for fluid unfollowing

        # since Instagram blocks accounts that mass unfollow, let's unfollow 48 accounts each day.
        while buttons_pressed < 50:
            
            try:
                self.to_scroll = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]')
            except NoSuchElementException:
                self.to_scroll = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]')

            buttons = [button for button in self.driver.find_elements_by_css_selector('li button')]
            accounts = [link.text for link in self.driver.find_elements_by_css_selector('li a') if link.text != "" and "followers" not in link.text and "following" not in link.text]
            
            print(len(buttons))

            for i in range(buttons_passed, len(buttons)):

                # break out of function when unfollowed accounts reach 48
                if buttons_pressed >= 48:
                    return

                if accounts[i] in self.accounts_list:
                    buttons_passed += 1
                    continue


                # unfollowing process

                time.sleep(1)

                try:
                    buttons[i].click()
                except NoSuchElementException:
                    time.sleep(1)
                    buttons[i].click()
                except ElementClickInterceptedException:
                    self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/button[2]').click()

                time.sleep(1)

                try:
                    self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()
                except NoSuchElementException:
                    try:
                        self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[1]').click()
                    except NoSuchElementException:
                        break
                    else:
                        buttons_pressed += 1
                else:
                    buttons_pressed += 1
                
                buttons_passed += 1

            
            if self.to_scroll:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.to_scroll)