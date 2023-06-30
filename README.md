CMU 15-112: Fundamentals of Programming and Computer Science
Term Project: Sudoku

Description:
Welcome to our term project readme file!

For our term project, we have decided to write a sudoku game inspired by the New York Times Sudoku.

There are a total of three screens that you can access: Splash Screen, Play Screen, and Help Screen

1. Splash Screen: This is the screen that comes up when we first run the app. On this screen, we can read some history about sudoku and Professor Kosbie. You can actually start playing the game by pressing one of the difficulties displayed in the middle of the screen.

2. Play Screen: This is the screen you enter once you choose a difficulty that you want to play.You can click the 'back' button on the top left to return to the spalsh screen to choose another difficulty and load another board. You can also view the difficulty of the current board on the top.

3. Help Screen: You can access the help screen within the 'Play Screen' by clicking the small question mark on the top right.Clicking the button shows a box that contains information on how to play, some tips, and a short guide.

Play Features:

1. There are two modes that you can make adjustments to the board. You can enter normal mode by clicking the 'Normal' button on the top right and enter candidate mode by clicking the 'Candidate' button on the top right. In normal mode, you can select a changable cell to highlight it and press a number on the number pad to change the value, or press the 'X' on the bottom to remove the value. In candidate mode, you can select a cell with no value in it to highlight it and press numbers on the number pad to add it as a potential candidate to the cell.

2. You can click the small box next to 'Auto Candidate Mode' to view the legal values that the cell can take and click it again to stop viewing.

3. You can click the 'Auto-Fill Naked Singles' to automatically fill all the cells with only one legal value left.

4. You can click the 'Remove Naked Tuples' to automatically ban obvious tupes from all the cells.

5. When you enter a wrong value into a cell, a red dot will appear in the cell to indicate that you placed a wrong value.


How to Run:

When you open the file, you will see two folders ('_MACOSX' and 'sudoku') as well as several text files. In order to run the game, you need to enter the 'sudoku' folder, make sure 'cmu_graphics' folder is inside the 'sudoku' folder and run the 'sudoku.py' python file.
