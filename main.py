import requests
import os
import random
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
APP_TOKEN = os.getenv("APP_TOKEN")
GROUP_ID = "179323429"


def download_image(url, name, extension="jpg"):
    response = requests.get(url)
    with open(f"./{name}.{extension}", "wb") as f:
        f.write(response.content)


def get_comix_json(comix_number):
    response = requests.get(f"https://xkcd.com/{comix_number}/info.0.json")
    comix_json = response.json()
    return comix_json


def get_groups_json():
    params = {
        "access_token": APP_TOKEN,
        "v": "5.92",
    }
    url = f"https://api.vk.com/method/groups.get"
    response = requests.get(url, params=params)
    return response.json()


def get_wall_upload_server_json():
    params = {
        "access_token": APP_TOKEN,
        "v": "5.92",
        "group_id": GROUP_ID
    }
    url = f"https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.post(url, params=params)
    return response.json()


def upload_image_resp_json(upload_url, comix_number):
    with open(f'./{comix_number}.jpg', 'rb') as img:
        params = {'photo': img}
        url = upload_url
        response = requests.post(url, files=params).json()
        params = {
            "access_token": APP_TOKEN,
            "v": "5.92",
            "group_id": GROUP_ID,
            "photo": response["photo"],
            "hash": response["hash"],
            "server": response["server"]
        }
        url = f"https://api.vk.com/method/photos.saveWallPhoto"
        response = requests.post(url, params=params)
    return response.json()


def post_photo(comix_comment, media_id, owner_id):
    photo_id = f"photo{owner_id}_{media_id}"
    params = {
        "access_token": APP_TOKEN,
        "v": "5.92",
        "owner_id": f"-{GROUP_ID}",
        "message": comix_comment,
        "attachments": photo_id,
    }
    url = f"https://api.vk.com/method/wall.post"
    response = requests.post(url, params=params)
    return response.json()


def main():
    comix_number = str(random.randint(1, 1000))
    comix_json = get_comix_json(comix_number)
    download_image(comix_json["img"], comix_number)
    comix_comment = comix_json["alt"]
    upload_server_json = get_wall_upload_server_json()
    upload_server = upload_server_json['response']['upload_url']
    uploaded_image_resp_json = upload_image_resp_json(upload_server, comix_number)
    media_id = uploaded_image_resp_json["response"][0]["id"]
    owner_id = uploaded_image_resp_json["response"][0]["owner_id"]
    post_photo(comix_comment, media_id, owner_id)


if __name__ == '__main__':
    main()
