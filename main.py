from WordleGuesser import WordleGuesser
from wordle import Wordle



if __name__ == "__main__":
    w = Wordle()
    guesser = WordleGuesser(w)

    print("Feedback format:\n0 = Not in Word (Gray)\n1 = In word, Wrong Position\n2 = In word, Correct Position\ne.g. 01021")

    while True:
        suggested_word = guesser.get_guess()
        if suggested_word is None:
            print("No more possible words to guess.")
            input("Press enter to continue...")
            break

        print(f"\n\nSuggested word: {suggested_word}")
        print(f"Total possible words remaining: {len(guesser.possible_words)}")

        user_input = input("Enter feedback for the suggested word.\n> ").strip()
        if user_input.lower() == 'exit':
            print("Exiting the game.")
            break
        elif user_input.lower() == 'reset':
            guesser.reset()
            print("Game reset. Starting over.")
            continue
        elif user_input.lower() == 'remove_last_guess':
            if guesser.feedbacks:
                removed_feedback = guesser.feedbacks.pop()
                print(f"Removed last guess feedback: {removed_feedback}")
            else:
                print("No feedback to remove.")
            continue

        feedback = []
        idx = 0
        for char in user_input:
            if char not in '012':
                print("Invalid input. Please enter digits only (0, 1, or 2).")
                break

            feedback.append((suggested_word[idx], int(char)))
            idx += 1


        #print(f"Feedback: {feedback}")
        guesser.feedbacks.append(feedback)