import config, scraper, notifier
import time

def main(send_log=False):
    ulleung_config = config.UlleungConfig()
    dokdo_config = config.DokdoConfig()

    ulleung_scraper = scraper.TicketChecker("ulleung_scraper")
    dokdo_scraper = scraper.TicketChecker("dokdo_scraper")

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

    if send_log:
        ulleung_scraper.send_messages(ulleung_parsed)
        dokdo_scraper.send_messages(dokdo_parsed)
    

if __name__ == "__main__":
    base_config = config.BaseCofig()
    
    count = 0
    sleep = base_config.check_interval
    log_count = base_config.log_interval
    send_log = False
    while 1:
        if count != 0 and count % log_count == 0:
            send_log = True
        
        main(send_log=send_log)
        print(f"Check count: {count}. Sleep for {sleep} seconds")
        
        send_log = False
        count += 1
        time.sleep(sleep)

