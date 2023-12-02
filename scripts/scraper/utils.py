import requests
from pathlib import Path
from typing import Union


def download_image(image_url: str, headers: dict, file_path: Union[str, Path]):
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        response = requests.get(image_url, headers=headers)
        with open(file_path, "wb") as file:
            file.write(response.content)
