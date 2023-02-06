# importing the library
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime, timedelta
import jsoncrud
import jsonpickle
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

helper_info = config_object["HELPER"]
profile_info = config_object["PROFILE"]


class Profile:
    def __init__(self, name, strdate, strtime):
        self.strdate = strdate
        self.strtime = strtime
        self.name = name


def get_videos():
    dirname = "videos"
    # giving file extension
    ext = ".mp4"
    # iterating over all files
    res = filter(lambda file: file.endswith(ext), os.listdir(dirname))
    return list(res)


def find(lst, key, value):
    if len(lst) == 0:
        return -1
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def compute_time(current_user):
    result = datetime.now()

    datearr = str(current_user.strdate).split("/")
    timearr = str(current_user.strtime).split(":")
    cur_date = [int(i) for i in datearr]
    cur_time = [int(i) for i in timearr]

    last_upload = datetime(
        cur_date[2], cur_date[1], cur_date[0], cur_time[0], cur_time[1]
    )

    duration = last_upload - datetime.now()
    hours = duration.total_seconds() / 3600

    print("duration_hours: ", hours)

    print("updated time: ", result)

    if hours >= float(helper_info["hr_to_update"]):
        result = last_upload + timedelta(
            hours=float(helper_info["space_between_video"])
        )
    print("updated time: ", result)

    return result


# update user before upload
def update_time(profile_name):
    today = datetime.now()
    # modifyname abit to match file format
    filename = str(profile_name).replace(" ", "_").lower()
    json_data = jsoncrud.readJSON(filename)
    current_user = jsonpickle.decode(json_data) if json_data else None

    # truong hop co user va da upload
    if current_user:
        # take last time and add 1 hr
        updatedtime = compute_time(current_user)
        current_user.strdate = updatedtime.strftime(r"%d/%m/%Y")
        current_user.strtime = updatedtime.strftime(r"%H:%M")
    else:
        current_user = Profile(
            profile_name, today.strftime(r"%d/%m/%Y"), today.strftime(r"%H:%M")
        )
    jsoncrud.writeJSON(jsonpickle.encode(current_user), filename=filename)

    return current_user


def wait_until_presence(driver, locator, value) -> WebElement:
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((locator, value))
    )
    if not element:
        return None
    return element


def wait_until_clickable_xpath(driver, locator, value) -> WebElement:
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((locator, value))
    )
    if not element:
        return None
    return element


def get_profiles():
    root = profile_info["profile_directory"]
    dirlist = [
        item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))
    ]
    # for root, dirs, files in os.walk(profile_info["profile_directory"], topdown=False):
    #     for name in dirs:
    #         directory_list.append(os.path.join(root, name))
    list_profile = list(filter(lambda item: str(item).startswith("Profile "), dirlist))
    print(list_profile)
    print("------- SELECT PROFILE ---------")
    res = int(input()) - 1
    print("res" + str(res))
    return list_profile[res]
