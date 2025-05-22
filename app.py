from collections import defaultdict
import json

@app.route('/')
def index():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])
    total = df['Amount'].sum() if not df.empty else 0
    expenses = df.to_dict(orient='records')

    # Prepare data for chart
    category_totals = df.groupby('Category')['Amount'].sum().to_dict()
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    return render_template('index.html', expenses=expenses, total=total,
                           categories=json.dumps(categories),
                           amounts=json.dumps(amounts))
