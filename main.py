# This is a sample Python script.
# api used is https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc
from basketball_reference_scraper.injury_report import get_injury_report
from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.seasons import get_schedule
import logging
import sendem
from logging.handlers import TimedRotatingFileHandler
from datetime import date, timedelta


def logger():
    logger = logging.getLogger('nbalog')

    logHandler = TimedRotatingFileHandler(filename="nba.log", when="midnight")
    logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logHandler.setFormatter(logFormatter)

    if not logger.handlers:
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        streamhandler.setFormatter(formatter)

        logger.addHandler(streamhandler)
        logger.addHandler(logHandler)


    # logger.error(message)
    logger.setLevel('INFO')
    return logger

TEAM_MAP = {
"ATLANTA HAWKS" : "ATL",
"BOSTON CELTICS" : "BOS",
"BROOKLYN NETS" : "BRK",
"CHICAGO BULLS" : "CHI",
"CHARLOTTE HORNETS" : "CHO",
"CLEVELAND CAVALIERS" : "CLE",
"DALLAS MAVERICKS" : "DAL",
"DENVER NUGGETS" : "DEN",
"DETROIT PISTONS" : "DET",
"GOLDEN STATE WARRIORS" : "GSW",
"HOUSTON ROCKETS" : "HOU",
"INDIANA PACERS" : "IND",
"LOS ANGELES CLIPPERS" : "LAC",
"LOS ANGELES LAKERS" : "LAL",
"MEMPHIS GRIZZLIES" : "MEM",
"MIAMI HEAT" : "MIA",
"MILWAUKEE BUCKS" : "MIL",
"MINNESOTA TIMBERWOLVES" : "MIN",
"NEW ORLEANS PELICANS" : "NOP",
"NEW YORK KNICKS" : "NYK",
"OKLAHOMA CITY THUNDER" : "OKC",
"ORLANDO MAGIC" : "ORL",
"PHILADELPHIA 76ERS" : "PHI",
"PHOENIX SUNS" : "PHO",
"PORTLAND TRAIL BLAZERS" : "POR",
"SACRAMENTO KINGS" : "SAC",
"SAN ANTONIO SPURS" : "SAS",
"TORONTO RAPTORS" : "TOR",
"UTAH JAZZ" : "UTA",
"WASHINGTON WIZARDS" : "WAS"
}

LOGO_MAP = {
"ATLANTA HAWKS" : "https://content.sportslogos.net/logos/6/220/thumbs/22081902021.gif",
"MILWAUKEE HAWKS" : "MIL",
"BOSTON CELTICS" : "https://content.sportslogos.net/logos/6/213/thumbs/slhg02hbef3j1ov4lsnwyol5o.gif",
"BROOKLYN NETS" : "https://content.sportslogos.net/logos/6/3786/thumbs/hsuff5m3dgiv20kovde422r1f.gif",
"CHICAGO BULLS" : "https://content.sportslogos.net/logos/6/221/thumbs/hj3gmh82w9hffmeh3fjm5h874.gif",
"CHARLOTTE HORNETS" : "https://content.sportslogos.net/logos/6/5120/thumbs/512019262015.gif",
"CLEVELAND CAVALIERS" : "https://content.sportslogos.net/logos/6/222/thumbs/22269212018.gif",
"DALLAS MAVERICKS" : "https://content.sportslogos.net/logos/6/228/thumbs/22834632018.gif",
"DENVER NUGGETS" : "https://content.sportslogos.net/logos/6/229/thumbs/22989262019.gif",
"DETROIT PISTONS" : "https://content.sportslogos.net/logos/6/223/thumbs/22321642018.gif",
"GOLDEN STATE WARRIORS" : "https://content.sportslogos.net/logos/6/235/thumbs/23531522020.gif",
"HOUSTON ROCKETS" : "https://content.sportslogos.net/logos/6/230/thumbs/23068302020.gif",
"INDIANA PACERS" : "https://content.sportslogos.net/logos/6/224/thumbs/22448122018.gif",
"LOS ANGELES CLIPPERS" : "https://content.sportslogos.net/logos/6/236/thumbs/23637762019.gif",
"LOS ANGELES LAKERS" : "https://content.sportslogos.net/logos/6/237/thumbs/uig7aiht8jnpl1szbi57zzlsh.gif",
"MEMPHIS GRIZZLIES" : "https://content.sportslogos.net/logos/6/231/thumbs/23143732019.gif",
"MIAMI HEAT" : "https://content.sportslogos.net/logos/6/214/thumbs/burm5gh2wvjti3xhei5h16k8e.gif",
"MILWAUKEE BUCKS" : "https://content.sportslogos.net/logos/6/225/thumbs/22582752016.gif",
"MINNESOTA TIMBERWOLVES" : "https://content.sportslogos.net/logos/6/232/thumbs/23296692018.gif",
"NEW ORLEANS PELICANS" : "https://content.sportslogos.net/logos/6/4962/thumbs/496226812014.gif",
"NEW YORK KNICKS" : "https://content.sportslogos.net/logos/6/216/thumbs/2nn48xofg0hms8k326cqdmuis.gif",
"OKLAHOMA CITY THUNDER" : "https://content.sportslogos.net/logos/6/2687/thumbs/khmovcnezy06c3nm05ccn0oj2.gif",
"ORLANDO MAGIC" : "https://content.sportslogos.net/logos/6/217/thumbs/wd9ic7qafgfb0yxs7tem7n5g4.gif",
"PHILADELPHIA 76ERS" : "https://content.sportslogos.net/logos/6/218d/thumbs/21870342016.gif",
"PHOENIX SUNS" : "https://content.sportslogos.net/logos/6/238/thumbs/23843702014.gif",
"PORTLAND TRAIL BLAZERS" : "https://content.sportslogos.net/logos/6/239/thumbs/23997252018.gif",
"SACRAMENTO KINGS" : "https://content.sportslogos.net/logos/6/240/thumbs/24040432017.gif",
"SAN ANTONIO SPURS" : "https://content.sportslogos.net/logos/6/233/thumbs/23325472018.gif",
"TORONTO RAPTORS" : "https://content.sportslogos.net/logos/6/227/thumbs/22770242021.gif",
"UTAH JAZZ" : "https://content.sportslogos.net/logos/6/234/thumbs/23467492017.gif",
"WASHINGTON WIZARDS" : "https://content.sportslogos.net/logos/6/219/thumbs/21956712016.gif"
}

