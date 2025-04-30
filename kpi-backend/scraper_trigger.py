import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_scrapers():
    subprocess.run(["python3", os.path.join(BASE_DIR, "./data/tiktok_scraping.py")])
    subprocess.run(["python3", os.path.join(BASE_DIR, "./data/ig_scraping.py")])
    subprocess.run(["python3", os.path.join(BASE_DIR, "./data/x_scraping.py")])

if __name__ == "__main__":
    run_scrapers()