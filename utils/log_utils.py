from datetime import datetime
from pyfiglet import Figlet


def log_bot_version(version="Alpha 1.0.0"):
    figlet = Figlet(font="slant")
    print(figlet.renderText("Pumps Bot"))
    print("Version : {}".format(version))

def log_entry_detect_pumps(stable_coin):
    print("-----------------------------------------------------")
    print("     Detecting Pumps - Quotes : {}    ".format(stable_coin))
    print("-----------------------------------------------------\n")


def log_coins_pump(coins, coin):
    print('-----------------------------------------------------')
    print(" Coin {} / {}  :  Checking : {} ...".format(coins.index(coin) + 1, len(coins), coin))



def log_pump_found(df, coin):
    num = len(df)
    print(" {} pumps founded in {} ".format(num, coin))


def log_add_data_pumps(df):
    print("-----------------------------------------------------")
    print("End of getting pumps. {} pumps founded".format(len(df)))
    print("-----------------------------------------------------")
    print('Adding backward/forward data to pumps dataframe...')
