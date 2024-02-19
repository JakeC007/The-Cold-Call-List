![Logo](https://github.com/JakeC007/The-Cold-Call-List/blob/main/imgs/logo.png?raw=true)

# The Cold Call List
Given a roster of students, generates a semester long cold call list that ensures that students are picked randomly and fairly. 

Inspired after a day in class where a student was cold-called in sequential classes – and as a bid to procrastinate on building outlines for my administrative, antitrust, and constitutional law final exams – I created "The Cold Call List," which painlessly generates a semester long cold-call list that is designed to do the following:
-	Students are picked randomly and fairly for cold-calls
-	Enforce a minimum number of cold-calls to other students before a given student is eligible to be cold called again
-	Ensures that all students are cold-called the same number of times in a semester


## Great! How Can I Use It?
Currently, you need a slight amount of technical know-how and have Python, `numpy` and `pandas` installed on your computer. If you're missing the packages run `pip install -r requirements.txt` in your terminal. 

Then:
0. Have a csv with one column called `Names` and unique names for each student in that column 
1. Open `list_gen.py`
2. Edit `pd.read_csv('your/csv/goes/here')`
3. Edit `n` the number of times you want to cycle through your roster this semester
4. Edit `m` the minimum number of cold calls to other students before a given student is eligible to be cold called again
5. Run `list_gen.py` and it will write your new cold call list

## That is not very user friendly to non-technical people
Yeah, sorry about that. My roadmap is as follows to improve.

## Roadmap
- GUI to handle user input
     - Maybe run as a `ipynb` file in the meantime?
- More robust roster info
     - Handle `.xslx` files
     - Handle files where student names are split across a first name and last name column
- Package the program so it runs self contained?

