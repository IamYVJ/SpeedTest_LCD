import speedtest  
import drivers
from time import sleep

display = ''

def speed_test():
    st = speedtest.Speedtest()
    st.get_servers()
    st.get_best_server()
    st.download()
    st.upload()
    results = st.results.dict()
    return results

def display_speed(results):
    download_speed = round(results['download']/(1024*1024),2)
    upload_speed = round(results['upload']/(1024*1024),2)
    ping = round(results['ping'], 1)
    ISP = results['client']['isp']

    display.lcd_backlight(1)
    display.lcd_display_string(f'D:{download_speed} U:{upload_speed}', 1)
    display.lcd_display_string(f'P:{ping} S:{ISP}', 2)
    sleep(30)
    # display.lcd_clear()
    display.lcd_backlight(0)

def start():
    while True:
        results = speed_test()
        display_speed(results)
        sleep(1200)

def main():
    global display
    display = drivers.Lcd()
    display.lcd_backlight(0)
    try:
        start()
    except Exception as e:
        pass
    finally:
        display.lcd_clear()
        display.lcd_backlight(0)


if __name__ == "__main__":
    main()
