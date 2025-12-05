# Exercise 1 - Maths Quiz

Develop a GUI using Tkinter that presents the user with quiz of arithmetic problems. Each "play" of the quiz should be 10 questions. The user should initially be presented with a short menu of options to select a difficulty level. It could look something like this:

    DIFFICULTY LEVEL
     1. Easy
     2. Moderate
     3. Advanced

The difficulty levels determine the number of digits in the numbers to be added or subtracted. Easy means only single digit numbers; moderate means double digit numbers; and advanced means 4-digit numbers. After the user picks the level they desire, your program presents problems that look like this:

    45 + 9 =
    34 - 88 =
    etc

For each problem presented, the user is given a chance to answer. If the answer is correct, another problem is presented. If the answer is wrong, the user is to be given one more chance at that problem. The program should keep a tally of the users score, awarding 10 points for a correct answer on first attempt and 5 points on the second attempt. You should implement a random number generator (see the resources folder) to determine:
- The values to be added or subtracted
- Whether the problem is addition or subtraction

&nbsp;
The program should include the functions listed below. These functions should make use of parameters and return values as appropriate. You may include others or extend the functionality of the program if you see fit.
- **displayMenu**: A function that displays the difficulty level menu at the beginning of the quiz.
- **randomInt**: A function that determines the values used in each question. The min and max values of the numbers should be based on the difficulty level chosen as described above.
- **decideOperation**: A function that randomly decides whether the problem is an addition or subtraction problem and returns a char.
- displayProblem: A function that displays the question to the user and accepts their answer.
-** isCorrect**: A function that checks whether the users answer was correct and outputs an appropriate message
- **displayResults**: function that outputs the users final score out of a possible 100 and ranks the user based on their score (e.g. A+ for a score over 90)

&nbsp;
Once the user has finished the quiz, prompt them to see if they'd like to play it again

&nbsp;
**HINT :**
- Use Labels to display questions and instructions.
- Use Entry widgets to accept answers.
- Use Buttons for submitting answers, selecting difficulty, and replaying.
- Use Label/messagebox to display results or feedback messages.