from flask import Flask, render_template
from crud import get_data
from db_formation import SmsProcessor
import requests
import json



app = Flask(__name__)

keys = ["id", "address", "date_sent", "message", "service_center", "amount", "message_type", "category", "date"]


@app.route("/")
def home():
  get_obj = get_data()
  data = get_obj.all_data()
  return render_template("index.html", data=data)

if __name__== "__main__":
  app.run(debug=True)