exception_list = ['Golden State Warriors', 'Los Angeles Lakers', 'Los Angeles Clippers', 'New Orleans Pelicans',
                  'New York Knicks', 'Oklahoma City Thunder', 'San Antonio Spurs']

PACE_MAP = {
  "Washington": 106.4,
  "Golden State": 104.4,
  "Milwaukee": 104.3,
  "Minnesota": 104.2,
  "Indiana": 103.9,
  "Houston": 103.6,
  "Oklahoma City": 103.2,
  "Memphis": 102.7,
  "Sacramento": 102.2,
  "New Orleans": 102.2,
  "Philadelphia": 101.9,
  "Brooklyn": 101.9,
  "Toronto": 101.6,
  "Chicago": 101.1,
  "Utah": 101.0,
  "Portland": 100.9,
  "San Antonio": 100.9,
  "Orlando": 100.8,
  "LA Lakers": 100.7,
  "Charlotte": 100.7,
  "Boston": 100.7,
  "Detroit": 100.1,
  "Atlanta": 99.8,
  "Cleveland": 99.5,
  "Dallas": 99.4,
  "Denver": 99.3,
  "Phoenix": 99.1,
  "LA Clippers": 99.0,
  "Miami": 98.8,
  "New York": 98.3
}


class BasketballTeamApi:
    def __init__(self):
        self.year = 2021


    def get_stats_per_game(self, team, dataformat='PER_GAME'):
        team_stats = get_team_stats(team, self.year, data_format=dataformat)
        return team_stats


    def get_opp_stats_per_game(self, team, dataformat='PER_GAME'):
        team_stats = get_opp_stats(team, self.year, data_format=dataformat)
        return team_stats


    def get_stats_per_poss(self, team, dataformat='PER_POSS'):
        team_stats = get_team_stats(team, self.year, data_format=dataformat)
        return team_stats


    def get_todays_schedule(self):
        schedule = get_schedule(self.year + 1)
        today = date.today().strftime('%Y-%m-%d')
        #print(today)
        # today = '2021-10-20'
        #today = date.today().strftime("%Y-%m-%d")
        filtered = schedule.loc[schedule['DATE'] == today]
        #print(filtered)
        games_list = ""
        texts_list = ""
        for i, row in filtered.iterrows():
            visitor = row['VISITOR'].upper()
            home = row['HOME'].upper()
            print(f"{row['VISITOR']} vs {row['HOME']}")
            if visitor in TEAM_MAP and home in TEAM_MAP:
                visitor_pace_lookup = row['VISITOR']
                home_pace_lookup = row['HOME']
                if visitor_pace_lookup in exception_list:
                    if visitor_pace_lookup == "Los Angeles Clippers":
                        visitor_pace_lookup = "LA Clippers"
                    elif visitor_pace_lookup == "Los Angeles Lakers":
                        visitor_pace_lookup = "LA Lakers"
                    else:
                        visitor_pace_lookup = ' '.join(visitor_pace_lookup.split(" ")[:2])
                else:
                    visitor_pace_lookup = visitor_pace_lookup.split(" ")[0]
                if home_pace_lookup in exception_list:
                    if home_pace_lookup == "Los Angeles Clippers":
                        home_pace_lookup = "LA Clippers"
                    elif home_pace_lookup == "Los Angeles Lakers":
                        home_pace_lookup = "LA Lakers"
                    else:
                        home_pace_lookup = ' '.join(home_pace_lookup.split(" ")[:2])
                else:
                    home_pace_lookup = home_pace_lookup.split(" ")[0]
                game = {
                    'AWAY': TEAM_MAP[visitor],
                    'HOME': TEAM_MAP[home],
                    'AWAY_PACE': PACE_MAP[visitor_pace_lookup],
                    'HOME_PACE': PACE_MAP[home_pace_lookup]
                }
                visitor_score, home_score = self.predict_the_game(game)
                # games_list += """<div class='w3-panel w3-card'>
                # <img src='{}' alt='{}'> @ <img src='{}' alt='{}'>  <p>{}</p>
                # </div>""".format(
                #     LOGO_MAP[visitor],
                #     TEAM_MAP[visitor],
                #     LOGO_MAP[home],
                #     TEAM_MAP[home], prediction)

                games_list += """<div class='w3-panel w3-card'> 
                <div>
                <img src='{}' alt='{}' style='display: inline-block'>
                <h4 style='display: inline-block'>{:.2f}</h4>
                </div>
                <div><h4>@</h4></div>
                 <div><img src='{}' alt='{}' style='display: inline-block'> 
                                  <h4 style='display: inline-block'>{:.2f}</h4>
                                  </div>
                </div>""".format(
                    LOGO_MAP[visitor],
                    TEAM_MAP[visitor],
                    visitor_score,
                    LOGO_MAP[home],
                    TEAM_MAP[home],
                    home_score,
                    )

                texts_list += "{} @ {}".format(row['VISITOR'], row['HOME'])
        text = """
        GAMES TODAY:
        {}
        """.format(texts_list)
        html = """
        <html>
        <style>
        .w3-panel:after,.w3-panel:before {{
        content:'';
        display:table;
        clear:both
        }}
        

        
        .w3-panel{{padding:6px 16px}}
        .w3-panel{{margin-top:16px;margin-bottom:16px}}
        .w3-card,.w3-card-2{{
        box-shadow:0 2px 5px 0 rgba(0,0,0,0.16),0 2px 10px 0 rgba(0,0,0,0.12); 
        border: 1px solid black;}}
        </style>
        
        <body>
        <br>GAMES TODAY: {}<br>
         
         {}
         
        </body>
        </html>
        """.format(today, games_list)

        sendem.send_the_email(text, html)


    def get_ppg(self, team):
        """
        Accepts dataframe object
        :param team: dataframe
        :return:
        """
        threes = team['3P']
        twos = team['2P']
        fts = team['FT']
        pts_threes = threes * 3
        pts_twos = twos * 2
        pts_fts = fts * 1
        total = pts_fts + pts_twos + pts_threes
        return total


    def get_opp_ppg(self, team):
        """
        :param team: accepts dataframe of opponent stats
        :return:
        """
        threes = team['OPP_3P']
        twos = team['OPP_2P']
        fts = team['OPP_FT']
        pts_threes = threes * 3
        pts_twos = twos * 2
        pts_fts = fts * 1
        total = pts_fts + pts_twos + pts_threes
        return total


    def get_injured(self, team):
        injured = get_injury_report()
        filter_ = injured['TEAM'] == team
        injured = injured[filter_]
        return injured


    def get_pace(self, home_pace, away_pace, league_average=101.42):
        pace = home_pace * away_pace / league_average
        return pace


    def get_ppp(self, offense, defense, league_average = 112.3):
        ppp = offense * defense / league_average
        return ppp


    def get_final_score(self, ppp, pace):
        score = ppp * pace / 100
        return score


    def predict_the_game(self, game):
        '''
        :param game: dictionary
            game = {
            'AWAY': 'NYK',
            'HOME': 'ATL',
            'AWAY_PACE': 98.2,
            'HOME_PACE': 99.9
            }
        :return:
        '''
        home_team = game.get('HOME')
        away_team = game.get('AWAY')
        home_team_pace = game.get('HOME_PACE')
        away_team_pace = game.get('AWAY_PACE')

        home_team_stats = self.get_stats_per_game(home_team)
        home_team_opp_stats = self.get_opp_stats_per_game(home_team)
        home_team_ppg = self.get_ppg(home_team_stats)
        home_team_opp_ppg = self.get_opp_ppg(home_team_opp_stats)

        away_team_stats = self.get_stats_per_game(away_team)
        away_team_opp_stats = self.get_opp_stats_per_game(away_team)
        away_team_ppg = self.get_ppg(away_team_stats)
        away_team_opp_ppg = self.get_opp_ppg(away_team_opp_stats)

        ## Offense calculation accounting for home/away
        home_team_offense = home_team_ppg * 1.014
        home_team_defense = home_team_opp_ppg - (.014 * home_team_opp_ppg)
        away_team_offense = away_team_ppg - (.014 * away_team_ppg)
        away_team_defense = away_team_opp_ppg + (.014 * away_team_opp_ppg)

       # print('HOME: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(home_team, home_team_offense, home_team_defense))
       # print('AWAY: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(away_team, away_team_offense, away_team_defense))
       # nba_log.info('\nHOME: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(home_team, home_team_offense, home_team_defense))
       # nba_log.info('\nAWAY: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(away_team, away_team_offense, away_team_defense))

        pace = self.get_pace(home_team_pace, away_team_pace)

        home_team_ppp = self.get_ppp(home_team_offense, away_team_defense)
        away_team_ppp = self.get_ppp(away_team_offense, home_team_defense)

        home_team_final_score = self.get_final_score(home_team_ppp, pace)
        away_team_final_score = self.get_final_score(away_team_ppp, pace)

        #print('PREDICTION:\n {}: {}, {}: {}'.format(away_team, away_team_final_score, home_team, home_team_final_score))
        #nba_log.info(
        #    '\nPREDICTION:\n {}: {}, {}: {}'.format(away_team, away_team_final_score, home_team, home_team_final_score))
        prediction = '{}: {}, {}: {}'.format(away_team, away_team_final_score, home_team, home_team_final_score)
        return away_team_final_score, home_team_final_score


    def get_average_pace(self):
        league_misc = {v: get_team_misc(v, 2021) for k, v in TEAM_MAP.items()}
        average_pace = sum([stats['PACE'] for team, stats in league_misc.items()]) / len(league_misc)
        return average_pace




