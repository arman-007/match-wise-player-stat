import requests
import os
import json

import os
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv

# Define the base directory as the directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Go one directory up to find the .env file in the project root
dotenv_path = BASE_DIR.parent / '.env' 

load_dotenv(dotenv_path=dotenv_path)

# You can now access your variables
MATCH_ID = os.environ.get("MATCH_ID")
API_KEY = os.environ.get("APIFOOTBALL_API_KEY")

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")


def fetch_players_from_db(player_names: list):
    """Fetch player data from MongoDB based on display_name or name."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Query MongoDB for all players by display_name or name in one go
        query = {
            "$or": [
                {"display_name": {"$in": player_names}},
                {"name": {"$in": player_names}}
            ]
        }

        players = collection.find(query)
        
        # Build a dictionary where both display_name and name can be used as keys
        player_data_dict = {}

        for player in players:
            # Use display_name as the primary key, and name as a fallback
            player_data_dict[player["display_name"].strip()] = player
            if player["name"].strip() != player["display_name"].strip():
                player_data_dict[player["name"].strip()] = player

        return player_data_dict
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def main():

    response = requests.get(f"https://apiv3.apifootball.com/?action=get_statistics&match_id={MATCH_ID}&APIkey={API_KEY}")
    result = response.json()

    player_stats = result[MATCH_ID]["player_statistics"]

    stats=[]
    player={}
    for player_stat in player_stats:
        player["player_id"] = player_stat.get("player_id", "SHOULD GET FROM SPORTMONKS")
        player["team_id"] = player_stat.get("team_id", "SHOULD GET FROM SPORTMONKS")
        player["fixture_id"] = player_stat.get("fixture_id", "NEED TO BE CLEARED")
        player["api_player_id"] = player_stat.get("player_key", "NOT FOUND IN APIFOOTBALL")
        player["api_team_id"] = player_stat.get("api_team_id", "SHOULD GET FROM USED API SOURCE")
        player["api_fixture_id"] = player_stat.get("api_fixture_id", "SHOULD GET FROM USED API SOURCE")
        player["display_name"] = player_stat.get("player_name", "SHOULD GET FROM SPORTMONKS")
        player["goals_scored"] = player_stat.get("player_goals", "NOT FOUND IN APIFOOTBALL")
        player["assists"] = player_stat.get("player_assists", "NOT FOUND IN APIFOOTBALL")
        player["saves"] = player_stat.get("player_saves", "NOT FOUND IN APIFOOTBALL")
        player["yellow_cards"] = player_stat.get("player_yellowcards", "NOT FOUND IN APIFOOTBALL")
        player["red_cards"] = player_stat.get("player_redcards")
        player["yellowred_cards"] = player_stat.get("yellowred_cards", "NEED TO BE CLEARED")
        player["penalties_won"] = player_stat.get("player_pen_won", "NOT FOUND IN APIFOOTBALL")
        player["penalties_saved"] = player_stat.get("player_pen_save", "NOT FOUND IN APIFOOTBALL")
        player["penalties_missed"] = player_stat.get("player_pen_miss", "NOT FOUND IN APIFOOTBALL")
        player["penalties_scored"] = player_stat.get("player_pen_score", "NOT FOUND IN APIFOOTBALL")
        player["penalties_committed"] = player_stat.get("player_pen_committed", "NOT FOUND IN APIFOOTBALL")
        player["own_goals"] = player_stat.get("own_goals", "NEED TO FIND A SOURCE")
        player["starting_at"] = player_stat.get("starting_at", "NEED TO FIND A SOURCE")
        player["minutes_played"] = player_stat.get("player_minutes_played", "NOT FOUND IN APIFOOTBALL")
        player["successful_passes"] = player_stat.get("player_passes_acc", "NOT FOUND IN APIFOOTBALL")
        player["successful_dribbles"] = player_stat.get("player_dribble_succ", "NOT FOUND IN APIFOOTBALL")
        player["error_lead_to_goal"] = player_stat.get("error_lead_to_goal", "NEED TO FIND A SOURCE")
        player["error_lead_to_shot"] = player_stat.get("error_lead_to_shot", "NEED TO FIND A SOURCE")
        player["shots_off_target"] = int(player_stat.get("player_shots_total")) - int(player_stat.get("player_shots_on_goal"))
        player["shots_on_target"] = player_stat.get("player_shots_on_goal", "NOT FOUND IN APIFOOTBALL")
        player["clearances"] = player_stat.get("player_clearances", "NOT FOUND IN APIFOOTBALL")
        player["shots_blocked"] = player_stat.get("player_blocks", "NOT FOUND IN APIFOOTBALL")
        player["accurate_crosses"] = player_stat.get("player_acc_crosses", "NOT FOUND IN APIFOOTBALL")
        player["big_chances_created"] = player_stat.get("big_chances_created", "NEED TO FIND A SOURCE")
        player["long_balls_won"] = player_stat.get("long_balls_won", "NEED TO FIND A SOURCE")
        player["interceptions"] = player_stat.get("player_interceptions", "NOT FOUND IN APIFOOTBALL")
        player["key_passes"] = player_stat.get("player_key_passes", "NOT FOUND IN APIFOOTBALL")
        player["successful_dribbles"] = player_stat.get("player_dribble_succ", "NOT FOUND IN APIFOOTBALL")
        player["through_balls_won"] = player_stat.get("through_balls_won", "NEED TO FIND A SOURCE")
        player["tackles"] = player_stat.get("player_tackles", "NOT FOUND IN APIFOOTBALL")
        player["fouls"] = player_stat.get("fouls", "AVAILABLE IN APIFOOTBALL: \"player_fouls_drawn\", \"player_fouls_commited\"")
        player["clean_sheets"] = player_stat.get("clean_sheets", "NOT FOUND IN APIFOOTBALL")
        player["gc"] = player_stat.get("gc", "AVAILABLE IN APIFOOTBALL: \"player_goals_conceded\"")
        player["position"] = player_stat.get("position", "SHOULD GET FROM SPORTMONKS")
        player["position_group"] = player_stat.get("position_group", "SHOULD GET FROM SPORTMONKS")
        player["bonus_points"] = player_stat.get("bonus_points", "NEED TO FIND A SOURCE OR CALCULATE")
        player["bps"] = player_stat.get("bps", "NOT SURE ABOUT THIS FIELD")
        player["total_points"] = player_stat.get("total_points", "NEED TO CALCULATE")
        player["cs"] = player_stat.get("cs", "NOT SURE ABOUT THIS FIELD")
        player["xG"] = player_stat.get("xG", "NEED TO CALCULATE")
        player["xA"] = player_stat.get("xA", "NEED TO CALCULATE")
        player["xA_per_90"] = player_stat.get("xA_per_90", "NEED TO CALCULATE")
        player["dispossessed"] = player_stat.get("player_dispossesed", "NOT FOUND IN APIFOOTBALL")
        player["dribbled_past"] = player_stat.get("player_dribbled_past", "NOT FOUND IN APIFOOTBALL")
        player["fouls_drawn"] = player_stat.get("player_fouls_drawn", "NOT FOUND IN APIFOOTBALL")
        player["recoveries"] = player_stat.get("recoveries", "NEED TO CALCULATE")
        player["recoveries_per_90"] = player_stat.get("recoveries_per_90", "NEED TO CALCULATE")
        player["duels_won"] = player_stat.get("player_duels_won", "NOT FOUND IN APIFOOTBALL")
        player["duels_lost"] = int(player_stat.get("player_duels_total")) - int(player_stat.get("player_duels_won"))
        player["aerials_won"] = player_stat.get("player_aerials_won", "NOT FOUND IN APIFOOTBALL")
        player["aerials_lost"] = player_stat.get("aerials_lost", "NEED TO FIND A SOURCE")
        player["blocked_shots"] = player_stat.get("player_blocks", "NOT FOUND IN APIFOOTBALL")
        player["offsides"] = player_stat.get("player_offsides", "NOT FOUND IN APIFOOTBALL")
        player["offsides_provoked"] = player_stat.get("fouls_committed", "NEED TO FIND A SOURCE")
        player["big_chances_missed"] = player_stat.get("big_chances_missed", "NEED TO FIND A SOURCE")
        player["price"] = player_stat.get("price", "NEED TO GET FROM SCRAPER")
        player["player_in_count"] = player_stat.get("player_in_count", "NNED TO FIND A SOURCE")
        player["player_out_count"] = player_stat.get("player_out_count", "NNED TO FIND A SOURCE")
        player["gameweek_code"] = player_stat.get("gameweek_code", "NNED TO FIND A SOURCE")
        player["is_home"] = True if player_stat.get("team_name") == "home" else False

        stats.append(player)
        player={}

    with open("Player_stats_for_match_id_" + str(MATCH_ID) + ".json", "w") as f:
        json.dump(stats, f, indent=2)
    print("Player_stats_for_match_id_" + str(MATCH_ID) + ".json")



if __name__ == "__main__":
    main()