# Habit Tracker Web App

#### This is a Habit Tracker Web App powered by a Flask server

## Getting started

To get this app up and running, these are the steps that you have to take:

### 1. Install

To git clone the repo, this is what you should run:
```
git clone https://github.com/barroca8/Habit-Tracker-Web-App
```
After having the repo on your machine, you should make sure you have the requirements installed.
Assuming you have pip installed:
```
$ pip install -r requirements.txt
```
If you don't have pip, you can install the libraries on `requirements.txt` one by one by following [this step by step tutorial](https://www.geeksforgeeks.org/how-to-install-python-libraries-without-using-the-pip-command/) 

### 2. Editing the default habits (Optional):

If you go to `/test_data/predefined_habits.json` , you will find 5 habits in the following format, that you can edit, add and remove:

```
[
    {"name": "Brush Teeth", "periodicity": "D", "success_rate": 0.95},
    {"name": "Exercise", "periodicity": "D", "success_rate": 0.5},
    {"name": "Read Book", "periodicity": "W", "success_rate": 0.2},
    {"name": "Call Family", "periodicity": "W", "success_rate": 0.6},
    {"name": "Grocery Shopping", "periodicity": "M", "success_rate": 0.8}
]
```

Each habit of this list will be created the following way:
- "name": the name of the habit (str)
- "periodicity": the periodicity of the habit you're creating, between daily, weekly and monthly. Options: "D", "W", "M" (str)
- "success_rate": defines the success rate this generated habit will have, between 0 and 1 (float, int)
- a random date between 1 year ago and 2 years ago will be chosen as start date for this habit
- a random date between yesterday and 10 days ago will be choses as last update date (last time habit was completed)

### 3. Getting the server started

Assuming you have python installed already, all you have to do is run:
```
python main.py
```
And your app will run on `http://127.0.0.1:5000`

### 4. Using the web app

- **"Create Initial Habits" button**: Creates the habits defined in `/test_data/predefined_habits.json`, and adds them to the database
- **"Clear Habits Table" button**: Deletes all data of all habits
- **"Create Habit" section**: In this section you can create your own habit, by defining its name and periodicity (Daily, Weekly or Monthly)
- **Search Longest Streak**: This table shows all created habits, along with their ___ (insert all fields here after deciding final ones)
    - In this table you can: Mark a habit as completed, delete a habit and filter the table by periodicity
- **"Streaks" section**: This section does an automatic API request to the Flask server to check what are the longest active streaks for each periodicity
- **"Search Longest Streak" section**: In this section you can search a habit by typing its name and it will show the current streak for that habit
- **"Tracking Calendar" section**: In this section you can pick one of your habits and you will have a visualization of its completion


 
