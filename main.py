from . import config, scraper
import time

def main():
    ulleung_config = config.UlleungConfig()
    dokdo_config = config.DokdoConfig()

    ulleung_scraper = scraper.TicketChecker()
    dokdo_scraper = scraper.TicketChecker()

    ulleung_scraper.set_attrs(
        ulleung_config.request_url,
        ulleung_config.request_headers,
        ulleung_config.request_data,
        ulleung_config.reservation_url
    )
    dokdo_scraper.set_attrs(
        dokdo_config.request_url,
        dokdo_config.request_headers,
        dokdo_config.request_data,
        dokdo_config.reservation_url
    )

    ulleung_response_bs = ulleung_scraper.get_data()
    dokdo_response_bs = dokdo_scraper.get_data()

    ulleung_parsed = ulleung_scraper.parse_data(ulleung_response_bs)
    dokdo_parsed = dokdo_scraper.parse_data(dokdo_response_bs)

    ulleung_scraper.check_empty_seat(ulleung_parsed)
    dokdo_scraper.check_empty_seat(dokdo_parsed)
    

if __name__ == "__main__":
    count = 0
    sleep = config.BaseCofig.check_interval
    while 1:
        main()
        print(f"Check count: {count}. Sleep for {sleep} seconds")
        time.sleep(sleep)

