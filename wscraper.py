from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
#driver = webdriver.Chrome("C:\Users\scedd\Documents\rwsDEV\chromedriver_win32d\chromedriver")
driver = webdriver.Chrome("/Users/scedd/Documents/universal_dependencies/chromedriver", options=chrome_options)
driver.get('http://www.espn.com/nba/hollinger/teamstats/_/sort/paceFactor')


rows = 1 + len(driver.find_elements_by_xpath('//tbody//tr'))
cols = len(driver.find_elements_by_xpath('//tbody//tr[3]//td'))
print(rows)
print(cols)


teams = []
team_pace = []
# Printing the data of the table
for r in range(3, rows):
    for p in range(1, cols + 1):
        # obtaining the text from each column of the table
        value = driver.find_element_by_xpath(
            "//tbody//tr[" + str(
                r) + "]//td[" + str(p) + "]").text

        if p==2:
            teams.append(value)
        elif p==3:
            team_pace.append(value)
        else:
            pass


print(teams)
print(team_pace)

#turn pace data into floats
for i, p in enumerate(team_pace):
    team_pace[i] = float(p)


res = dict(zip(teams, team_pace))
pace_dict = {}
for key in teams:
    for p in team_pace:
        pace_dict[key] = p

print(res)

def get_average(statslist):
    sum = 0    for ele in statslist:

        sum += ele
    res = sum / len(statslist)
    return res

def get_avg_pandas(statslist):
    pass

print(get_average(team_pace))



