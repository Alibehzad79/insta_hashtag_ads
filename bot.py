from calendar import c
from cmath import log
from errno import EMSGSIZE
from lib2to3.pgen2 import driver
from pkgutil import ImpImporter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os
import random
import ast
from instaloader import Instaloader, Profile

os.system('clear')
print('Only Linux users, chrome browser')
print('---------------------------------')

# Begin driver confing
path = os.getcwd() + '/'
driver_path = path + 'chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# End driver config

# Begin Global urls

instagram_url = 'https://instagram.com/'
login_url = instagram_url + 'accounts/login/'
logout_url = instagram_url + 'accounts/logout/'
hashtag_url = instagram_url + 'explore/tags/'


# End Global urls

# Begin XPATH
username_xpath = '//input[@name="username"]'
password_xpath = '//input[@name="password"]'


notification_xpath = '//*[contains(text(), "Not Now")]'
search_user_xpath = '//input[name="queryBox"]'
textarea_xpath = '//textarea[@placeholder="Message..."]'

# End XPATH


class Bot:
    # login function
    def login_instagram(self, username, password):
        # login
        driver.get(login_url)
        time.sleep(3)
        try:
            username_box = driver.find_element(By.XPATH, username_xpath)
            username_box.send_keys(username)
            time.sleep(2)
        except Exception as error:
            print(error)
        try:
            password_box = driver.find_element(By.XPATH, password_xpath)
            password_box.send_keys(password)
            time.sleep(2)
        except Exception as error:
            print(error)
        try:
            password_box.send_keys(Keys.ENTER)
            time.sleep(5)
        except Exception as error:
            print(error)

        if 'Save Your Login Info?' in driver.page_source:
            print(username + ': Login in Successful!')
            driver.get(instagram_url + username + '/')
            return True
        else:
            print(username + ': Login Field!')
            return False

    # logout function
    def logout_instagram(self):
        driver.get(logout_url)
        time.sleep(3)

    # extract user from hashtag

    def extract_user_from_hashtag(self, L):
        user_list = []
        with open('tags.txt') as tags:
            tags = tags.read().split('\n')
            tag = tags[1]
            driver.get(hashtag_url + tag + '/')
            time.sleep(15)
            try:
                first_post = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[2]/div/div[1]/div[2]')
                first_post.click()
                time.sleep(10)
            except Exception as error:
                print(error)
                print('error in first_post from extract_user_from_hashtag')
            while(True):
                try:
                    target_username = driver.find_element(
                        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a')
                except Exception as error:
                    print(error)
                    print('error in target_username from extract_user_from_hashtag')

                try:
                    target_user_info = Profile.from_username(
                        L.context, target_username.text)
                except Exception as error:
                    print(error)
                with open('targets_done.txt') as targets_done:
                    targets_done = targets_done.read().split('\n')
                    if target_user_info.username in targets_done:
                        print(target_user_info.username +
                              ': arleady exists in targets_done.txt')
                    else:
                        target_user_followers_count = int(
                            target_user_info.get_followers().count)
                        if 100 < target_user_followers_count < 10000:
                            user_list.append(target_user_info.username)
                            print(target_user_info.username + '(' +
                                  str(target_user_info.get_followers().count) + ')' + ": added")
                            with open('target_users.txt', 'a') as target_users:
                                target_users.write(
                                    target_user_info.username + '\n')
                        else:
                            print(target_user_info.username + '(' +
                                  (str(target_user_info.get_followers().count)) + ')' + ': add field')

                        if len(user_list) == 4:
                            break
                        try:
                            next_btn = driver.find_element(
                                By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button')
                            next_btn.click()
                            time.sleep(10)
                        except Exception as error:
                            print(error)
                            print(
                                'error in next_btn from extract_user_from_hashtag function')
        if len(user_list) > 0:
            return user_list
        else:
            return 'user list is empty!'

    # send message to direct function
    def send_message(self, user_list):
        with open('message.txt') as message:
            driver.get(instagram_url + 'direct/inbox/')
        try:
            notification = driver.find_element(By.XPATH, notification_xpath)
            notification.click()
        except:
            print('notification not fond!')
        for user in user_list:
            driver.get(instagram_url + 'direct/new/')
            try:
                search_box = driver.find_element(By.XPATH, search_user_xpath)
                search_box.send_keys(user)
                time.sleep(10)
            except Exception as error:
                print(error)
                print('error in search_box from send_message function')
            try:
                select_username = driver.find_element(
                    By.XPATH, f'//div[contains(text(), "{user}")]')
                time.sleep(5)
                select_username.click()
                time.sleep(5)
            except Exception as error:
                print(error)
                print('select_username is not found')
            try:
                next_button = driver.find_element(
                    By.XPATH, f'//div[contains(text(), "Next")]')
                time.sleep(5)
                next_button.click()
                time.sleep(10)
            except Exception as error:
                print(error)
                print('next_button is not found')
            try:
                textarea = driver.find_element(
                    By.XPATH, textarea_xpath)
                time.sleep(5)
                textarea.click()
                textarea.send_keys(message + Keys.ENTER)
                time.sleep(20)
                with open('targets_done.txt', 'a') as targets_done:
                    targets_done.write(user + '\n')
                driver.get(instagram_url + 'direct/inbox/')
                x = random.randint(120, 140)
                print(f'sleep for {str(x)} seccond')
                time.sleep(x)
            except Exception as e:
                print('textarea is not found')

    def start(self, L):
        with open('accounts.txt') as accounts:
            accounts = accounts.read().split('\n')
            if accounts[-1] == '':
                del accounts[-1]
            for account in accounts:
                new_account = ast.literal_eval(account)
                username = new_account.get('username')
                password = new_account.get('password')
                login = self.login_instagram(username=username, password=password)
                if login:
                    user_list = self.extract_user_from_hashtag(L=L)
                    self.send_message(user_list=user_list)
                    self.logout_instagram()
                else:
                    self.logout_instagram()    
                    


user = 'username'
password = 'password'
status = False
try:
    L = Instaloader()
    L.login(user, password)
    print('instaloader Login successful')
    status = True
except:
    print('instaloader Login field!')
    status = False

bot = Bot()
if status:
    bot.start(L)
    L.close()
else:
    print('instaloader Login field!')
    L.close()
