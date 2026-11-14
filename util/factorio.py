import factorio_rcon
import os
import re

RCON_TIMEOUT_SEC: float = 5.0


def create_client(bot) -> factorio_rcon.RCONClient:
    """
    RCONクライアントを生成する（この時点では接続しない）。
    接続は呼び出し側で client.connect() を実行すること。
    """
    IP = bot.config["factorio"]["rcon_ip"]
    PORT = bot.config["factorio"]["rcon_port"]
    PASSWORD = os.getenv("FACTORIO_RCON_PASSWORD","")
    client = factorio_rcon.RCONClient(
        IP, PORT, PASSWORD, timeout=RCON_TIMEOUT_SEC, connect_on_init=False
    )
    return client

def version(client:factorio_rcon.RCONClient) -> str:
    """
    Factorioのゲームバージョンを取得
    """
    response:str = str(client.send_command("/version"))
    return response


def seed(client:factorio_rcon.RCONClient) -> str:
    """
    起動中のゲームのシード値を取得
    """
    response:str = str(client.send_command("/seed"))
    return response


def time(client:factorio_rcon.RCONClient) -> str:
    """
    起動中のゲーム内時間を取得
    """
    response:str = str(client.send_command("/time"))
    return response


def player_count(client:factorio_rcon.RCONClient) -> int:
    """
    ゲームに1度でも参加したプレイヤー数を取得
    """
    response:str = str(client.send_command("/players count"))
    pattern:str = '(?<=\\().+?(?=\\))'
    player_count:int = int(re.findall(pattern, response.splitlines()[0])[0])
    return player_count


def player_list(client:factorio_rcon.RCONClient) -> list:
    """
    ゲームに1度でも参加したプレイヤーリストを取得
    """
    response:str = str(client.send_command("/players"))
    pattern:str = '(?<=\\().+?(?=\\))'
    player_count:int = int(re.findall(pattern, response.splitlines()[0])[0])

    player_list = []
    if player_count>=1:
        for i,text in enumerate(response.splitlines()):
            if i==0:
                # 「プレイヤー (x):」の行は不要なのでスキップ
                continue
            player_list.append(text.strip().split()[0])
    return player_list


def online_player_count(client:factorio_rcon.RCONClient) -> int:
    """
    現在オンラインのプレイヤー数を取得
    """
    response:str = str(client.send_command("/players online count"))
    pattern:str = '(?<=\\().+?(?=\\))'
    player_count:int = int(re.findall(pattern, response.splitlines()[0])[0])
    return player_count


def online_player_list(client:factorio_rcon.RCONClient) -> list:
    """
    現在オンラインのプレイヤーリストを取得
    """
    response:str = str(client.send_command("/players online"))
    pattern:str = '(?<=\\().+?(?=\\))'
    player_count:int = int(re.findall(pattern, response.splitlines()[0])[0])
    player_list = []
    if player_count>=1:
        for i,text in enumerate(response.splitlines()):
            if i==0:
                # 「オンラインのプレイヤー (x):」の行は不要なのでスキップ
                continue
            # ユーザ名の後ろに「 (onilne)」がつくため、取り除いて設定
            player_list.append(text.strip().split()[0])
    return player_list

def evolution(client:factorio_rcon.RCONClient) -> str:
    """
    エイリアンの進化ファクター情報を取得
    """
    response:str = str(client.send_command("/evolution"))
    return response

def send_message(client:factorio_rcon.RCONClient):
    response:str = str(client.send_command("/s message_test"))
    return response
