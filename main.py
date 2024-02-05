import requests
from bs4 import BeautifulSoup

#初始化
games = []

def find_in_matrix(text):
    for i in range(len(games)):
        if games[i][0] == text:
            return i
def load_data(start_page=1,pages=10):
    with open("data.csv","w",encoding="utf-8") as f:
        for page_num in range(start_page,pages+1):
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
                    games.append([game_name,game_current_players,game_peak_players,game_hours_played])
            print(f"Successfully saved the Page{page_num}")
    print("All done!")
    return

try:
    with open("data.csv","r",encoding="utf-8") as f:
        if(f.readline() == ""):
            raise FileNotFoundError
        f.seek(0)
        for line in f:
            games.append(line.strip().split(","))
except FileNotFoundError:# 第一次运行
    print("[LOG] First time to run this program. Start crawling...\n")
    load_data()

while True:
    game_name = input("Please enter the game name: ")
    if game_name == "Debug" or game_name == "debug":# 手动调整、测试bug用，不会在正式版中出现
        extension = int(input("请输入要拓展的页数，可以获得更多数据:")) 
        load_data(11,10+extension)  
        break
    # 输入修正
    game_name = game_name.title()
    if game_name == "quit":
        break
    else:
        i = 0
        try:
            i = find_in_matrix(game_name) 
            print(f"Current players: {games[i][1]}\nPeak players: {games[i][2]}\nHours played: {games[i][3]}")
        except TypeError:
            print("未找到游戏,请检查输入是否正确。或使用Debug模式拓展数据。")