import os
import random
import csv

from tools import metacritic, ascii_art

from simple_term_menu import TerminalMenu


def load_reviews_and_movies():
    data_folder = "data"
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    reviews = {}
    total_reviews = 0
    for csv_file in csv_files:
        movie_name = csv_file.replace("_reviews.csv", "")
        with open(os.path.join(data_folder, csv_file), "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            all_reviews = [row[0] for row in csv_reader]
            selected_reviews = random.sample(all_reviews, min(5, len(all_reviews)))
            reviews[movie_name] = selected_reviews
            total_reviews += len(selected_reviews)
    return reviews, total_reviews

def wrap_review(review):
    border = "=" * 60
    wrapped_review = f"\n{border}\n{review}\n{border}\n"
    return wrapped_review

def play_game(reviews, total_reviews):

    print(ascii_art.header)

    print("Match the review with the correct movie. 🤔")

    score = 0
    total_reviews_og = total_reviews

    while total_reviews > 0:
        movie_name, movie_reviews = random.choice(list(reviews.items()))

        if not movie_reviews:
            continue

        # print(f"\nMovie: {movie_name}")
        current_review = random.choice(movie_reviews)
        print(f"\nReview {total_reviews_og - total_reviews + 1} of {total_reviews_og}")


        print(wrap_review(current_review))

        del movie_reviews[movie_reviews.index(current_review)]
        total_reviews -= 1

        movie_menu = TerminalMenu(list(reviews.keys()), title="Available movies to choose from:", menu_cursor=">", menu_cursor_style=("fg_red", "bold"))
        selected_index = movie_menu.show()

        # If the user hasn't selected any movie (e.g., pressed 'Esc'), end the game
        if selected_index is None:
            break

        selected_movie_name = list(reviews.keys())[selected_index]

        if selected_movie_name == movie_name:
            print("✅ Correct! 🎉")
            score += 1
        else:
            print(f"❌ Wrong! The review is for '{movie_name}'. 😕")

    print(ascii_art.game_over)
    print(f"Your final score is:")
    print("\n")

    score_merged = ascii_art.merge_ascii_numbers(ascii_art.print_ascii_number(score), ascii_art.slash)
    total_merged = ascii_art.merge_ascii_numbers(ascii_art.print_ascii_number(int(str(total_reviews_og)[0])), ascii_art.print_ascii_number(int(str(total_reviews_og)[1])))

    print(ascii_art.merge_ascii_numbers(score_merged, total_merged))

if __name__ == "__main__":
    metacritic.generate_csv_files()
    reviews, total_reviews = load_reviews_and_movies()
    play_game(reviews, total_reviews)