import gspread
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
import json
import time

# This part takes the service account that grants access (this is the file that you got from google api, I renamed it and put it in the same directory I run the code from)
sa = gspread.service_account(filename="service_account.json")
# The sheet to edit
sh = sa.open("Current Shoe/Clothing List & Bots")

def crypto():
    # The worksheet to edit
    wks = sh.worksheet("Total Value")
    # The symbols I want info on
    slug = 'loopring,helium,ethereum,planetwatch,helium-iot'
    # This code was taken from Coin Market Caps docs with some slight alteration.
    # The url is adjusted to get the quotes of specific suymbols you want to get data for, in my case the ones in the symb string.
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    # Parameters so you get only what you want
    parameters = {
        'slug': slug,
        'convert': 'USD'
    }
    # In here you'll need to add your own key
    headers = {
        'Accepts': 'application/json',
        'Accept-Encoding': 'deflate, gzip',
        'X-CMC_PRO_API_KEY': 'c5623937-5e55-450c-8115-61a7e204a4e9',
    }

    session = Session()
    session.headers.update(headers)

    #Grabs Crypto prices
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        lrc = data['data']['1934']['quote']['USD']['price']
        hnt = data['data']['5665']['quote']['USD']['price']
        eth = data['data']['1027']['quote']['USD']['price']
        planets = data['data']['11861']['quote']['USD']['price']
        iot = data['data']['24686']['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # This part updates the desired cells.
    wks.update('H29', lrc)
    wks.update('H30', hnt)
    wks.update('H31', eth)
    wks.update('H32', planets)
    wks.update('H33', iot)

def skinport():
    # The worksheet to edit
    wks = sh.worksheet("CSGO")

    items = requests.get("https://api.skinport.com/v1/items", params={
        "app_id": "730",
        "currency": "CAD",
    }).json()

    myitems = ["★ Talon Knife | Tiger Tooth (Factory New)", "★ Hand Wraps | CAUTION! (Field-Tested)", 
                "Desert Eagle | Printstream (Minimal Wear)", "USP-S | Printstream (Field-Tested)", 
                "StatTrak™ Glock-18 | Steel Disruption (Factory New)", "MP9 | Rose Iron (Minimal Wear)",
                "Five-SeveN | Monkey Business (Field-Tested)", "M4A1-S | Control Panel (Field-Tested)",
                "Galil AR | Chatterbox (Well-Worn)", "Glock-18 | Water Elemental (Minimal Wear)",
                "Dual Berettas | Twin Turbo (Minimal Wear)", "USP-S | The Traitor (Field-Tested)",
                "Two Times McCoy | TACP Cavalry", "Glock-18 | Snack Attack (Field-Tested)",
                "Blueberries Buckshot | NSWC SEAL", "P90 | Asiimov (Minimal Wear)",
                "AWP | Asiimov (Well-Worn)", "Number K | The Professionals",
                "AK-47 | Asiimov (Minimal Wear)", "P250 | Asiimov (Field-Tested)",
                "Music Kit | bbno$, u mad!", "Paris 2023 Challengers Sticker Capsule",
                "Paris 2023 Contenders Sticker Capsule", "Paris 2023 Legends Sticker Capsule",
                "Paris 2023 Champions Autograph Capsule", "Tec-9 | Remote Control (Minimal Wear)",
                "Paris 2023 Mirage Souvenir Package", "Sticker | Showdown (Foil)",
                "Sticker | Baby Howl", "Paris 2023 Vertigo Souvenir Package",
                "Paris 2023 Ancient Souvenir Package", "★ Bayonet | Marble Fade (Factory New)",
                "AK-47 | Leet Museo (Field-Tested)","AWP | Sun in Leo (Factory New)",
                "Glock-18 | Reactor (Minimal Wear)","USP-S | Blueprint (Minimal Wear)"]

    n = wks.get("A2:A37")
    names = [item for sublist in n for item in sublist]
    v = wks.get("E2:E37")
    values = [item for sublist in v for item in sublist]

    for item in items:
        name = item.get('market_hash_name')
        name = name.replace("'","")
        if name in myitems:
            sugg = item.get('suggested_price')
            
            index = names.index(name)
            values[index] = '=' + str(sugg) + '*B' + str(index+2)

    res = []
    for el in values:
        res.append([el])

    wks.update('E2:E37', res, raw=False)

# I set the code to run indefinitely since I want the data to be updated and since I run a server I can just leave it running all the time.
# I have hard codded the data being pulled since for now I have no need to make it more versatile but if I need to in the future I will
def main():
    while True:

        crypto()
        skinport()

        time.sleep(1800)

if __name__ == '__main__':
    main()
