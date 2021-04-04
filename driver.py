import speedtest  
import drivers
from time import sleep, time, asctime, localtime
import requests

ALWAYS_ON = False
FREQUENCY = 1200
BACKLIGHT_TIME = 30 # Used when ALWAYS ON is True

display = ''

def check_internet():
    try:
        requests.get('https://www.google.com/').status_code
        return True
    except:
        return False

def speed_test():
    st = speedtest.Speedtest()
    st.get_servers()
    st.get_best_server()
    st.download()
    st.upload()
    results = st.results.dict()
    return results

def display_speed(download_speed, upload_speed, ping, ISP):
    display.lcd_backlight(1)
    display.lcd_display_string(f'D:{download_speed} U:{upload_speed}', 1)
    display.lcd_display_string(f'P:{ping} S:{ISP}', 2)

def display_no_internet():
    display.lcd_backlight(1)
    display.lcd_display_string('No Internet!', 1)

def start():
    while True:

        print(asctime(localtime(time())), end = ' - ')

        if check_internet():
            results = speed_test()

            download_speed = round(results['download']/(1024*1024),2)
            upload_speed = round(results['upload']/(1024*1024),2)
            ping = round(results['ping'], 1)
            ISP = results['client']['isp']

            print(f'D:{download_speed} U:{upload_speed} P:{ping} S:{ISP}')

            display_speed(download_speed, upload_speed, ping, ISP)

        else:
            print('No Internet!')
            display_no_internet()

        if ALWAYS_ON==False:
            sleep(BACKLIGHT_TIME)
            display.lcd_backlight(0)
        sleep(FREQUENCY)

def print_header():
    print()
    print('-----------------------------------------------------')
    print('                  SpeedTest LCD')
    print('-----------------------------------------------------')
    print()

def main():
    print_header()
    global display
    display = drivers.Lcd()
    if ALWAYS_ON==False:
        display.lcd_backlight(0)
    try:
        start()
    except Exception as e:
        print('Error:', str(e))
    finally:
        display.lcd_clear()
        display.lcd_backlight(0)


if __name__ == "__main__":
    main()
