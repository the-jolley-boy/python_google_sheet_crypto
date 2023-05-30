import gspread
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

# This part takes the service account that grants access (this is the file that you got from google api, I renamed it and put it in the same directory I run the code from)
sa = gspread.service_account(filename="service_account.json")
# The sheet to edit
sh = sa.open("TableName")
# The worksheet to edit
wks = sh.worksheet("WorksheetName")

# The symbols I want info on
symb = 'LRC,HNT,ETH,PLANETS,SOL,GST,GMT,IOT'

# This code was taken from Coin Market Caps docs with some slight alteration.
# The url is adjusted to get the quotes of specific suymbols you want to get data for, in my case the ones in the symb string.
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# Parameters so you get only what you want
parameters = {
  'symbol': symb,
  'convert': 'USD'
}
# In here you'll need to add your own key
headers = {
  'Accepts': 'application/json',
  'Accept-Encoding': 'deflate, gzip',
  'X-CMC_PRO_API_KEY': 'key_goes_here',
}

# I set the code to run indefinitely since I want the data to be updated and since I run a server I can just leave it running all the time.
# I have hard codded the data being pulled since for now I have no need to make it more versatile but if I need to in the future I will
while True:

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      lrc = data['data']['LRC']['quote']['USD']['price']
      hnt = data['data']['HNT']['quote']['USD']['price']
      eth = data['data']['ETH']['quote']['USD']['price']
      planets = data['data']['PLANETS']['quote']['USD']['price']
      sol = data['data']['SOL']['quote']['USD']['price']
      gst = data['data']['GST']['quote']['USD']['price']
      gmt = data['data']['GMT']['quote']['USD']['price']
      iot = data['data']['IOT']['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    # This part updates the desired cells.
    wks.update('H29', lrc)
    wks.update('H30', hnt)
    wks.update('H31', eth)
    wks.update('H32', planets)
    wks.update('H33', sol)
    wks.update('H34', gst)
    wks.update('H35', gmt)
    wks.update('H36', iot)

    time.sleep(1800)