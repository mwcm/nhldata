# 50 goal scorers

import pandas as pd
import matplotlib.pyplot as plt

SKATER_DATA_PATH = './skater_stats.csv'

sd = pd.read_csv(SKATER_DATA_PATH, encoding = "ISO-8859-1")

# skater data has:
# - a row for every unique combination of: 
#       - REG or POST season
#       - player id
#       - year
#       - team played for that regular season
#           - OR "TOT" for season total if multiple teams played for



# we mostly want to find data about 50 goal scorers
# - if we only care about 50 goal scorers we don't care about scoring avg's

# but, if we get into calculating the avg goals scored by players in a season
# we may not want drag down averages by including players who didn't play regularly
# - how do we define "regularly"?
# - do we include players who didn't play much but did score?
# - i think the point is get rid of ppl with few goals + few games
# - can figure this out w trial and error later


# so to start if we want to find all 50 goal seasons

# get all rows for a given player_id
# use TOT row if multiple exist for a specific year

# get rid of playoff stats
reg_rows = sd[sd["Game_Type"] == 'REG']

# yearly total rows for players who where traded midseason
multi_team_seasons_totals = reg_rows[reg_rows['Team_ID'] == "TOT"]

reg_rows_minus_tot_rows = reg_rows[reg_rows['Team_ID'] != "TOT"]

# seasons where a player played for a single team
single_team_seasons = reg_rows.drop_duplicates(subset=['Player_ID', 'Season'], keep=False)

# just double checking counts here
print(f' all REG season stats {len(reg_rows)}')
print(f' multi team season TOT rows {len(multi_team_seasons_totals)}')
print(f' reg  seasons stats MINUS TOT rows {len(reg_rows_minus_tot_rows)}')
print(f'single team seasons {len(single_team_seasons)}')
multi_team_season_rows_non_tot = pd.concat([reg_rows_minus_tot_rows, single_team_seasons]).drop_duplicates(keep=False)
print(f'multi team season rows NON tot {len(multi_team_season_rows_non_tot)}')
print(len(multi_team_season_rows_non_tot) + len(single_team_seasons))

# we only care about tot rows and single season rows
multi_team_tots_and_single_team_seasons = pd.concat([multi_team_seasons_totals, single_team_seasons]).drop_duplicates(keep=False)
print(len(multi_team_tots_and_single_team_seasons))
print(len(multi_team_tots_and_single_team_seasons) + len(multi_team_season_rows_non_tot))


# renamed filtered data
sd = multi_team_tots_and_single_team_seasons

# okay now, find which ones have over 50 goals, sort by year
fiftygoals = sd[sd['G'] >= 50].sort_values(by=['Season'])
print(len(fiftygoals))

# increase max row display wrt fiftygoals len
pd.set_option('display.max_rows', fiftygoals.shape[0]+1)

# print a selection of columns
# print(fiftygoals[['G', 'Season', 'Player_Name', 'Age', 'Team_Name']])

# scatter plot of each season and it's goal total through time
# p = fiftygoals.plot(x='Season', y='G', kind='scatter')
# for i, txt in enumerate(fiftygoals.Player_Name):
    # p.annotate(txt, (fiftygoals.Season.iat[i]+0.05, fiftygoals.G.iat[i]))

# - 50+ goal scorers per year as a bar
#fiftygoals.groupby('Season').Season.count().plot(x='Season', y='G', kind='bar')

# more than half of games, is that an alright definition?
regular_player_seasons = sd[sd['GP'] > 42].sort_values(by=['Season'])

# pts by season
#p = regular_players.plot(x='Season', y='PTS', kind='scatter')
#for i, txt in enumerate(regular_players.Player_Name):
#    p.annotate(txt, (regular_players.Season.iat[i]+0.05, regular_players.PTS.iat[i]))


std_devs = []

for i, txt in enumerate(set(regular_player_seasons.Season)):
    print(txt)
    players_in_season = regular_player_seasons[regular_player_seasons['Season'] == txt]
    goal_std_dev = players_in_season['G'].std()
    hscore_g = players_in_season['G'].max()
    mscore_g = players_in_season['G'].mean()
    lscore_g = players_in_season['G'].min()
    pts_std_dev = players_in_season['PTS'].std()
    hscore_pts = players_in_season['PTS'].max()
    mscore_pts = players_in_season['PTS'].mean()
    lscore_pts = players_in_season['PTS'].min()

    std_devs.insert(i, {})
    std_devs[i]['H_SCORE_PTS'] = hscore_pts
    std_devs[i]['M_SCORE_PTS'] = mscore_pts
    std_devs[i]['L_SCORE_PTS'] = lscore_pts
    std_devs[i]['H_SCORE_G'] = hscore_g
    std_devs[i]['M_SCORE_G'] = mscore_g
    std_devs[i]['L_SCORE_G'] = lscore_g
    std_devs[i]['G_STD'] = goal_std_dev
    std_devs[i]['PTS_STD'] = pts_std_dev
    std_devs[i]['Season'] = txt



std_dev_df = pd.DataFrame(data=std_devs)
print(std_dev_df)

 # it looks like these have both increased over time which flies in the face of the
 # rules in Full House Chapter 10
 # 1. "Complex systems improve when the best players play by the same rules over extended
 #   periods of time. As systems improve they equilibriate and variation decreases"
 #       - this one is debateable, I guess since some rules have changed over time

p = std_dev_df.plot(x='Season', y=['H_SCORE_PTS', 'M_SCORE_PTS', 'L_SCORE_PTS', 'PTS_STD'])
p = std_dev_df.plot(x='Season', y=['H_SCORE_G', 'M_SCORE_G', 'L_SCORE_G', 'G_STD'])


# next
#   - overall goals scored in league over time
#   - same things for goalie stats over time 



# pts by season
#p = regular_players.plot(x='Season', y='PTS', kind='scatter')
#for i, txt in enumerate(regular_players.Player_Name):
#    p.annotate(txt, (regular_players.Season.iat[i]+0.05, regular_players.PTS.iat[i]))

plt.show()


# plot these next