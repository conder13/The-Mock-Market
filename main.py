print("Checking for packages...")
import subprocess
import os
import subprocess
import sys
import pip    
import time
from pip._internal.utils.misc import get_installed_distributions
files = []
for file in get_installed_distributions():
  files.append(file)

for i in files:
  if i == "":
    print("Please hold as we install some packages!") 

    time.sleep(1.3)
    os.system("pip install yahoo_fin")
    os.system("pip install -U textblob")
    os.system("python -m textblob.download_corpora")
os.system("clear")

from yahoo_fin.stock_info import *
from yahoo_fin import news
from replit import db
from datetime import date
from pprint import pprint
import sys
import re

repl_user = os.environ['REPL_OWNER']
signed_in = False
username = ""

account_shares = username + "shares"
account_prices = username + "prices"
account_port = username + "portfolio"
account_history = username + "history"
account_balance = username + "balance"
account_status = username + "status"

times_home = 0
balance = 5000

owned_stocks = []
pnum_shares = {}
pprice_got = {}
portfolio = [pnum_shares,pprice_got,owned_stocks]
history = []
account_status = username + "status"

if username != "":
  db[account_status] == "Online"

def create_account():
  acc_name = input("What would you like your username to be?\n> ")
  if acc_name not in db:
    acc_pswrd = input("Great! What would you like your password to be?\n> ")
    db[acc_name] = acc_pswrd
    username == acc_name
    db[account_balance] = 5000
    db[account_port] = []
    db[account_history] = []
    db[account_shares] = {}
    db[account_prices] = {}

  home()

def sign_in():
  global username
  global balance
  username = input("What is your username?\n> ")
  if username in db:
    si_pswrd = input("Account found! What is your password?\n> ")
    if si_pswrd == db[username]:
      remember = input("Before we log you in, do you want to turn on 'Remember Me' so you won't have to sign in every time? Type 'yes' or 'no'")
      if remember == "yes" or "Yes":
        print("Okay, enabling 'Remember Me'...")
        db["(repl)"+username] = repl_user
      print("Great! Signed in!")
      account = username + "data"
    if si_pswrd != db[username]:
      print("Username and password do not match.")
      si_pswrd = input("What is your password?\n> ")
    time.sleep(1.5)
    
  os.system("clear")
  home()


online = {}
offline ={}
controller = {}
def update_custom():
  for account in account_status:
    if account == "Online":
      online.append(account)
    if account == "Offline":
      offline.append(account)
    if account in controller and account in offline:
      controller.pop(account)

def dev_stuff():
  print("welcome dev")
  accountsl = {}
  historiesl = {}
  pricesl = {}
  portfoliosl = {}
  sharesl = {}
  usersl = {}
  item = ""
  for item in db:
    histories = re.search("^HISTORY", item)
    prices = re.search("^PRICE", item)
    portfolios = re.search("^PORTFOLIO", item)
    shares = re.search("^SHARE", item)
    users = re.search("USER", item)
    if histories:
      item == re.sub("HISTORY","",str(item))
      historiesl[item] = db[item]
    if prices:
      pricesl[item] = db[item]
    if portfolios:
      portfoliosl[item] = db[item]
    if shares:
      sharesl[item] = db[item]
    if users:
      new_item = re.sub("USERNAME","",item)
      usersl[new_item] = db[item]
  option = input(">")
  if option == "users":
    print()
    for item in usersl:
      print(item+":",db[item])


def add_to_history(share_count,user_stock):
  today = date.today()
  datetoday = today.strftime("%d/%m/%y")
  hist_stock = user_stock
  history.append(datetoday+": You bought")
  history.append(str(share_count)+" shares of")
  history.append(hist_stock)
#difference = price - get_premarket_price(user_stock)
#news = news.get_yf_rss(user_stock)

def portfolio():
  print(username+"'s Portfolio")
  for item in db[account_port]:
    print(item,"\n")

