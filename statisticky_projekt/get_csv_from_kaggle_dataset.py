# VYGENEROVÁNO GEMINI
import os
import pandas as pd
from dotenv import load_dotenv

# 1. NAČTENÍ PŘÍSTUPŮ KE KAGGLE (musí být před importem kaggle)
print("Načítám prostředí...")
load_dotenv()
import kaggle

# 2. STAŽENÍ DAT
dataset_name = 'martinellis/nhl-game-data'
print(f"Stahuji a rozbaluji dataset: {dataset_name} (to může chvíli trvat)...")
kaggle.api.dataset_download_files(dataset_name, path='.', unzip=True)
print("Data stažena a rozbalena!")

# 3. ZPRACOVÁNÍ ZÁKLADNÍCH INFORMACÍ O ZÁPASECH A TÝMECH
print("Načítám tabulku zápasů...")
games = pd.read_csv('game.csv')

# Najdeme nejnovější sezónu a vyfiltrujeme pouze zápasy základní části (Regular season - 'R')
latest_season = games['season'].max()
print(f"Zpracovávám nejnovější dostupnou sezónu: {latest_season}")

games_latest = games[(games['season'] == latest_season) & (games['type'] == 'R')].copy()
game_ids = games_latest['game_id'].unique() # Seznam ID zápasů pro filtrování dalších tabulek

# Slovník pro překlad team_id na srozumitelný název (např. 'BOS', 'TBL')
teams = pd.read_csv('team_info.csv')
team_dict = dict(zip(teams['team_id'], teams['shortName']))


# =====================================================================
# HYPOTÉZA 1: DOMÁCÍ PROSTŘEDÍ A PRVNÍ GÓL
# =====================================================================
print("Zpracovávám data pro 1. CSV (Zápasy a góly)...")

# A. Kdo vyhrál zápas
games_latest['winning_team_id'] = games_latest.apply(
    lambda row: row['home_team_id'] if row['home_goals'] > row['away_goals'] else row['away_team_id'], 
    axis=1
)

# B. Kdo dal první gól (načítáme jen nutné sloupce kvůli úspoře RAM)
plays = pd.read_csv('game_plays.csv', usecols=['play_id', 'game_id', 'event', 'team_id_for'])
# Vyfiltrujeme jen góly z naší vybrané sezóny
goals = plays[(plays['game_id'].isin(game_ids)) & (plays['event'] == 'Goal')].copy()

# Seřadíme události a vezmeme úplně první gól každého zápasu
first_goals = goals.sort_values(['game_id', 'play_id']).groupby('game_id').first().reset_index()
first_goals = first_goals[['game_id', 'team_id_for']].rename(columns={'team_id_for': 'first_goal_team_id'})

# C. Spojení dat dohromady
df_h1 = pd.merge(games_latest, first_goals, on='game_id', how='left')

# D. Překlad ID na textové názvy týmů pro přehlednost
df_h1['Domaci'] = df_h1['home_team_id'].map(team_dict)
df_h1['Hoste'] = df_h1['away_team_id'].map(team_dict)
df_h1['Prvni_gol_tym'] = df_h1['first_goal_team_id'].map(team_dict)
df_h1['Vitez_zapasu'] = df_h1['winning_team_id'].map(team_dict)

# Finální úprava a uložení
final_csv1 = df_h1[['game_id', 'Domaci', 'Hoste', 'home_goals', 'away_goals', 'Prvni_gol_tym', 'Vitez_zapasu']]
final_csv1.to_csv('1_hypoteza_zapasove_statistiky.csv', index=False)
print("-> Soubor '1_hypoteza_zapasove_statistiky.csv' byl vytvořen.")


# =====================================================================
# HYPOTÉZA 2: HRÁČI, VĚK A ČAS NA LEDĚ (TOI)
# =====================================================================
print("Zpracovávám data pro 2. CSV (Hráči a čas na ledě)...")

# A. Čas na ledě (opět šetříme RAM)
stats = pd.read_csv('game_skater_stats.csv', usecols=['game_id', 'player_id', 'timeOnIce'])
stats_latest = stats[stats['game_id'].isin(game_ids)].copy()

# Výpočet průměrného času na ledě (v datasetu je v sekundách, převedeme na minuty)
player_toi = stats_latest.groupby('player_id')['timeOnIce'].mean().reset_index()
player_toi['Prumerny_cas_na_lede_min'] = round(player_toi['timeOnIce'] / 60, 2)

# B. Informace o hráčích (věk a jméno)
players = pd.read_csv('player_info.csv', usecols=['player_id', 'firstName', 'lastName', 'birthDate'])
players['Hrac'] = players['firstName'] + ' ' + players['lastName']

# Výpočet věku: Rok začátku sezóny (např. pro 20192020 je to 2019) minus rok narození
season_start_year = int(str(latest_season)[:4])
players['birth_year'] = pd.to_datetime(players['birthDate'], errors='coerce').dt.year
players['Vek'] = season_start_year - players['birth_year']

# C. Spojení a uložení
df_h2 = pd.merge(player_toi, players, on='player_id', how='inner')
final_csv2 = df_h2[['Hrac', 'Vek', 'Prumerny_cas_na_lede_min']].dropna()

final_csv2.to_csv('2_hypoteza_hracske_statistiky.csv', index=False)
print("-> Soubor '2_hypoteza_hracske_statistiky.csv' byl vytvořen.")

print("Vše hotovo! Obě CSV máš připravená pro svůj statistický projekt.")