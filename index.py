from flask import Flask, render_template, request
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>柯泯靖Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=泯靖>傳送使用者暱稱</a><br>"
    homepage += "<a href=/me>柯泯靖的簡介網頁</a><br>"
    homepage += "<a href=/account>輸入帳號密碼</a><br>"
    homepage += "<a href=/search>課程查詢</a><br><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/me")
def me():
    return render_template("aboutme.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cond = request.form["keyword"]
        result = "您輸入的課程關鍵字是：" + cond 

    if request.method == "POST":
        cond = request.form["teacher"]
        result = "您輸入的教師關鍵字是：" + cond 

        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"]:
                #print("{}老師開的{}課程，每週{}於{}上課".format(dict["Leacture"]，dict["Course"]，dict["Time"]，dict["Room"]))
                result += dict["Leacture"] + "老師開的" + dict["Course"] + "課程，每週"
                result += dict["Time"] + "於" + dict["Room"] + "上課<br>"

            if result == "":
                result = "抱歉，查無相關條件的選修課程"
        return result
    else:
        return render_template("search.html")


#if __name__ == "__main__":
#    app.run()
