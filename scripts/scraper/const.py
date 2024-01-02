from pathlib import Path

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    )
}

timeout_time = 10

config = {
    "base_url": "https://www.transfermarkt.com",
    "players_url": "/spieler-statistik/wertvollstespieler/marktwertetop",
    "clubs": [
        "https://www.transfermarkt.com/inter-mailand/startseite/verein/46",
        "https://www.transfermarkt.com/al-nasr-riad/startseite/verein/18544",
        "https://www.transfermarkt.com/real-madrid/startseite/verein/418/from/newsansicht",
    ],
}

photos_dir = Path("photos")

months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}
