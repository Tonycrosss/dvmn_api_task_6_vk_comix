import requests
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
APP_TOKEN = os.getenv("APP_TOKEN")
print(APP_TOKEN)


def download_image(url, name, extension="jpg"):
    response = requests.get(url)
    with open(f"./{name}.{extension}", "wb") as f:
        f.write(response.content)


def get_comix_json(comix_number):
    response = requests.get(f"https://xkcd.com/{comix_number}/info.0.json")
    comix_json = response.json()
    print(comix_json)
    return comix_json


def main():
    comix_number = "614"
    # download_image("https://imgs.xkcd.com/comics/python.png")
    comix_json = get_comix_json(comix_number)
    download_image(comix_json["img"], comix_number)
    comix_comment = comix_json["alt"]
    print(comix_comment)
    groups_json = get_groups_json()
    print(groups_json)


def get_groups_json():
    params = {
        "access_token": APP_TOKEN,
        "v": "5.92",
    }
    # url = f"https://api.vk.com/method/groups.get?access_token={APP_TOKEN}&v=5.92"
    url = f"https://api.vk.com/method/groups.get"
    response = requests.get(url, params=params)
    return response.json()


if __name__ == '__main__':
    main()