def buy():
  global balance
  
  price = get_live_price(user_stock)
  share_count = int(input("How many shares?\n> "))
  cost = price * share_count
  if cost < balance:
    confirm = input("Are you sure you want to buy "+user_stock+"? It will cost $"+str(round(cost,2))+".\n> ")
    if confirm == "yes" or "Yes":
      balance = balance - cost
      print("Great! You bought",share_count,"shares of",user_stock,"!")
      add_to_history(share_count,user_stock)
      owned_stocks.append(user_stock)
      if user_stock in pprice_got and user_stock in pnum_shares:
        find_avg_price = (pprice_got[user_stock]+price) / 2
        find_numshares = pnum_shares[user_stock]+share_count
        pprice_got.update({user_stock:find_avg_price})
        pnum_shares.update({user_stock:find_numshares})
      else:
        pprice_got.update({user_stock:price})
        pnum_shares.update({user_stock:share_count})
    else:
      print("Okay! Returning to Home...")
  else:
    print("You don't have enough in your account!")

  time.sleep(2)
  os.system("clear")
  home()

#def sell():

def find_money_change():  
  global money_change
  money_change = 0
  for stock in owned_stocks:
    ind_money_change = (get_live_price(stock) - pprice_got[stock]) * pnum_shares[stock]
    money_change = money_change + ind_money_change
  return(money_change)

def save():
  db["SHARE"+account_shares] = pnum_shares
  db["PRICE"+account_prices] = pprice_got
  db["PORTFOLIO"+account_port] = owned_stocks
  db["HISTORY"+account_history] = history
  db["USERNAME"+username] = db[username]
  db["BALANCE"+account_balance] = balance
  db[account_shares] = pnum_shares
  db[account_prices] = pprice_got
  db[account_port] = owned_stocks
  db[account_history] = history
  db[username] = db[username]
  db[account_balance] = round(balance,2)
  print("saved")

def home():
  global account_shares
  global account_prices
  global account_port
  global account_history
  global account_balance
  global price
  global user_stock
  global money_change
  global times_home
  global balance
  global pnum_shares
  global pprice_got
  global history
  global owned_stocks
  global portfolio
  global account_status

  if username != "" and times_home < 1:
    
    balance = db[account_balance]
    portfolio = db[account_port]
    pnum_shares = db[account_shares]
    pprice_got = db[account_prices]
    history = db[account_history]
    times_home += 1
  elif username == "":
    balance = 5000
  print("___"+username+"___\nBalance: $"+str(round(balance,2)))
  #print(db[account])
  if times_home >= 1:
    save()
  user_action = input()
  if user_action == "buy":
    user_stock = input("What stock?\n> ")
    buy()
  if user_action == "sign up":
    create_account()
    home()
  if user_action == "sign in":
    sign_in()
    home()
  if user_action == "show":
    print(db[account])
  if user_action == "history":
    word_count = 0
    word = []
    for item in db[account_history]:
      if word_count < 3:
        word.append(item)
        word_count += 1
      if word_count >= 3:
        print(' '.join(word))
        word.clear()
        word_count -= 3
    home()

  if user_action == "money":
    find_money_change()
    print(money_change)
  if user_action == "portfolio":
    portfolio()    
  if user_action == "view":
    user_stock = input("What stock?\n> ")
    
    price = get_live_price(user_stock)
    while True:
      print(user_stock,":",round(price,2), end = "\r")
      print("\n")
      ws_action = input("")
      if ws_action == "buy":
        buy()
        break
        
        home()
  if user_action == "status":
    print(online,"\n",offline)
      #print(difference)



'''

def buy():
  user_buy = input("Would you like to buy this?")
  if user_buy == "yes":
    bought_price = price
  print(bought_price)'''

def main():
  print("Welcome to The Mock Market! Please sign in or create an account to continue...\n\n")
  sioca = input("> ")
  if sioca == "create account":
    create_account()
  if sioca == "sign in":
    sign_in()


main()
'''while True:'''


