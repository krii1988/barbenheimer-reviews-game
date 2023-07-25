# Barbenheimer Reviews

Barbenheimer Reviews is a Python script that allows users to play a fun guessing game based on movie reviews scraped from Metacritic. Users are presented with reviews from two different movies and have to guess which review belongs to which movie.

## Features

- Scrape movie details (film title, director, and cast) from Metacritic.
- Scrape user reviews from Metacritic for selected movies.
- Replace movie-related details (film title, director, and cast) in reviews with asterisks.
- Save cleaned reviews to CSV files, but only if the CSV files are older than 24 hours.
- Allow users to play the "Barbenheimer Reviews" game by guessing which review belongs to which movie.

## Setup

1. Install the required Python packages:

`pip install requests beautifulsoup4 langdetect simple-term-menu`

1. Run the `barbenheimer.py` script to play the "Barbenheimer Reviews" game.
2. You will be presented with 10 reviews from both movies (5 from each).
3. Use the arrow keys to select a movie and press Enter to make your choice.
4. The script will tell you if your guess was correct or not.
5. Continue playing and try to guess all the reviews correctly.
6. After playing all the reviews, the game will display your final score in gorgeous ASCII art.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The "Barbenheimer Reviews" project is inspired by the "Metacritic" website.
- Developed as a part of Python introductory course at the Riga Technical University.
- Special thanks to [OpenAI](https://openai.com) for the GPT-3.5-based language model used for chat interactions.
- GitHub Copilot for assisting with code suggestions during development.