# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc
from basketball_reference_scraper.injury_report import get_injury_report
from basketball_reference_scraper.box_scores import get_box_scores
import logging
from logging.handlers import TimedRotatingFileHandler

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

TEAM_MAP = """
ATLANTA HAWKS : ATL
ST. LOUIS HAWKS : SLH
MILWAUKEE HAWKS : MIL
TRI-CITIES BLACKHAWKS : TCB
BOSTON CELTICS : BOS
BROOKLYN NETS : BRK
NEW JERSEY NETS : NJN
CHICAGO BULLS : CHI
CHARLOTTE HORNETS (1988-2004): CHH
CHARLOTTE HORNETS (2014-Present): CHO
CHARLOTTE BOBCATS : CHA
CLEVELAND CAVALIERS : CLE
DALLAS MAVERICKS : DAL
DENVER NUGGETS : DEN
DETROIT PISTONS : DET
FORT WAYNE PISTONS : FWP
GOLDEN STATE WARRIORS : GSW
SAN FRANCISCO WARRIORS : SFW
PHILADELPHIA WARRIORS : PHI
HOUSTON ROCKETS : HOU
INDIANA PACERS : IND
LOS ANGELES CLIPPERS : LAC
SAN DIEGO CLIPPERS : SDC
BUFFALO BRAVES : BUF
LOS ANGELES LAKERS : LAL
MINNEAPOLIS LAKERS : MIN
MEMPHIS GRIZZLIES : MEM
VANCOUVER GRIZZLIES : VAN
MIAMI HEAT : MIA
MILWAUKEE BUCKS : MIL
MINNESOTA TIMBERWOLVES : MIN
NEW ORLEANS PELICANS : NOP
NEW ORLEANS/OKLAHOMA CITY HORNETS : NOK
NEW ORLEANS HORNETS : NOH
NEW YORK KNICKS : NYK
OKLAHOMA CITY THUNDER : OKC
SEATTLE SUPERSONICS : SEA
ORLANDO MAGIC : ORL
PHILADELPHIA 76ERS : PHI
SYRACUSE NATIONALS : SYR
PHOENIX SUNS : PHO
PORTLAND TRAIL BLAZERS : POR
SACRAMENTO KINGS : SAC
KANSAS CITY KINGS : KCK
KANSAS CITY-OMAHA KINGS : KCK
CINCINNATI ROYALS : CIN
ROCHESTER ROYALS : ROR
SAN ANTONIO SPURS : SAS
TORONTO RAPTORS : TOR
UTAH JAZZ : UTA
NEW ORLEANS JAZZ : NOJ
WASHINGTON WIZARDS : WAS
WASHINGTON BULLETS : WAS
CAPITAL BULLETS : CAP
BALTIMORE BULLETS : BAL
CHICAGO ZEPHYRS : CHI
CHICAGO PACKERS : CHI
ANDERSON PACKERS : AND
CHICAGO STAGS : CHI
INDIANAPOLIS OLYMPIANS : IND
SHEBOYGAN RED SKINS : SRS
ST. LOUIS BOMBERS : SLB
WASHINGTON CAPITOLS : WAS
WATERLOO HAWKS : WAT
"""


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_stats_per_game(team, year=2021, dataformat='PER_GAME'):
    team_stats = get_team_stats(team, year, data_format=dataformat)
    return team_stats

def get_stats_per_game(team, year=2021, dataformat='PER_GAME'):
    team_stats = get_team_stats(team, year, data_format=dataformat)
    return team_stats

def get_opp_stats_per_game(team, year=2021, dataformat='PER_GAME'):
    team_stats = get_opp_stats(team, year, data_format=dataformat)
    return team_stats

def get_stats_per_poss(team, year=2021, dataformat='PER_POSS'):
    team_stats = get_team_stats(team, year, data_format=dataformat)
    return team_stats


def get_ppg(team):
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

def get_opp_ppg(team):
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


def get_injured(team):
    injured = get_injury_report()
    filter_ = injured['TEAM'] == team
    injured = injured[filter_]
    return injured

def get_pace(home_pace, away_pace, league_average=102.78):
    pace = home_pace * away_pace / league_average
    return pace

def get_ppp(offense, defense, league_average = 112.1):
    ppp = offense * defense / league_average
    return ppp

def get_final_score(ppp, pace):
    score = ppp * pace / 100
    return score

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = logger()
    nba_log = logging.getLogger('nbalog.'+ __name__)
    game = {
        'AWAY': 'POR',
        'HOME': 'SAS',
        'AWAY_PACE': 101.6,
        'HOME_PACE': 102.7
    }

    home_team = game.get('HOME')
    away_team = game.get('AWAY')
    home_team_pace = game.get('HOME_PACE')
    away_team_pace = game.get('AWAY_PACE')

    home_team_stats = get_stats_per_game(home_team)
    home_team_opp_stats = get_opp_stats_per_game(home_team)
    home_team_ppg = get_ppg(home_team_stats)
    home_team_opp_ppg = get_opp_ppg(home_team_opp_stats)

    away_team_stats = get_stats_per_game(away_team)
    away_team_opp_stats = get_opp_stats_per_game(away_team)
    away_team_ppg = get_ppg(away_team_stats)
    away_team_opp_ppg = get_opp_ppg(away_team_opp_stats)

    ## Offense calculation accounting for home/away
    home_team_offense = home_team_ppg * 1.014
    home_team_defense = home_team_opp_ppg - (.014 * home_team_opp_ppg)
    away_team_offense = away_team_ppg - (.014 * away_team_ppg)
    away_team_defense = away_team_opp_ppg + (.014 * away_team_opp_ppg)

    print('HOME: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(home_team, home_team_offense, home_team_defense))
    print('AWAY: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(away_team, away_team_offense, away_team_defense))
    nba_log.info('\nHOME: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(home_team, home_team_offense, home_team_defense))
    nba_log.info('\nAWAY: {} \nOff: {:.2f}\nDef: {:.2f}\n'.format(away_team, away_team_offense, away_team_defense))

    
    pace = get_pace(home_team_pace, away_team_pace)

    home_team_ppp = get_ppp(home_team_offense, away_team_defense)
    away_team_ppp = get_ppp(away_team_offense, home_team_defense)

    home_team_final_score = get_final_score(home_team_ppp, pace)
    away_team_final_score = get_final_score(away_team_ppp, pace)

    print('PREDICTION:\n {}: {}, {}: {}'.format(home_team, home_team_final_score, away_team, away_team_final_score))
    nba_log.info('\nPREDICTION:\n {}: {}, {}: {}'.format(home_team, home_team_final_score, away_team, away_team_final_score))



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