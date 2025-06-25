# Expense Tracker (CS50P Final Project)

## Video Demo

https://www.youtube.com/watch?v=myGbfCjv9_Q


## Description

This Expense Tracker is a Python-written desktop application that helps users track their monthly and daily expenses. It was developed using tkinter and ttkbootstrap and serves as a friendly graphical user interface in which users can enter, save, and see expenditures. The application helps users keep track of personal finances with fewer barriers by incorporating an easy-to-use interface and immediate feedback, long-term storage, and some basic data visualization.

The user can enter an expense with the type (bills, food, transportation), date, and cost. The entries will be saved into a local JSON file, allowing the app to maintain expense history during stretches where the application is opened and closed. The application loads the most recent expense data from the JSON file when started and allows the user to view, modify, and extend previous entries.

The program allows for additional visualization of expenditure in various categories or time periods, using the matplotlib module, which plots a user's expenditure on an x and y axis. This allows a user to see patterns of expenditure, which informs them in areas of overspending and more budget-savvy management.

This project was serendipitously the last available assignment for CS50's Introduction to Programming with Python. The project utilizes a number of concepts learned in the course including file I/O, data structures (most notably dictionaries and lists), Python object-oriented programming principles, and matplotlib tools for data visualization.

In using this application, I had the opportunity to do event-driven programming for a GUI—something not explicitly taught via CS50P, but highly relevant to real-world applications. I had to design easy-to-use layouts through `tkinter` frames and grid control, refresh state changes as a result of button presses or form submission, and ensure that the program can stay responsive even when the user provides invalid or unexpected inputs. These problems led me to write modular defensive code and to execute the program on a regular basis as I developed each feature.

One of the features that I am most satisfied with is the JSON persistence system. Instead of using external, independent databases, which would be superfluous for a desktop application running locally, I decided to employ Python's `json` module to serialize and deserialize user data. This allowed me to have organized data in a compact format and still leave the file human-readable and easy to back up or transfer. It also forced me to consider edge cases like how to deal with an empty or invalid JSON file upon starting the application.

The visualisation aspect was another tricky technical problem. I used `matplotlib` to create bar plots showing total spending by category. This meant taking the raw data and formatting it so that it could be plotted, for example, by calculating sums and grouping entries by category. I also had to blend `matplotlib` with the `tkinter` event loop, which meant figuring out how to embed plots in the GUI window rather than present them in a pop-up window.

The overall design goal for this project was simplicity. I did not wish to overwhelm the user with jargon terms or complicate them with too many choices. Instead, I wished to design an interface that a first-time budgeting app user could easily understand. Everything—from recording an expense, to viewing a chart, to closing the app—is a couple clicks away. The emphasis is on control, speed, and simplicity.

Overall, this project enabled me to synthesize nearly everything I'd covered in CS50P: Python syntax, algorithmic problem-solving, input and output, programming with modules, error handling with elegance, and writing programs that are of use beyond the classroom. It also proved to be a useful learning experience of splitting a large application into manageable parts—setting out the core logic first, then attaching on the UI, and finally making the user experience shine with polish like visualization and styling. I'm also satisfied with how the project ended up, and I can see ways that I could expand upon it in the future—maybe with budget targets, multi-user support, or exporting to CSV.

## Features

- GUI built with `Tkinter` and styled using `ttkbootstrap`
- Add expenses with name, amount, date, and category
- Real-time monthly total and category breakdown
- Pie chart visualization using `matplotlib`
- Spending prediction using a 3-month average
- JSON-based data persistence

## Requirements

- Python 3.x
- `ttkbootstrap`
- `matplotlib`

Install dependencies:
```bash
pip install ttkbootstrap matplotlib
