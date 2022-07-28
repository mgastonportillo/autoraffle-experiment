"""Setting up and rolling Eroica Awards raffles on Discord automatically"""

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# BROWSER SETTINGS
options = webdriver.FirefoxOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

# FIREFOX DRIVER SETUP
driver_path = 'path\\to\\python-autoraffle-eroica'
driver = webdriver.Firefox(driver_path, options=options)
wait = WebDriverWait(driver, 5)

# RAFFLE SETTINGS - MODIFY FOR EVERY NEW RAFFLE
apow = 'powNOT'  # "Player of The Week" raffle name
gb = 'gb4NOT'  # "Guild Boss Tamer" raffle name

# USEFUL FUNCTIONS


class WebDriverActions:
    """Perform Actions for the selected WebDriver"""

    def __init__(self):
        self.times = 0
        self.actions = ActionChains(driver)
        self.txt_str = ''

    def hit_tab(self, times):
        """Hits TAB for you"""
        self.actions = ActionChains(driver)
        self.times = times
        self.actions.send_keys(Keys.TAB * self.times)
        self.actions.perform()

    def hit_enter(self, times):
        """Hits ENTER for you"""
        self.actions = ActionChains(driver)
        self.times = times
        self.actions.send_keys(Keys.ENTER * self.times)
        self.actions.perform()

    def input_args(self, txt_str):
        """Inputs something for you"""
        self.actions = ActionChains(driver)
        self.txt_str = txt_str
        self.actions.send_keys(txt_str)
        self.actions.perform()


# Generates the commands to add entries


class EroicaRaffle:
    """Read specific .txt files and modify their values to turn them into accionable bot commands"""

    def __init__(self):
        self.the_file = []
        self.list_names = []
        self.commands_pow = []
        self.commands_gb = []

    def read_names(self, file):
        """Reads a text file and turns it into a list"""
        self.the_file = file
        with open(file, 'r') as f:
            self.list_names = f.read().splitlines()
        return self.list_names

    def create_pow(self):
        """Creates the 'Player of The Week' Award commands"""
        for line in self.list_names:
            self.commands_pow.append(
                f'!raffle tickets add {apow} "{line}" 1')
        return self.commands_pow

    def create_gb(self):
        """Creates the 'Guild Boss Tamer' Award commands"""
        # Reversing the list to make it easier to output the commands
        self.list_names = self.list_names[::-1]
        # default values for 'entry' so that first value is 3
        entry = 2
        # Grabbing indexes of list items to operate with them
        for index, line in enumerate(self.list_names):
            if index < 5:
                self.commands_gb.append(
                    f'!raffle tickets add {gb} "{line}" 1')
            elif index < 10:
                self.commands_gb.append(
                    f'!raffle tickets add {gb} "{line}" 2')
            else:
                entry += 1
                self.commands_gb.append(
                    f'!raffle tickets add {gb} "{line}" {entry}')
        return self.commands_gb


# Creates instances of EroicaRaffle()
raff_pow = EroicaRaffle()
raff_pow.read_names('names_pow.txt')
iter_raff_pow = raff_pow.create_pow()

raff_gb = EroicaRaffle()
raff_gb.read_names('names_gb.txt')
iter_raff_gb = raff_gb.create_gb()

wda = WebDriverActions()

# Concatenates both command lists
submit_comm = iter_raff_pow + iter_raff_gb

# CONNECTS TO DISCORD AND LOGIN
# Opens Discord in channel
driver.get('https://discord.com/channels/CHANNEL_ID')
time.sleep(1)

# Skips the 'Discord App Detected message'
wait.until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div/div[1]/div/div/div/section/div/button[2]')))\
    .click()
time.sleep(1)

# Submits the email or phone number
wait.until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')))\
    .send_keys("USER_EMAIL")
time.sleep(1)

# Submits password
wait.until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')))\
    .send_keys('USER_PASS')
time.sleep(1)

# Hits enter and logs in
wait.until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]')))\
    .click()
time.sleep(5)

# CREATES THE RAFFLES AND SUBMITS COMMANDS
# My 'hack' to get into the input field
wda.hit_tab(1)
time.sleep(1)

# Submits command to create raffle for 'Player of the Week'
wda.input_args(f'!raffle create {apow}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)

# Submits command to create raffle for 'Guild Boss Tamer'
wda.input_args(f'!raffle create {gb}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)

# My 'hack' to get into the input field
wda.hit_tab(1)
time.sleep(1)

# Resets 'commands.txt'
with open('commands.txt', 'w') as c:
    c.truncate(0)

# Saves bot commands into a file and submits them
for comm in submit_comm:
    temp = open('commands.txt', 'w')
    temp.write(comm + "\n")
    wda.input_args(comm)
    time.sleep(1)
    wda.hit_enter(1)
    time.sleep(1)

# PERFORMS RAFFLES
# Opens raffle channel
driver.get('https://discord.com/channels/CHANNEL_ID')
time.sleep(5)

# My 'hack' to get into the input field
wda.hit_tab(1)
time.sleep(1)

# Submits commands
wda.input_args(f'!raffle tickets list {apow}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)
wda.input_args(f'!raffle roll {apow}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)
wda.input_args(f'!raffle tickets list {gb}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)
wda.input_args(f'!raffle roll {gb}')
time.sleep(1)
wda.hit_enter(1)
time.sleep(1)
# Closes WebDriver session
driver.quit()
