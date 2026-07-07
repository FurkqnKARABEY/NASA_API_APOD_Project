import datetime
import io
import os
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import requests
from dotenv import load_dotenv
from PIL import Image


APOD_URL = "https://api.nasa.gov/planetary/apod"


def get_date_range(days: int = 7) -> tuple[str, str]:
    """Return start and end dates for the APOD API request."""
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    return start_date.isoformat(), today.isoformat()


def get_api_key() -> str:
    """Read the NASA API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")

    if not api_key:
        raise RuntimeError(
            "NASA_API_KEY is missing. Create a .env file from .env.example "
            "and add your NASA API key."
        )

    return api_key


def fetch_apod_data(api_key: str, days: int = 7) -> list[dict[str, Any]]:
    """Fetch APOD data from NASA for the given date range."""
    start_date, end_date = get_date_range(days)

    params = {
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
    }

    response = requests.get(APOD_URL, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return [data]

    raise ValueError("Unexpected APOD API response format.")


def filter_image_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return APOD entries that contain image URLs."""
    image_entries: list[dict[str, Any]] = []

    for entry in entries:
        url = entry.get("url", "")
        media_type = entry.get("media_type", "")

        if media_type == "image" and url.lower().endswith((".jpg", ".jpeg", ".png")):
            image_entries.append(entry)

    return image_entries


def print_entry_summary(entry: dict[str, Any]) -> None:
    """Print basic information about an APOD entry."""
    print(f"Date: {entry.get('date', 'Unknown')}")
    print(f"Title: {entry.get('title', 'Untitled')}")
    print(f"Explanation: {entry.get('explanation', 'No explanation available.')}")
    print(f"Image URL: {entry.get('url', 'No URL')}\n")


def display_image(image_url: str, title: str) -> None:
    """Download and display an image from a remote URL."""
    response = requests.get(image_url, timeout=20)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "image" not in content_type:
        raise ValueError(f"URL did not return an image. Content-Type: {content_type}")

    image = Image.open(io.BytesIO(response.content))
    image_array = np.array(image)

    plt.figure(figsize=(10, 6))
    plt.imshow(image_array)
    plt.axis("off")
    plt.title(title, fontsize=14)
    plt.show()


def main() -> None:
    api_key = get_api_key()
    entries = fetch_apod_data(api_key, days=7)
    image_entries = filter_image_entries(entries)

    if not image_entries:
        print("No image-based APOD entries were found in the selected date range.")
        return

    for entry in image_entries:
        print_entry_summary(entry)

    first_image = image_entries[0]
    display_image(
        image_url=first_image["url"],
        title=f"NASA APOD - {first_image.get('title', 'Image')}",
    )


if __name__ == "__main__":
    main()
