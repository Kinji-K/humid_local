from flask import abort, Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

@app.route("/")
def PostHumid():
    ACCESS_URL = ""
    SLACK_URL = ""
    temp = ""
    humid = ""
    abs_humid = ""
    message = ""

    with open('url.json','r') as f:
        json_load = json.load(f)

        ACCESS_URL = json_load["ACCESS_URL"]
        SLACK_URL = json_load["SLACK_URL"]

    temp = request.args.get('temp')
    humid = request.args.get('humid')
    abs_humid = request.args.get('abs_humid')

    if temp == "" or humid == "" or abs_humid == "":
        message = "センサーエラーです"
    elif float(abs_humid) > 15: 
        message = "部屋の湿度が高いです\n絶対湿度は" + abs_humid + "です"
    elif float(abs_humid) < 5:
        message = "部屋が乾燥しています\n絶対湿度は" + abs_humid + "です"

    flug = requests.get(ACCESS_URL+"get")

    if flug.text == "0" and message != "":
        requests.post(SLACK_URL,data=json.dumps({
            "text" : message
        }))

    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
