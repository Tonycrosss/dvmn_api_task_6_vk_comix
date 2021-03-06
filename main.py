import requests
import os
import random
from dotenv import load_dotenv


GROUP_ID = "179323429"


def download_image(url, name, extension="jpg"):
    response = requests.get(url)
    with open(f"./{name}.{extension}", "wb") as f:
        f.write(response.content)


def get_comix(comix_number):
    response = requests.get(f"https://xkcd.com/{comix_number}/info.0.json")
    comix = response.json()
    return comix


def get_comix_count():
    response = requests.get(f"https://xkcd.com/info.0.json").json()
    comix_count = response["num"]
    return comix_count


def get_groups(app_token):
    params = {
        "access_token": app_token,
        "v": "5.92",
    }
    url = f"https://api.vk.com/method/groups.get"
    response = requests.get(url, params=params)
    return response.json()


def get_wall_upload_server(app_token):
    params = {
        "access_token": app_token,
        "v": "5.92",
        "group_id": GROUP_ID
    }
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.post(url, params=params)
    print(response.json())
    upload_server = response.json()['response']['upload_url']
    return upload_server


def upload_image(upload_url, comix_number, app_token):
    with open(f'./{comix_number}.jpg', 'rb') as img:
        params = {'photo': img}
        url = upload_url
        response = requests.post(url, files=params).json()
        params = {
            "access_token": app_token,
            "v": "5.92",
            "group_id": GROUP_ID,
            "photo": response["photo"],
            "hash": response["hash"],
            "server": response["server"]
        }
        url = f"https://api.vk.com/method/photos.saveWallPhoto"
        response = requests.post(url, params=params)
    return response.json()


def post_photo(comix_comment, media_id, owner_id, app_token):
    photo_id = f"photo{owner_id}_{media_id}"
    params = {
        "access_token": app_token,
        "v": "5.92",
        "owner_id": f"-{GROUP_ID}",
        "message": comix_comment,
        "attachments": photo_id,
    }
    url = f"https://api.vk.com/method/wall.post"
    response = requests.post(url, params=params)
    return response.json()


def main():
    load_dotenv()
    app_token = os.getenv("APP_TOKEN")
    comix_count = int(get_comix_count())
    comix_random_number = str(random.randint(1, comix_count))
    comix = get_comix(comix_random_number)
    download_image(comix["img"], comix_random_number)
    comix_comment = comix["alt"]
    upload_server = get_wall_upload_server(app_token)
    uploaded_image = upload_image(upload_server, comix_random_number, app_token)
    media_id = uploaded_image["response"][0]["id"]
    owner_id = uploaded_image["response"][0]["owner_id"]
    post_photo(comix_comment, media_id, owner_id, app_token)


if __name__ == '__main__':
    main()
