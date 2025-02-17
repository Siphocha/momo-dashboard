from crud import get_data
from flask import Flask, render_template

app = Flask(__name__)

keys = [
    "id",
    "address",
    "date_sent",
    "message",
    "service_center",
    "amount",
    "message_type",
    "category",
    "date",
]


@app.route("/")
def home():
    get_obj = get_data()
    data = get_obj.all_data()
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
