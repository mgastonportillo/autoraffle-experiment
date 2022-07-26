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
driver_path = 'C:\\folder\\of\\the\\webdriver'
driver = webdriver.Firefox(driver_path, options=options)
wait = WebDriverWait(driver, 5)

# RAFFLE SETTINGS - MODIFY FOR EVERY NEW RAFFLE
gb = 'gb4s3'  # "Guild Boss Tamer" raffle name
apow = 'pow4s3'  # "Player of The Week" raffle name

# USEFUL ACTIONS FUNCTIONS


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
        self.actions.send_keys(Keys.TAB * times)
        self.actions.perform()

    def hit_enter(self, times):
        """Hits ENTER for you"""
        self.actions = ActionChains(driver)
        self.times = times
        self.actions.send_keys(Keys.ENTER * times)
        self.actions.perform()

    def input_args(self, txt_str):
        """Inputs something for you"""
        self.actions = ActionChains(driver)
        self.txt_str = txt_str
        self.actions.send_keys(txt_str)
        self.actions.perform()


# Creating instances
tab = WebDriverActions()
enter = WebDriverActions()
send = WebDriverActions()

# CONNECT TO DISCORD AND LOGIN
# Open Discord in channel
driver.get('https://discord.com/channels/CHANNEL_ID')
time.sleep(2)

# Submit the email or phone number
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'input.inputDefault-3FGxgL input-2g-os5 inputField-2RZxdl'.replace(' ', '.'))))\
    .send_keys("USER_EMAIL")
time.sleep(2)


# My 'hack' to access the password field
tab.hit_tab(1)
time.sleep(2)

# Submit password and click enter button
send.input_args('USER_PASSWORD')

time.sleep(2)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button.marginBottom8-emkd0_ button-1cRKG6 button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeLarge-3mScP9 fullWidth-fJIsjq grow-2sR_-F'.replace(' ', '.'))))\
    .click()
time.sleep(10)

# My 'hack' to get into the input field
tab.hit_tab(1)
time.sleep(1)

# CREATING THE RAFFLES
# Submit command to create raffle for 'Player of the Week'
send.input_args(f'!raffle create {apow}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(1)

# Submit command to create raffle for 'Guild Boss Tamer'
send.input_args(f'!raffle create {gb}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(1)

# Generate the commands to add entries


class EroicaRaffle:
    """Read specific .txt files and modify their values to turn them into accionable bot commands"""

    # Defining constructor
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
            # Simple f-string to output the bot command; max of entries is 2 and bot sums repeated entries up
            self.commands_pow.append(
                f'!raffle tickets add {apow} "{line}" 1')
        return self.commands_pow

    def create_gb(self):
        """Creates the 'Guild Boss Tamer' Award commands"""
        # Reversing the list to make it easier to output the commands
        self.list_names = self.list_names[::-1]
        # default values for entry so that first value is 3
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


# Creating instance of the class
raff_pow = EroicaRaffle()
# Calling the right methods for 'Player of the Week'
raff_pow.read_names('names_pow.txt')
iter_raff_pow = raff_pow.create_pow()

# Creating instance of the class
raff_gb = EroicaRaffle()
# Calling the right methods for 'Guild Boss Tamer'
raff_gb.read_names('names_gb.txt')
iter_raff_gb = raff_gb.create_gb()

# Concatenating both lists for a smoother command submission method
submit_comm = iter_raff_pow + iter_raff_gb

# SUMBITTING THE COMMANDS
# My 'hack' to get into the input field
tab.hit_tab(1)
time.sleep(2)

# Saving bot commands into a file and submitting them
temp = open('commands.txt', 'w')
for comm in submit_comm:
    temp.write(comm)
    send.input_args(comm)
    time.sleep(1)
    enter.hit_enter(1)
    time.sleep(2)
temp.close()
time.sleep(2)

# PERFORM RAFFLES
# Open raffle channel
driver.get('https://discord.com/channels/CHANNEL_ID')
time.sleep(10)

# My 'hack' to get into the input field
tab.hit_tab(1)
time.sleep(2)

# Submit commands
send.input_args(f'!raffle tickets list {gb}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(2)
send.input_args(f'!raffle roll {gb}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(2)
send.input_args(f'!raffle tickets list {gb}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(2)
send.input_args(f'!raffle roll {gb}')
time.sleep(1)
enter.hit_enter(1)
time.sleep(2)

driver.quit()

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
