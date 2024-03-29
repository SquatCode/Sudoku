from flask import Flask, render_template

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

import sudoku_solver

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess huh'

bootstrap = Bootstrap(app)


class SudokuForm(FlaskForm):
    sudoku_puzzle = TextAreaField("SudokuPuzzle", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    name = None
    numbers = sudoku_solver.BLANK_PUZZLE
    numbers[38] = '1'
    numbers[51] = '2'
    numbers[66] = '8'
    numbers[80] = '9'
    return render_template('index.html', numbers=numbers)


@app.route('/solve_helper', methods=['GET', 'POST'])
def solve_helper():
    form = SudokuForm()
    if form.validate_on_submit():
        my_puzzle = sudoku_solver.SudokuSolver(puzzle_string = form.sudoku_puzzle.data)
        puzzle_solution = my_puzzle.get_possibilities_for_web() # TODO: make new function to make possibilities pretty
        reduced_puzzle = my_puzzle.get_reduced_puzzle()
        return render_template('solved.html', numbers=puzzle_solution, reduced_puzzle=reduced_puzzle)
    name = None
    numbers = [i for i in range(0, 81)]
    return render_template('solve_input.html', numbers=numbers, form=form)

@app.route('/solved/')
def solved():
    return render_template('solved.html',numbers=sudoku_solver.BLANK_PUZZLE)

@app.route('/advanced_solver/',methods=['GET','POST'])
def advanced_solver():
    return render_template('solved.html')
    # TODO: make an advanced solver using a backtracking algorithm
        # Which takes advantage of having reduced solutions from the beginning.
    # TODO: figure out how flask does rest in this situation
    '''
    That is, how can I go from a webpage that the SERVER creates 
        (from info the CLIENT provides)
        to another webpage that the SERVER creates
    '''