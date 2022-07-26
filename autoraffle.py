"""My very first attemp at automating stuff"""

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

# FIREFOX DRIVER PATH SETUP
driver_path = 'C:\\Users\\gale\\vscode_repo\\python-autoraffle'
driver = webdriver.Firefox(driver_path, firefox_options=options)

# VALUES TO MODIFY MANUALLY APART FROM THE .TXT FILES
# (no idea why Pylint thinks these are constants, or maybe I'm just too lost here...)

# "Guild Boss Tamer" raffle name
gb = 'gb4s3'
# "Player of The Week" raffle name
apow = 'pow4s3'


class EroicaRaffle():
    """Practicing class implementation to avoid global statements"""

    def __init__(self):
        self.the_file = []
        self.read_pow = []
        self.read_gb = []
        self.commands_apow = []
        self.commands_gb = []

    def read_file_apow(self, file):
        """Reads an apow text file and turns it into a list"""
        self.the_file = file
        with open(file, 'r') as f:
            # splitlines() takes care of the line jumps
            self.read_apow = f.read().splitlines()
        return self.read_apow

    def read_file_gb(self, file):
        """Reads a gb text file and turns it into a list"""
        self.the_file = file
        with open(file, 'r') as f:
            # splitlines() takes care of the line jumps
            self.read_gb = f.read().splitlines()
        return self.read_gb

    def create_apow(self):
        """Creates the 'Player of The Week' Award commands"""
        for line in self.read_apow:
            self.commands_apow.append(
                f'!raffle tickets add {apow} "{line}" 1')
        return self.commands_apow

    def create_gb(self):
        """Creates the 'Guild Boss Tamer' Award commands"""
        self.read_gb = self.read_gb[::-1]
        entry = 2
        for index, line in enumerate(self.read_gb):
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


cmds_apow = EroicaRaffle()
cmds_apow.read_file_apow('names_pow.txt')
iter_apow = cmds_apow.create_apow()

cmds_gb = EroicaRaffle()
cmds_gb.read_file_gb('names_gb.txt')
iter_gb = cmds_gb.create_gb()

submit_comm = iter_apow + iter_gb

# Open Discord
driver.get("https://discord.com/channels/CHANNEL")
wait = WebDriverWait(driver, 10)
# Click on the email or phone number input field
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "input.inputDefault-3FGxgL input-2g-os5 inputField-2RZxdl".replace(" ", "."))))\
    .send_keys("DISCORD_EMAIL")
time.sleep(3)
# Trying to click on password field
n = 1
actions = ActionChains(driver)
actions.send_keys(Keys.TAB * n)
actions.send_keys("PASSWORD")
actions.perform()
time.sleep(3)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "button.marginBottom8-emkd0_ button-1cRKG6 button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeLarge-3mScP9 fullWidth-fJIsjq grow-2sR_-F".replace(" ", "."))))\
    .click()

time.sleep(20)
n = 1
actions = ActionChains(driver)
actions.send_keys(Keys.TAB * n)
actions.perform()

time.sleep(5)

for comm in submit_comm:
    n = 1
    actions = ActionChains(driver)
    actions.send_keys(comm)
    actions.perform()
    n = 1
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER * n)
    actions.perform()
    time.sleep(5)

# ------------------------------------------------------------
# --- DIRTY CODE, DON'T LOOK! (Back-up of the first draft) ---
# ------------------------------------------------------------
# # Values to modify manually
# gb = 'gb4s3'  # "Guild Boss Tamer" raffle name
# pow = 'pow4s3'  # "Player of The Week" raffle name

# # Initialise empty lists
# names = []
# commands_pow = []
# commands_gb = []

# def read_file(file):
#     """Reads a text file and turns it into a list"""
#     with open(file, 'r') as f:
#         # splitlines() takes care of the line jumps
#         global names
#         names = f.read().splitlines()
#     return names

# read_pow = read_file('names_pow.txt')
# read_gb = read_file('names_gb.txt')

# def pow_create():
#     """Creates the 'Player of The Week' Award commands"""
#     for line in read_pow:
#         commands_pow.append(f'!raffle tickets list add {pow} "{line}" 1')
#     return commands_pow

# def gb_create():
#     """Creates the 'Guild Boss Tamer' Award commands"""
#     global read_gb
#     read_gb = read_gb[::-1]
#     entry = 2
#     for line in read_gb:
#         if i in range(len(read_gb)) < 5:
#             commands_gb.append(f'!raffle tickets list add {gb} "{line}" 1')
#         elif i in range(len(read_gb)) < 10:
#             commands_gb.append(f'!raffle tickets list add {gb} "{line}" 2')
#         else:
#             entry += 1
#             commands_gb.append(
#                 f'!raffle tickets list add {gb} "{line}" {entry}')
#     return commands_gb
# ------------------------------------------------------------
