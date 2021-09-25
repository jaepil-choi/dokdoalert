HUPO2ULLEUNG_DATE = "2021-10-08"
DOKDO_DATE = "2021-10-09"
ULLEUNG2HUPO_DATE = "2021-10-10"

HUPO_ID = 43030
ULLEUNG_ID = 43110
DOKDO_ID = 96330
class BaseCofig:
    def __init__(self) -> None:
        self.request_url = "https://www.jhferry.com/booking/get_Departure.php"
        self.request_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,ja;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "54",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Cookie": "PHPSESSID=qnspecd4ul4r37k1pdi87gsaa3; _ga=GA1.2.1695114459.1632547800; _gid=GA1.2.317497070.1632547800; _gat_gtag_UA_20106939_1=1",
            "Host": "www.jhferry.com",
            "Origin": "https://www.jhferry.com",
            "Referer": "https://www.jhferry.com/booking/booking.html",
            # "sec-ch-ua": ""Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"",
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": ""Windows"",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            }
        self.check_interval = 300 # seconds
        self.log_interval = 12 * 6 # counts
        # self.check_interval = 10 # seconds
        # self.log_interval = 10 # counts
        self.reservation_url = "https://www.jhferry.com/booking/booking.html"

class UlleungConfig(BaseCofig):
    def __init__(self, port_from, port_to, departure) -> None:
        super().__init__()
        self.request_data = { # Hupo to Ulleung
            # "idx": 1,
            "fportid": port_from, # Port Hupo
            "tportid": port_to, # Port Ulleung
            "departure": departure,
            }

class DokdoConfig(BaseCofig):
    def __init__(self, port_from, port_to, departure) -> None:
        super().__init__()
        self.request_data = { # Ulleung to Dokdo
            # "idx": 1,
            "fportid": port_from, # Port Ulleng
            "tportid": port_to, # Port Dokdo
            "departure": departure,
            }
        