def get_html(today, games_list):
    html = """
    <html>
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <body>
    <br>GAMES TODAY: {}<br>
     <ul>
     {}
     </ul>
    </body>
    </html>
    """.format(today, games_list)
    return html

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = logger()
    nba_log = logging.getLogger('nbalog.'+ __name__)
    game = {
        'AWAY': 'NYK',
        'HOME': 'ATL',
        'AWAY_PACE': 98.2,
        'HOME_PACE': 99.9
    }

    bapi = BasketballTeamApi()
    bapi.get_todays_schedule()
    #get_todays_schedule()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/





#get_team_stats(team, season_end_year, data_format='PER_GAME')
#Parameters:
#
#team - NBA team abbreviation (e.g. 'GSW', 'SAS')
#season_end_year - Desired end year (e.g. 1988, 2011)
#data_format - One of 'TOTAL'|'PER_GAME'|'PER_POSS'. Default value is 'PER_GAME'
#Returns:

#get_box_scores(date, team1, team2, period='GAME', stat_type='BASIC')
#Parameters:
#date - Desired date in a string format (e.g. '2020-01-06')
#team1 - One of the team abbreviation (e.g. 'DEN', 'GSW')
#team2 - Other team abbreviation (e.g. 'DEN', 'GSW')
#period - Period for which to acquire stats. One of 'GAME'|'Q1'|'Q2'|'Q3'|'Q4'|'H1'|'H2'. Default value is 'GAME'
#stat_type - Period for which to acquire stats. One of 'BASIC'|'ADVANCED'. Default value is 'BASIC'. Note that advanced stats are only available for period='GAME'.