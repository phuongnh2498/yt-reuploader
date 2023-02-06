import time
import helper
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from configparser import ConfigParser


# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

profile_info = config_object["PROFILE"]

PROFILE = helper.get_profiles()

print("you choose " + PROFILE)

chrome_options = Options()
# e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
)
chrome_options.add_argument("--disable-disable-extensions")
chrome_options.add_argument(
    "user-data-dir={}".format(profile_info["profile_directory"])
)
chrome_options.add_argument("--profile-directory={}".format(PROFILE))
chrome_options.binary_location = (
    "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
)


def upload_to_youtube(file_name):
    bot = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    print(bot.title)
    if not bot.current_url.startswith("https://studio.youtube.com"):
        bot.get("https://studio.youtube.com")

    # start loop click
    upload_button = helper.wait_until_clickable_xpath(
        bot, By.CSS_SELECTOR, "#upload-icon"
    )
    # remove youtube tutorial shit
    upload_button.click()

    file_input = helper.wait_until_presence(bot, By.XPATH, '//*[@id="content"]/input')
    simp_path = "videos/{}".format(file_name)
    abs_path = os.path.abspath(simp_path)

    file_input.send_keys(abs_path)
    time.sleep(7)

    # kid button
    radio_button = helper.wait_until_clickable_xpath(
        bot,
        By.CSS_SELECTOR,
        "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'] #radioLabel",
    )

    radio_button.click()

    next_button = helper.wait_until_clickable_xpath(
        bot, By.XPATH, '//*[@id="next-button"]'
    )
    for i in range(3):
        next_button.click()
        time.sleep(1)

    # update user before upload
    helper_user = helper.update_time(PROFILE)

    # set schedule
    schedule_button = helper.wait_until_clickable_xpath(
        bot, By.XPATH, '//*[@id="schedule-radio-button"]'
    )
    schedule_button.click()

    # outer
    schedule_time = bot.find_element(By.CSS_SELECTOR, "#input-1 > input")
    schedule_time.clear()
    schedule_time.send_keys(helper_user.strtime)
    schedule_time.send_keys(Keys.RETURN)

    schedule_date = bot.find_element(
        By.CSS_SELECTOR, "#datepicker-trigger > ytcp-dropdown-trigger > div"
    )
    schedule_date.click()

    schedule_date = helper.wait_until_presence(
        bot, By.CSS_SELECTOR, "ytcp-date-picker input"
    )
    schedule_date.clear()
    schedule_date.send_keys(helper_user.strdate)
    schedule_date.send_keys(Keys.RETURN)

    done_button = helper.wait_until_clickable_xpath(
        bot, By.XPATH, '//*[@id="done-button"]'
    )
    done_button.click()

    time.sleep(5)
    bot.quit()
    print("Done 1 Video")


print(
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc.."
)
answer = input(
    "\033[1;32;40m Press 1 if you want to spam same video or Press 2 if you want to upload multiple videos: "
)

if int(answer) == 1:
    nameofvid = input(
        "\033[1;33;40m Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> "
    )
    howmany = input("\033[1;33;40m How many times you want to upload this video ---> ")
    for i in range(int(howmany)):
        upload_to_youtube(nameofvid)

elif int(answer) == 2:
    print(
        "\033[1;31;40m IMPORTANT: Please make sure the name of the videos are like this: vid1.mp4, vid2.mp4, vid3.mp4 ...  etc"
    )
    videos = helper.get_videos()
    for video in videos:
        upload_to_youtube(video)
