from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create the Flask app
app = Flask(__name__)

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    amount INTEGER,
                    upi_id TEXT
                )''')
    conn.commit()
    conn.close()

# Route to display the donation form and donation history
@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    
    # Get the donation history
    c.execute('SELECT * FROM donations')
    donations = c.fetchall()
    
    # Get the total donations
    c.execute('SELECT SUM(amount) FROM donations')
    total_donations = c.fetchone()[0] or 0

    conn.close()
    
    # Render the HTML page with donation history and total donations
    return render_template('index.html', donations=donations, total_donations=total_donations)

# Route to handle donation submission
@app.route('/donate', methods=['POST'])
def donate():
    # Get data from the form
    name = request.form['name']
    amount = request.form['amount']
    upi_id = request.form['upi_id']

    # Validate minimum donation
    if int(amount) < 30:
        return redirect(url_for('index'))  # Redirect if amount is less than ₹30

    # Insert donation into the database
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('INSERT INTO donations (name, amount, upi_id) VALUES (?, ?, ?)', (name, amount, upi_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))  # Redirect to the homepage after donation

if __name__ == '__main__':
    init_db()  # Initialize the database on startup
    app.run(debug=True)
