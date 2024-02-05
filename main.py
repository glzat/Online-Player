import requests
from bs4 import BeautifulSoup

with open("steamcharts.csv","w",encoding="utf-8") as f:
    for page_num in range(1,11):
        url = f"https://steamcharts.com/top/p.{page_num}"
        while True:
            try:
                response = requests.get(url)
            except requests.exceptions.ConnectionError:
                print("[Error] 403. Forbidden")
            else:
                break
        soup = BeautifulSoup(response.text, "html.parser")
        games_info = soup.find("table",id="top-games")
        games_info_body = games_info.find("tbody")
        games_td = games_info_body.find_all("tr")
        for i in range(len(games_td)):    
            try:
                game_name = games_td[i].find("td",attrs={"class":"game-name left"}).text.strip()       
                game_current_players = games_td[i].find("td",attrs={"class":"num"}).text
                game_peak_players = games_td[i].find("td",attrs={"class":"num period-col peak-concurrent"}).text
                game_hours_played = games_td[i].find("td",attrs={"class":"num period-col player-hours"}).text
            except AttributeError:
                print("[Error] 未爬取到信息.Retrying...")
                continue
            else:
                f.write(f"{game_name},{game_current_players},{game_peak_players},{game_hours_played}\n")
        print(f"Successfully saved the Page{page_num}")
print("All done!")
    