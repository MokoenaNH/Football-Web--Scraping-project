# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 23:08:51 2024

@author: NeoMokoena600
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Function to get the team results
def get_team_results(url, selected_team):
    # Initialize the Selenium WebDriver
    driver = webdriver.Chrome()  # Use your specific path if necessary
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)  # Adjust this time if necessary

    # Get the page source after JavaScript has executed
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize variables to store total goals scored and conceded
    total_goals_scored = 0
    total_goals_conceded = 0

    # Find all match links
    matches = soup.find_all('a', class_='match_link__42JvI')  # Update with the correct class used for match links

    if matches:
        for i, match in enumerate(matches, start=1):
            print(f"\nProcessing match {i}:")
            team_divs = match.find_all('div')
            
            # Check if there are enough divs to proceed
            if len(team_divs) >= 3:
                team1 = team_divs[0].text.strip()  # First team name
                score_span = team_divs[1].find('span', {'aria-label': 'Score'})

                # Check if score span exists and retrieve score
                if score_span:
                    try:
                        score_text = score_span.get_text(strip=True)
                        scored, conceded = map(int, score_text.split(' : '))
                        team2 = team_divs[2].text.strip()  # Second team name
                        print(f"Match: {team1} vs {team2} | Score: {scored} : {conceded}")

                        # Check if the selected team is in team1 or team2 and update totals accordingly
                        if selected_team.lower() in team1.lower():
                            total_goals_scored += scored
                            total_goals_conceded += conceded
                        elif selected_team.lower() in team2.lower():
                            total_goals_scored += conceded
                            total_goals_conceded += scored
                    except ValueError:
                        print("Could not split or parse the score text:", score_text)
                else:
                    print(f"No score span found for match between {team1} and {team2}.")
            else:
                print("Unexpected structure: Not enough div elements found in match div.")

        print(f"\nTotal Goals Scored by {selected_team}: {total_goals_scored}")
        print(f"Total Goals Conceded by {selected_team}: {total_goals_conceded}")
    else:
        print("No match data found.")

    # Close the WebDriver
    driver.quit()

# List of teams and their corresponding result URLs
team_links = {
    "Arsenal": "https://www.goal.com/en-za/team/arsenal/fixtures-results/4dsgumo7d4zupm2ugsvm4zm4d",
    "Manchester City": "https://www.goal.com/en-za/team/manchester-city/fixtures-results/a3nyxabgsqlnqfkeg41m6tnpp",
    "Liverpool": "https://www.goal.com/en-za/team/liverpool/fixtures-results/c8h9bw1l82s06h77xxrelzhur",
    "Manchester United": "https://www.goal.com/en-za/team/manchester-united/fixtures-results/6eqit8ye8aomdsrrq0hk3v7gh",
    "Newcastle": "https://www.goal.com/en-za/team/newcastle/fixtures-results/7vn2i2kd35zuetw6b38gw9jsz",
    "Chelsea": "https://www.goal.com/en-za/team/chelsea/fixtures-results/9q0arba2kbnywth8bkxlhgmdr",
    "Tottenham": "https://www.goal.com/en-za/team/tottenham/fixtures-results/22doj4sgsocqpxw45h607udje",
    "West Ham": "https://www.goal.com/en-za/team/west-ham/fixtures-results/4txjdaqveermfryvbfrr4taf7",
    "Brentford": "https://www.goal.com/en-za/team/brentford/fixtures-results/7yx5dqhhphyvfisohikodajhv",
    "Brighton": "https://www.goal.com/en-za/team/brighton/fixtures-results/e5p0ehyguld7egzhiedpdnc3w",
    "Fulham": "https://www.goal.com/en-za/team/fulham/fixtures-results/hzqh7z0mdl3v7gwete66syxp",
    "Bournemouth": "https://www.goal.com/en-za/team/bournemouth/fixtures-results/1pse9ta7a45pi2w2grjim70ge",
    "Nottingham Forest": "https://www.goal.com/en-za/team/nottingham-forest/fixtures-results/1qtaiy11gswx327s0vkibf70n",
    "Aston Villa": "https://www.goal.com/en-za/team/aston-villa/fixtures-results/b496gs285it6bheuikox6z9mj",
    "Leicester": "https://www.goal.com/en-za/team/leicester/fixtures-results/avxknfz4f6ob0rv9dbnxdzde0",
    "Everton": "https://www.goal.com/en-za/team/everton/fixtures-results/ehd2iemqmschhj2ec0vayztzz",
    "Crystal Palace": "https://www.goal.com/en-za/team/crystal-palace/fixtures-results/1c8m2ko0wxq1asfkuykurdr0y",
    "Ipswich": "https://www.goal.com/en-za/team/ipswich/fixtures-results/8b523ujgl21tbc01me65q0aoh",
    "Wolverhampton": "https://www.goal.com/en-za/team/wolverhampton/fixtures-results/b9si1jn1lfxfund69e9ogcu2n",
    "Southampton": "https://www.goal.com/en-za/team/southampton/fixtures-results/d5ydtvt96bv7fq04yqm2w2632",
    # Add more teams and URLs here as needed
}

# Display the list of teams and ask the user to select two
print("Please select two teams from the list below:")
for index, team in enumerate(team_links.keys(), start=1):
    print(f"{index}. {team}")

# Get user input for the first team selection
team_choice_1 = int(input("Enter the number corresponding to your first team: ")) - 1  # Convert to index
team_names = list(team_links.keys())
if 0 <= team_choice_1 < len(team_names):
    selected_team_1 = team_names[team_choice_1]
    url_input_1 = team_links[selected_team_1]
else:
    print("Invalid selection. Exiting the program.")
    exit()

# Get user input for the second team selection
team_choice_2 = int(input("Enter the number corresponding to your second team: ")) - 1  # Convert to index
if 0 <= team_choice_2 < len(team_names):
    selected_team_2 = team_names[team_choice_2]
    url_input_2 = team_links[selected_team_2]
else:
    print("Invalid selection. Exiting the program.")
    exit()

# Get results for both selected teams
print(f"\nResults for {selected_team_1}:")
get_team_results(url_input_1, selected_team_1)

print(f"\nResults for {selected_team_2}:")
get_team_results(url_input_2, selected_team_2)
