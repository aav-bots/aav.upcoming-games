import time
import praw
import requests
import datetime
import parsedatetime
from bs4 import BeautifulSoup

_cal = parsedatetime.Calendar()
_base = r"http://ca.ign.com/upcoming/games/upcoming-ajax"
_ua = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

class UpcomingGame(object):
    def __init__(self, name, systems, release):
        self.name = name
        self.systems = systems
        self.release = release
    def add_system(self, newsys, newrls):
        if newsys not in systems:
            systems.append(newsys)
        if newrls not in release:
            release.append(newrls)

def log(msg):
    print(f'[{time.ctime()}] {msg}')

def get_all_games(time='7d', system=''):
    if time not in ('7d', '1m', '3m', '6m', '12m', 'all'):
        log("Invalid time period given, stopping.")
        retur
    log("Starting scraping for games.")
    params = { 'time': time, 'startIndex': 0 }
    headers = { 'User-Agent': _ua }
    games = dict()
    gdata = requests.get(_base, params=params, headers=headers)
    soup = BeautifulSoup(gdata.content, 'html.parser')
    divs = soup.find_all('div', class_='clear itemList-item')
    while len(divs) > 0:
        log(f"Parsing {len(divs)} game entries..")
        cursize = len(games)
        for div in divs:
            gchildren = list(div.children)
            gname = gchildren[3].div.h3.a.text.strip()
            gsyst = gchildren[3].div.h3.span.text.strip()
            gdtmp, gstat = _cal.parse(gchildren[-2].text.strip())
            gdate = datetime.date(*gdtmp[:3])
            if gdate > datetime.date.today():
                if gname not in games.keys():
                    games[gname] = UpcomingGame(gname, [gsyst], [gdate])
        log(f"Added {len(games) - cursize} new games.")
        params['startIndex'] += len(divs)
        gdata = requests.get(_base, params=params)
        soup = BeautifulSoup(gdata.content, 'html.parser')
        divs = soup.find_all('div', class_='clear itemList-item')
    log("Done scraping games.")
    return games

def get_markdown(tformat='short'):
    if tformat not in ('short', 'long'):
        log("Table must be in short or long format.")
        return
