import requests


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

if __name__ == '__main__':
    main()
