import os
import json


FINAL_STATS = []


def read_json_file(folder_name: str, file_name: str) -> dict:
    """
    Reads the JSON file from the 'input' folder and returns its contents as a dictionary.

    Args:
        file_name (str): The name of the JSON file to read.

    Returns:
        dict: The contents of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist in the 'input' folder.
        json.JSONDecodeError: If the file is not a valid JSON.
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(current_directory, folder_name)

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The 'input' folder does not exist at {input_folder}.")

    file_path = os.path.join(input_folder, file_name)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_name}' does not exist in the 'input' folder.")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_name}: {str(e)}")
        raise
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")

def write_json_to_file(data: list, output_folder: str, output_file_name: str):
    """
    Writes the given data (list of dictionaries) to a JSON file in the specified folder.

    Args:
        data (list): The data to write to the JSON file, usually in the form of a list of dictionaries.
        output_folder (str): The folder where the JSON file should be saved.
        output_file_name (str): The name of the output JSON file.

    Raises:
        FileNotFoundError: If the specified folder does not exist.
        IOError: If there is an error writing to the file.
    """

    # Get the current working directory and ensure the folder exists
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_folder_path = os.path.join(current_directory, output_folder)

    # Check if the folder exists, if not create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Define the path to the output file
    output_file_path = os.path.join(output_folder_path, output_file_name)

    try:
        # Open the file in write mode and dump the data as a JSON string
        with open(output_file_path, 'w') as output_file:
            json.dump(data, output_file, indent=4)
        print(f"Data successfully written to {output_file_path}")
    except IOError as e:
        raise IOError(f"Error writing to the file {output_file_name}: {str(e)}")

def _rename_keys(individual_player_stats: dict, key_maps: dict):
    for key, value in key_maps.items():
        if key in individual_player_stats:
            individual_player_stats[value] = individual_player_stats.pop(key)
    # Remove keys with any uppercase letter
    keys_to_remove = [k for k in individual_player_stats if any(c.isupper() for c in k)]
    for k in keys_to_remove:
        del individual_player_stats[k]

def _fill_remaining_keys(individual_player_stats: dict, key_maps: dict):
    for key, value in key_maps.items():
        if "stats_status" in individual_player_stats:
            individual_player_stats.pop("stats_status")
            return
        if value not in individual_player_stats:
            individual_player_stats[value] = 0

def _map_match_Stats(match_stats: dict, individual_player_stats: dict, stat_map: dict):
    # print(f"Number of stats: {len(stat)} for {individual_player_stats['display_name']}")
    if not match_stats:
        individual_player_stats["stats_status"] = "NOT FOUND"

    for stat in match_stats:
        if str(stat["type_id"]) in stat_map:

            stat_key = stat_map[str(stat["type_id"])]
            
            stat_value = stat["data"]["value"]

            individual_player_stats[stat_key] = stat_value
        else:
            print(f"type_id: {stat['type_id']} not found in stat_map for {individual_player_stats['display_name']}")

def map_player_stats(player_stats: dict, stat_map: dict, key_maps: dict):
    individual_player_stats = {
        "player_id": player_stats.get("player_id", "NOT FOUND"),
        "team_id": player_stats.get("team_id", "NOT FOUND"),
        "fixture_id": player_stats.get("fixture_id", "NOT FOUND"),
        "api_player_id": player_stats.get("player_id", "NOT FOUND"),
        "api_team_id": player_stats.get("team_id", "NOT FOUND"),
        "api_fixture_id": player_stats.get("fixture_id", "NOT FOUND"),
        "display_name": player_stats.get("player_name", "NOT FOUND"),
        "position_id": player_stats.get("position_id", "NOT FOUND"),
    }
    _map_match_Stats(player_stats["details"], individual_player_stats, stat_map)
    _rename_keys(individual_player_stats, key_maps)
    _fill_remaining_keys(individual_player_stats, key_maps)

    FINAL_STATS.append(individual_player_stats)

if __name__ == "__main__":
    try:
        json_data = read_json_file(folder_name="input", file_name="sportmonks_response_fixture_id_19427531.json")
        stat_map = read_json_file(folder_name="docs", file_name="sportmonks_player_stats_map.json")
        key_maps = read_json_file(folder_name="docs", file_name="key_value_map.json")

        fetch_players_stats = json_data["data"]["lineups"]

        for player_stats in fetch_players_stats:
            map_player_stats(player_stats, stat_map, key_maps)

        write_json_to_file(FINAL_STATS, output_folder="output", output_file_name="player_stats_for_fixture_id_19427531_sportmonks.json")

    except (json.JSONDecodeError, Exception) as e:
        print(f"Error: {e}")
