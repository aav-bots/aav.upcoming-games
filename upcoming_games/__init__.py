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
        if newsys not in self.systems:
            self.systems.append(newsys)
        if newrls not in self.release:
            self.release[newrls] = [newsys]
        else:
            if newsys not in self.release[newrls]:
                self.release[newrls].append(newsys)

def log(msg, silent):
    if silent:
        return
    print(f'[{time.ctime()}] {msg}')

def get_all_games(time='7d', systems=[], silent=False):
    """Get a list of tuples of game names and UpcomingGame objects for the specified range."""
    if time not in ('7d', '1m', '3m', '6m', '12m', 'all'):
        log("Invalid time period given, stopping.", silent)
        return
    log("Starting scraping for games.", silent)
    params = { 'time': time, 'startIndex': 0 }
    headers = { 'User-Agent': _ua }
    games = dict()
    gsess = requests.Session()
    gdata = gsess.get(_base, params=params, headers=headers)
    soup = BeautifulSoup(gdata.content, 'html.parser')
    divs = soup.find_all('div', class_='clear itemList-item')
    while len(divs) > 0:
        log(f"Parsing {len(divs)} game entries..", silent)
        cursize = len(games)
        for div in divs:
            gchildren = list(div.children)
            gname = gchildren[3].div.h3.a.text.strip()
            gsyst = gchildren[3].div.h3.span.text.strip()
            gdtmp, gstat = _cal.parse(gchildren[-2].text.strip())
            gdate = datetime.date(*gdtmp[:3])
            if systems is not None and gsyst not in systems:
                continue
            if gdate > datetime.date.today():
                if gname not in games.keys():
                    games[gname] = UpcomingGame(gname, [gsyst], {gdate: [gsyst]})
                else:
                    games[gname].add_system(gsyst, gdate)
        log(f"Added {len(games) - cursize} new games.", silent)
        params['startIndex'] += len(divs)
        gdata = gsess.get(_base, params=params, headers=headers)
        soup = BeautifulSoup(gdata.content, 'html.parser')
        divs = soup.find_all('div', class_='clear itemList-item')
    log("Done scraping games, sorting by closest release.", silent)
    gsorted = sorted(games.items(), key=lambda v: (min(v[1].release.keys()), v[0]))
    return gsorted

def get_markdown(games, limit=10, tformat='short', silent=False):
    """Format a list of game tuples in a Markdown table."""
    if tformat not in ('short', 'long'):
        log("Table must be in short or long format.", silent)
        return
    output = ""
    if tformat == 'short':
        log("Building 'short' Markdown table.", silent)
        output += "| Title | Release |\n"
        output += "| ----- | ------- |\n"
        count = 0
        while count < limit and count < len(games):
            name, data = games[count]
            output += f"| {name} | {min(data.release.keys()).strftime('%b %d')} |\n"
            count += 1
    else:
        log("Building 'long' Markdown table.", silent)
        output += "| Title | Systems | Release Dates |\n"
        output += "| ----- | ------- | ------------- |\n"
        count = 0
        while count < limit and count < len(games):
            name, data = games[count]
            output += f"| {name} | {', '.join(sorted(data.systems))} | "
            dates = data.release.keys()
            doutp = []
            if len(dates) == 1:
                doutp = [list(dates)[0].strftime('%B %d')]
            else:
                for date in dates:
                    doutp.append(f"{date.strftime('%B %d')}: ({', '.join(sorted(data.release[date]))})")
            output += f"{'; '.join(doutp)} |\n"
            count += 1
    return output

def post_table(reddit, subreddit, table, formatstring, ptype='sidebar'):
    """Make either a stickied post, or edit the sidebar to add a Markdown table."""
    if ptype not in ('sidebar', 'sticky'):
        log("Post type must be sticky or sidebar.", silent)
        return
    if ptype == "sidebar":
        log("Updating sidebar...", silent)
        sett = reddit.get_settings(subreddit)
        sidebar = formatstring.replace("%%%TABLE%%%", table)
        reddit.update_settings(reddit.get_subreddit(subreddit), description=sidebar)
        log("Sidebar updated successfully.", silent)
    else:
        log("Creating stickied post...", silent)
        post_title = f'Upcoming Games: {datetime.date.today().strftime("%B %d, %Y")}'
        post_data = formatstring.replace("%%%TABLE%%%", table)
        subr = reddit.subreddit(subreddit)
        post = subr.submit(post_title, post_data)
        post.distinguish()
        post.sticky()
        log("Stickied post created successfully.", silent)

__all__ = ['UpcomingGame', 'get_all_games', 'get_markdown']