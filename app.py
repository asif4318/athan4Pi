from playsound import playsound
import os
import requests
import time
import schedule

# Change to script directory to fix relative filepaths
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)


def fetchPrayerTime(city, state, country):
    '''Fetches prayer time based on a provided location  and returns response in JSON format'''

    parameters = {'city': city, 'state': state, 'country': country}
    url = 'http://api.aladhan.com/v1/timingsByCity/:date_or_timestamp'

    r = requests.get(
        url, params=parameters)

    return r.json()


def main():
    today_prayer_time = fetchPrayerTime('Gainesville', 'FL', 'USA')

    # Separate times out
    fajr_time = today_prayer_time['data']['timings']['Fajr']
    dhuhr_time = today_prayer_time['data']['timings']['Dhuhr']
    asr_time = today_prayer_time['data']['timings']['Asr']
    maghrib_time = today_prayer_time['data']['timings']['Maghrib']
    isha_time = today_prayer_time['data']['timings']['Isha']

    # Create job functions to run
    def fajr_job():
        print('Time for Fajr at: ' + fajr_time)
        return schedule.CancelJob

    def dhuhr_job():
        print('Time for Dhuhr at: ' + dhuhr_time)
        playsound('./athan.mp3')
        return schedule.CancelJob

    def asr_job():
        print('Time for Asr at: ' + asr_time)
        playsound('./athan.mp3')
        return schedule.CancelJob

    def maghrib_job():
        print('Time for Maghrib at: ' + maghrib_time)
        playsound('./athan.mp3')
        return schedule.CancelJob

    def isha_job():
        print('Time for Isha at: ' + isha_time)
        playsound('./athan.mp3')
        return schedule.CancelJob

    def update_prayer_time():
        nonlocal today_prayer_time
        today_prayer_time = fetchPrayerTime()

    # Daily scheduling of the 5 prayer notifications
    def set_prayer_times_today():
        update_prayer_time()

        # Schedule notifications for each of the 5 prayers
        schedule.every().day.at(fajr_time).do(fajr_job)
        schedule.every().day.at(dhuhr_job).do(dhuhr_job)
        schedule.every().day.at(asr_time).do(maghrib_job)
        schedule.every().day.at(maghrib_time).do(asr_job)
        schedule.every().day.at(isha_time).do(isha_job)

    # Schedule the daily function
    set_prayer_times_today()

    dhuhr_job()
    # Primary Job Loop
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
