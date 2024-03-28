import time, getpass, selenium
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sce
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
Exception if web driver cannot navigate to a default link on initial startup.
"""
class NoDriverFunctionality(Exception):
    def __init__(self, home_link, message=None):
        if message == None:
            self.message = f"Web driver initialized, but could not navigate to home: {home_link}"
        else:
            self.message = message

        super().__init__(self.message)

"""
A class that initializes a webdriver (browser) instance.

Attributes:
username (str) - The user's GeoGuessr username.
password (str) - The user's GeoGuessr password.
"""
class Browser():
    def __init__(self, username, password, home_link="https://www.google.com"):
        self.username = username
        self.password = password
        self.home_link = home_link
        # Open an instance of Chrome and navigate to google.com.  Throw an error if not initialized.
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.get(home_link)

            if self.driver.title:
                print(f"Web driver initialized and navigated to home: {home_link}.")
            else:
                raise NoDriverFunctionality(home_link) 
        except Exception as e:
            raise e

    """
    Attempts button clicks repeatedly until maximum attempts reached (i.e., throw exception).
    """
    def click_button(self, xpath, attempts=20):
        i = 0
        while i < attempts:
            try:
                button = self.driver.find_element(By.XPATH, xpath)
                button.click()
                break
            except:
                i += 1
                time.sleep(1)
        if i == attempts: # Last chance!
            button.click()
            
    """
    Attempts to fill out a form element until maximum attempts reached (i.e., throw exception).
    """
    def fill_form(self, xpath, text, attempts=20):
        i = 0
        while i < attempts:
            try:
                field = self.driver.find_element(By.XPATH, xpath)
                field.send_keys(text)
                break
            except:
                i += 1
                time.sleep(1)
        if i == attempts: # Last chance!
            field.send_keys(text)

    """
    Check if a web element exists.
    Returns: True or False
    """
    def check_element_exists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except sce.NoSuchElementException:
            return False
        except Exception as e:
            raise e
        else:
            return True
    """
    Delete an element by its class name.
    """
    def delete_element(self, class_name):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        self.driver.execute_script("arguments[0].style.display = 'none';", element)
    
    def click_map(self, xpath):
        time.sleep(5)

        element = self.driver.find_element(By.XPATH, xpath)
        ActionChains(self.driver).move_to_element(element).click().perform()
        
    """
    Start browsing GeoGuessr.
    """
    # settings functionality is not implemented yet
    def start_game(self, country, settings):
        home_link = "https://www.google.com"
        country = country.lower()
        geoguessr_link = f"https://www.geoguessr.com/maps/{country}/play"

        # Navigate to desired map.
        self.driver.get(geoguessr_link)

        # Accept cookies
        cookies_xpath = "/html/body/div[2]/div[2]/div/div/div[2]/div/div/button"
        self.click_button(xpath=cookies_xpath)

        # Click login button
        login_xpath = "/html/body/div[1]/div/div[2]/div[1]/div[2]/header/div[2]/div[2]/a"
        self.click_button(xpath=login_xpath)

        # Enter GG username
        username_field = "/html/body/div[1]/div/div[2]/div[1]/main/div/div/form/div/div[1]/div[2]/input"
        self.fill_form(username_field, self.username)
        
        # Enter GG password
        password_field = "/html/body/div[1]/div/div[2]/div[1]/main/div/div/form/div/div[2]/div[2]/input"
        self.fill_form(password_field, self.password)

        # Submit form
        userpass_xpath = "/html/body/div[1]/div/div[2]/div[1]/main/div/div/form/div/div[3]/div[1]/div/button"
        self.click_button(userpass_xpath)
        
        # Game settings
        # Make sure settings are default
        move_setting = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[1]/div[3]/input"
        pan_setting = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[2]/div[3]/input"
        zoom_setting = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[2]/label[3]/div[3]/input"
        time_setting = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[2]/div/div[1]/div/label/div[2]/div/div/div[2]"
        default_settings_button = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div[1]/div[2]/input"

        # For now, just set the settings to default
        if self.check_element_exists(move_setting):
            assert self.check_element_exists(pan_setting) and self.check_element_exists(zoom_setting)
            assert self.check_element_exists(time_setting)
            self.click_button(default_settings_button)
        
        # Start the game.
        start_game = "/html/body/div[1]/div[2]/div[2]/div[1]/main/div/div/div/div/div[3]/div/div/button"
        self.click_button(start_game)

        # Delete arrows
        self.delete_element("SLHIdE-sv-links-control")

        # Delete HUD
        self.delete_element("game_status__q_b7N")
        self.delete_element("game_controls___pIfC")
        self.delete_element("game_topHud__tAKJD")

        # Click map (enables guess button)
        map_xpath = "/html/body/div[1]/div[2]/div[2]/main/div/div/div[4]/div/div[3]/div/div/div/div[3]/div[1]/div[2]"
        self.click_map(map_xpath)
        
        while True:
            time.sleep(10000)
            print("i'm still here!")
        

"""
Grabs user's credentials to log into website.

Parameters:
os (str) - Enter as windows or mac, not case sensitive
admin_name (str) - The OS username (NOT GG USERNAME)
admin (bool) - Set to True if you have an admin.txt file in the default home directory. \
Otherwise, enter directly into the terminal.

Returns:
username, password (tuple, str)
"""
def get_credentials(os, admin_name="", admin=False):
    username = ""
    password = ""
    path = ""

    
    # I know it's bad...but please store user/pw in plain text, each on separate line
    if admin:
        if os.lower() == "mac":
            path = f"/Users/{admin_name}/admin.txt"
        elif os.lower() == "windows":
            path = f"C:\\Users\\{admin_name}\\admin.txt"
            # Implement with windows
        else:
            print("dirty linux abusers are not allowed")
            return
        with open(path) as f:
            lines = f.read().splitlines()
            username = lines[0]
            password = lines[1]
    else:
        username = input("Enter your GeoGuessr username: ")
        password = getpass.getpass("Enter your GeoGuessr password: ")

    return (username, password)
        

if __name__ == "__main__":
    # yo aidan please change the get_credentials parameters below or it will not work :)
    username, password = get_credentials(os="Mac", admin_name="ethan", admin=True)
    data_acq = Browser(username, password)
    game_settings = {
        "default": False,
        "time": np.inf,
        "move": True,
        "pan": True,
        "zoom": True
    }
    data_acq.start_game("andorra", game_settings)