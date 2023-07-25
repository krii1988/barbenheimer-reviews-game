import os
import re
import requests
import datetime
from bs4 import BeautifulSoup
from langdetect import detect
import csv

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def replace_names_with_asterisks(text, names):
    # Create a regex pattern to match any name in the list (case-insensitive)
    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(name) for name in names) + r')\b', re.IGNORECASE)
    # Replace the matched names with "*"
    return pattern.sub('***', text)

def split_name(name):
    parts = name.split(" ")
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first_name, last_name

def scrape_movie_details(movie_url):
    response = requests.get(movie_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract film title
        film_wrap = soup.find("div", class_="product_page_title")
        film_title = film_wrap.find("h1").text.strip()
        
        # Extract director name
        director_tag = soup.find("div", class_="director")
        director = director_tag.find("a").text.strip() if director_tag else None
        director_first_name, director_last_name = split_name(director)

        # Extract cast names
        cast_wrap = soup.find("div", class_="summary_cast")
        cast_tags = cast_wrap.find_all("a")
        cast = [cast_tag.text.strip() for cast_tag in cast_tags]
        cast = [cast_tag.text.strip() for cast_tag in cast_tags]
        cast_first_names, cast_last_names = zip(*[split_name(actor) for actor in cast])

        return film_title, (director_first_name, director_last_name), (list(cast_first_names), list(cast_last_names))
    else:
        return None, None, None

def scrape_metacritic_movie_reviews(movie_url, num_pages=1):
    film_title, director, cast = scrape_movie_details(movie_url)
    if film_title and director and cast:
        print(f"⏱️ Scraping user reviews for {film_title}")

        user_reviews = []

        for page in range(0, num_pages):
            page_url = f"{movie_url}/user-reviews?page={page}"
            response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                reviews = soup.find_all("div", class_="review_body")

                for review in reviews:
                    review_text = review.find("span", class_="blurb blurb_expanded")
                    if review_text and is_english(review_text.text.strip()):
                        cleaned_review = replace_names_with_asterisks(review_text.text.strip(), [film_title, director[0], director[1]] + cast[0] + cast[1])
                        user_reviews.append(cleaned_review)

        return film_title, user_reviews

    else:
        print("😭 Failed to scrape movie details.")
        return []
    


def generate_csv_files():
    # Replace these URLs with the Metacritic movie pages you want to scrape
    movie_urls = [
        "https://www.metacritic.com/movie/oppenheimer",
        "https://www.metacritic.com/movie/barbie"
    ]

    # Set the number of pages to scrape. Each page typically contains 100 user reviews.
    num_pages_to_scrape = 5

        # Create a data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    for movie_url in movie_urls:
        film_title, reviews = scrape_metacritic_movie_reviews(movie_url, num_pages=num_pages_to_scrape)
        if reviews:
            # ... (same as before)
            csv_filename = os.path.join("data", f"{film_title}_reviews.csv")

            # Check if the CSV file already exists and its modification time
            if os.path.exists(csv_filename):
                last_modified_time = os.path.getmtime(csv_filename)
                current_time = datetime.datetime.now().timestamp()
                time_difference = current_time - last_modified_time
                one_day_in_seconds = 24 * 60 * 60

                if time_difference < one_day_in_seconds:
                    print(f"👌 {csv_filename} is up to date. Skipping CSV generation.")
                    continue

            with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Review"])
                for review in reviews:
                    cleaned_review = replace_names_with_asterisks(review, [film_title])
                    csv_writer.writerow([cleaned_review])
            print(f"💾 Reviews for '{film_title}' saved to '{csv_filename}'.")
        else:
            print(f"😭 No user reviews found for '{film_title}'.")