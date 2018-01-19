# upcoming-games

[![PyPI](https://img.shields.io/pypi/v/aav.upcoming-games.svg?style=for-the-badge)](https://pypi.python.org/pypi/aav.upcoming-games)

Reddit bot to update sidebar for /r/IGN. Can be configured for a variety of uses.

# Usage

1. Install Python 3.6 or greater if you have not already.
2. Install the bot with `pip install aav.upcoming-games`. You may need to use `sudo` or `pip3` or `--user` depending on your permissions, i.e. if you do not have sudo permissions and you also have Python 2 installed, you may need to use `pip3 install --user aav.upcoming-games`.
3. Obtain a Reddit client ID and client secret from https://reddit.com/prefs/apps on the account you want to use for the bot.
4. Set up your configuration file and template as mentioned in the 'Configuration' section.
5. Run the bot from the command line with the full path to your config file: `upcoming-games "/home/aav/my.yaml"`

# Developer Usage

1. Install Python 3.6 or greater if you have not already.
2. Install the bot with `pip install aav.upcoming-games`. You may need to use `sudo` or `pip3` or `--user` depending on your permissions, i.e. if you do not have sudo permissions and you also have Python 2 installed, you may need to use `pip3 install --user aav.upcoming-games`.
3. `import upcoming_games`
4. You can use any of the three functions: `get_all_games`, `get_markdown`, `post_table`, and the class `UpcomingGame` as desired.

# Configuration

Here is the default configuration file:
```yaml
general:
  silent: False
  time_period: "7d"
  systems: []
  game_limit: 10
  table_format: "short"

reddit:
  client_id: "..."
  client_secret: "..."
  subreddit: "..."
  scripthost: "..."
  password: "..."
  post_type: "sidebar"
  template: 'path/to/template.txt'
```

Here's what each setting is for:

- `general`
  - `silent` - True if you don't want any script output.
  - `time_period` - Valid time period for upcoming games (can be one of `7d, 1m, 3m, 6m, 12m, all`).
  - `system` - List of consoles you want to include releases for. Empty means include all.
  - `game_limit` - Number of games you want for the Markdown table.
  - `table_format` - `short` for only the game name and first release, `long` for system details.
- `reddit`
  - `client_id` - Your reddit bot's client ID.
  - `client_secret` - Your reddit bot's client secret.
  - `subreddit` - The subreddit (your must be a moderator) to post to/update the sidebar.
  - `scripthost` - The username for the bot account you registered for the client ID on.
  - `password` - The password for the bot account.
  - `post_type` - `sidebar` to update the sidebar, `sticky` to make a 'bottom' stickied post.
  - `template` - the full path to the template you want to use.

Note the template must contain somewhere in it the text %%%TABLE%%%, as this is where the Markdown table will be put. If no path or an invalid path is specified, the template used will be blank, i.e. it will only contain the Markdown table, nothing else.