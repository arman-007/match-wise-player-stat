import requests
import os

import os
from pathlib import Path
from dotenv import load_dotenv

# Define the base directory as the directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Go one directory up to find the .env file in the project root
dotenv_path = BASE_DIR.parent / '.env' 

load_dotenv(dotenv_path=dotenv_path)

# You can now access your variables
MY_VARIABLE = os.getenv("APIFOOTBALL_API_KEY")


def main():

    api_key = os.environ.get("APIFOOTBALL_API_KEY")
    print(MY_VARIABLE)
    # response = requests.get("https://apiv3.apifootball.com/?action=get_statistics&match_id=86392&APIkey=")
    # print(response.json())

if __name__ == "__main__":
    main()