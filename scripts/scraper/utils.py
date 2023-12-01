import requests
from pathlib import Path
from typing import Union


def download_image(image_url: str, headers: dict, file_path: Union[str, Path]):
    response = requests.get(image_url, headers=headers)
    with open(file_path, "wb") as file:
        file.write(response.content)
