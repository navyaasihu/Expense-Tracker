from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = os.path.join('data', 'expenses.csv')

@app.route('/')
def index():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
    total = df['Amount'].sum() if not df.empty else 0
    expenses = df.to_dict(orient='records')
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])

        new_expense = pd.DataFrame([[date, category, description, amount]], 
                                   columns=['Date', 'Category', 'Description', 'Amount'])

        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_expense], ignore_index=True)
        else:
            df = new_expense

        df.to_csv(DATA_FILE, index=False)
        return redirect(url_for('index'))

    return render_template('add_expense.html')

if __name__ == '__main__':
    app.run(debug=True)
