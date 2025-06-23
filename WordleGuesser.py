import random
from wordle import Wordle
from string import ascii_lowercase

WORDS = []
with open('words.txt', 'r') as file:
    for line in file:
        word = line.strip()
        if len(word) == 5 and word.isalpha():
            WORDS.append(word.lower())


class WordleGuesser:
    def __init__(self, wordle: Wordle):
        """
        Initializes the WordleGuesser with a Wordle instance and a guessing method.

        :param wordle:
        """
        self.wordle = wordle
        self.possible_words = []
        self.feedbacks = []

    def reset(self):
        self.possible_words = []
        self.wordle.reset()
        self.feedbacks = []

    def word_matches_feedback(self, word, feedback):
        """
        Checks if a given word matches the feedback received so far.
        The feedback is a list of tuples where each tuple contains a letter and its status:
        - 0: Letter is not in the word (gray)
        - 1: Letter is in the word but in the wrong position (yellow)
        - 2: Letter is in the word and in the correct position (green)
        This function checks each letter in the feedback against the word to see if it matches the expected status.

        :param word: The word to check against the feedback.
        :param feedback: A list of tuples where each tuple contains a letter and its status.
        :return: True if the word matches the feedback, False otherwise.
        """
        for i, (letter, status) in enumerate(feedback):
            if status == 2 and word[i] != letter:
                #print("testing word:", word, "with feedback:", feedback, "-> does not match")
                return False
            elif status == 1 and (not letter in word or word[i] == letter):
                #print("testing word:", word, "with feedback:", feedback, "-> does not match")
                return False
            elif status == 0 and letter in word:
                #print("testing word:", word, "with feedback:", feedback, "-> does not match")
                return False
        #print("testing word:", word, "with feedback:", feedback, "-> matches")
        return True

    def get_possible_words(self):
        """
        Updates the list of possible words based on the feedback received so far.
        If no feedback has been received, it initializes the possible words with all valid words.
        If feedback has been received, it filters the words based on the feedback.

        :return: None
        """
        self.possible_words = []

        if len(self.feedbacks) == 0:
            self.possible_words = WORDS.copy()
            return

        for word in WORDS:
            valid = True
            for feedback in self.feedbacks:
                if not self.word_matches_feedback(word, feedback):
                    valid = False
                    break
            if valid: self.possible_words.append(word)

    def get_guess(self):
        """
        Returns a guess based on the current state of the game.
        :return: A word from the possible words list or None if no words are left.
        """
        self.get_possible_words()  # Update possible words based on feedback
        if not self.possible_words:
            return None

        # Randomly select a word from the possible words
        guess = random.choice(self.possible_words)
        return guess

        # maybe come back to this later, currently produces worse results than random choice
        '''
        # score words based on number of new letters they introduce
        new_letters = []
        used = set()
        for feedback in self.feedbacks:
            for letter, status in feedback:
                if status == 0:
                    used.add(letter)

        print(used)
        for l in ascii_lowercase:
            if l not in used:
                new_letters.append(l)
        print(f"New letters to consider: {new_letters}")

        scores = {}
        for word in self.possible_words:
            score = 0
            for letter in word:
                if letter in new_letters:
                    score += 1
            scores[word] = score

        # Sort words by score (descending) and return the first one
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print(f"Chose: {sorted_words[0][0]} with score {sorted_words[0][1]} from {len(self.possible_words)} possible words.")

        return sorted_words[0][0] if sorted_words else None
        '''

    def _make_guess(self, guess=None):
        """
        Makes a guess in the Wordle game and records the feedback.
        :param guess: The word to guess.
        :return: A tuple containing the guess and the feedback received.
        """
        feedback = self.wordle.guess(guess)
        self.feedbacks.append(feedback)
        return guess, feedback

    def make_guess(self):
        """
        Makes a guess based on the current state of the game.
        :return: A tuple containing the guess and the feedback received, or None if no more guesses can be made.
        """
        if len(self.feedbacks) >= self.wordle.max_guesses:
            return None
        guess = self.get_guess()
        if guess is None:
            return None
        #print(f"Guess: {guess}, Feedback: {feedback}")
        #print(f"Correct? {guess == self.wordle.correct_word}")
        #print(f"Possible words remaining: {len(self.possible_words)}")
        return self._make_guess(guess=guess)


def feedback_format(feedback):
    """
    Formats the feedback for display.
    :param feedback: List of tuples (letter, status)
    :return: Formatted string

    Example: [(a, 0), (b, 1), (c, 2)] -> "a0;b1;c2"
    """
    return ';'.join(f"{letter}{status}" for letter, status in feedback)


def feedback_parse(feedback_str):
    """
    Parses the feedback string into a list of tuples.
    :param feedback_str: Formatted string
    :return: List of tuples (letter, status)
    :exception: IndexError if the string is not formatted correctly
    :exception: ValueError if the status is not an integer

    Example: "a0;b1;c2" -> [(a, 0), (b, 1), (c, 2)]
    """
    return [(part[0], int(part[1])) for part in feedback_str.split(';')]


if __name__ == '__main__':
    import json

    w = Wordle()
    guesser = WordleGuesser(w)

    games = []

    num = 15000
    for i in range(num):
        guesser.reset()
        print(f"Game {i + 1}/{num}")
        game = {
            "attempts": 0,
            "correct_word": w.correct_word,
            "guesses": [],
            "feedbacks": [],
            "status": ""
        }
        while True:
            guess, feedback = guesser.make_guess()
            game["attempts"] += 1
            game["guesses"].append(guess)
            game["feedbacks"].append(feedback)

            if guess is None:
                game["status"] = "FAIL"
                games.append(game)
                break
            if guess == w.correct_word:
                game["status"] = "SUCCESS"
                games.append(game)
                break
            elif len(guesser.feedbacks) >= w.max_guesses:
                game["status"] = "FAIL"
                games.append(game)
                break

    print(f"Played {num} games.")
    success_rate = sum(1 for game in games if game["status"] == "SUCCESS") / num
    print(f"Success rate: {success_rate:.2%}%")
    avg_attempts = sum(game["attempts"] for game in games) / num
    print(f"Average attempts: {avg_attempts:.2f}")

    # save games to file
    _games = []
    for game in games:
        _game = {
            "attempts": game["attempts"],
            "correct_word": game["correct_word"],
            "guesses": game["guesses"],
            "feedbacks": [feedback_format(feedback) for feedback in game["feedbacks"]],
            "status": game["status"]
        }
        _games.append(_game)
    with open('game_data.json', 'w') as f:
        json.dump(_games, f, indent=4)

    print("Game data saved to game_data.json")
    input("Press ENTER to exit.")
