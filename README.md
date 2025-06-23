# Wordle solver
A simple Wordle solver that uses a dictionary of words to find the best guess based on the previous guesses and their results.

# Usage
    ```bash
    git clone https://github.com/SnekProgrammer/WordleSolver.git
    cd WordleSolver
    python main.py
    ```
To use a different wordlist, you can replace the `words.txt` file, it should be one word per line.

# Accuracy
A test run of 15,000 games:\
**Success rate:** 83.47%  

| Guess       | Success Rate |
|-------------|--------------|
| 1st guess   | 0.01%        |
| 2nd guess   | 1.10%        |
| 3rd guess   | 9.21%        |
| 4th guess   | 25.68%       |
| 5th guess   | 28.70%       |
| 6th guess   | 18.76%       |

**Average attempts:** 4.88


# Example game
Correct word is `skimp`
```commandline
Feedback format:
0 = Not in Word (Gray)
1 = In word, Wrong Position
2 = In word, Correct Position
e.g. 01021


Suggested word: axial
Total possible words remaining: 12972
Enter feedback for the suggested word.
> 00200


Suggested word: reiks
Total possible words remaining: 570
Enter feedback for the suggested word.
> 00211


Suggested word: spink
Total possible words remaining: 14
Enter feedback for the suggested word.
> 21201


Suggested word: skimp
Total possible words remaining: 1
Enter feedback for the suggested word.
>
```


# Credits
Wordlist from https://github.com/steve-kasica/wordle-words/tree/master

