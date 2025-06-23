import random


WORDS = []
with open('words.txt', 'r') as file:
    for line in file:
        word = line.strip()
        if len(word) == 5 and word.isalpha():
            WORDS.append(word.lower())



class Wordle:
    def __init__(self):
        self.correct_word = None
        self.guesses = []
        self.max_guesses = 6
        self.reset()

    def reset(self):
        """Reset the game state with a new random word."""
        self.correct_word = random.choice(WORDS)
        self.guesses = []

    def guess(self, word) -> list:
        """Make a guess and return feedback."""
        word = word.lower()
        if not word in WORDS:
            return [] # Invalid guess, not in word list

        feedback = []
        for i, letter in enumerate(word):
            if letter == self.correct_word[i]:
                feedback.append((letter, 2)) # 2 for correct position, correct letter
            elif letter in self.correct_word:
                feedback.append((letter, 1)) # 1 for correct letter, incorrect position
            else:
                feedback.append((letter, 0)) # 0 for incorrect letter

        self.guesses.append((word, feedback))
        return feedback


if __name__ == '__main__':
    w = Wordle()
    while True:
        guess = input("Enter your 5-letter guess (or 'exit' to quit): ").strip()
        if guess.lower() == 'exit':
            break
        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        feedback = w.guess(guess)
        print("Feedback:", feedback)

        if guess == w.correct_word:
            print("Congratulations! You've guessed the word:", w.correct_word)
            break
        elif len(w.guesses) >= w.max_guesses:
            print("Sorry, you've used all your guesses. The correct word was:", w.correct_word)
            break