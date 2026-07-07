# NASA APOD API Project

A small Python project that fetches recent Astronomy Picture of the Day (APOD) data from NASA's public API and displays the first available image with its metadata.

## Project Purpose

This project demonstrates basic API consumption, JSON response handling, image downloading, and simple data visualization in Python.

It is useful for practicing:

- Working with external REST APIs
- Managing API keys securely with environment variables
- Parsing JSON responses
- Filtering image-based APOD results
- Downloading and displaying remote images
- Basic visualization with Matplotlib

## Features

- Fetches APOD records for the last 7 days
- Prints APOD date, title, explanation, and image URL
- Filters results to image files (`.jpg`, `.png`)
- Downloads the first available image result
- Displays the image using Matplotlib
- Keeps the NASA API key outside the source code

## Tech Stack

- Python
- NASA APOD API
- Requests
- Matplotlib
- NumPy
- Pillow
- python-dotenv

## Project Structure

```text
NASA_API_APOD_Project/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/FurkqnKARABEY/NASA_API_APOD_Project.git
cd NASA_API_APOD_Project
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local `.env` file:

```bash
cp .env.example .env
```

Then add your NASA API key:

```env
NASA_API_KEY=your_nasa_api_key_here
```

You can get a NASA API key from NASA's official API portal.

## Run

```bash
python app.py
```

## Security Note

Do not commit real API keys, tokens, passwords, or `.env` files to GitHub. Keep secrets in environment variables or local configuration files ignored by Git.

## Author

**Furkan Karabey**
