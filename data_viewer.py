import json

from WordleGuesser import feedback_parse

with open("game_data.json", "r") as f:
    _games = json.load(f)


games = []
for game in _games:
    _game = {
        "attempts": game["attempts"],
        "correct_word": game["correct_word"],
        "guesses": game["guesses"],
        "feedbacks": [feedback_parse(feedback) for feedback in game["feedbacks"]],
        "status": game["status"]
    }
    games.append(_game)



# stats
num = len(games)
success_rate = sum(1 for game in games if game["status"] == "SUCCESS") / num
first_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 1) / num
second_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 2) / num
third_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 3) / num
fourth_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 4) / num
fifth_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 5) / num
sixth_guess_success_rate = sum(1 for game in games if game["status"] == "SUCCESS" and game["attempts"] == 6) / num
avg_attempts = sum(game["attempts"] for game in games) / num

print(f"Played {num} games.")
print(f"Success rate: {success_rate:.2%}%")
print(f"Success rate by guess count:")
print(f"  1st guess: {first_guess_success_rate:.2%}%")
print(f"  2nd guess: {second_guess_success_rate:.2%}%")
print(f"  3rd guess: {third_guess_success_rate:.2%}%")
print(f"  4th guess: {fourth_guess_success_rate:.2%}%")
print(f"  5th guess: {fifth_guess_success_rate:.2%}%")
print(f"  6th guess: {sixth_guess_success_rate:.2%}%")
print(f"Average attempts: {avg_attempts:.2f}")
