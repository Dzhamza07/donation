from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# In-memory database for storing donation data
donations = []

@app.route("/", methods=["GET", "POST"])
def home():
    total_donations = sum(donation["amount"] for donation in donations)
    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"])
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        donations.append({"name": name, "amount": amount, "date": date})
        total_donations += amount
    return render_template("index.html", donations=donations, total_donations=total_donations)

if __name__ == "__main__":
    app.run(debug=True)
