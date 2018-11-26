from flask import Flask, abort, request, jsonify, render_template, redirect, url_for, session
import pymongo
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/index", methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		userName = request.form['username']
		password = request.form['password']
		userInfo = users.find_one({"userName":userName})
		foundPassword = userInfo["password"]
	
		if str(foundPassword) == password:
			session['userName'] = userName
			return redirect(url_for('profile', userName=userName))

		return redirect(url_for('index'))


@app.route("/restaurants", methods=["GET"])
def restaurants():
	return render_template("main.html")

@app.route("/restaurant_detail", methods=["GET", "POST"])
def restaurant_detail():
	return render_template("restaurant_info.html")

@app.route("/profile/<string:userName>", methods=["GET"])
def profile(userName):
	return render_template("profile.html", userName=userName)

@app.route("/preferences/<string:userName>", methods=["GET", "POST"])
def preferences(userName):
	
	if request.method == 'GET':
		userInfo = users.find_one({"userName":userName})
		foodPrefs = userInfo["foodTags"]
		languagePrefs = userInfo["languageTags"]
		hobbyPrefs = userInfo["hobbyTags"]

		preferenceList = {'food': foodPrefs, 'language': languagePrefs, 'hobby': hobbyPrefs}
		return render_template("preferences.html", preferenceList = preferenceList, userName = userName)
	else:
		if request.form['submit_btn'] == 'add a food' and request.form['new_food'] is not None:
			food = request.form['new_food']
			print food
			userInfo = users.find_one({"userName":userName})
			foodPrefs = userInfo["foodTags"]
			print foodPrefs
			foodPrefs.append(food)
			users.find_one_and_update({"userName":userName}, 
										 {'$set': {"foodTags":foodPrefs}})
			return redirect(url_for('preferences', userName = userName))
			
		elif request.form['submit_btn'] == 'add a language' and request.form['new_lan'] is not None:
			lan = request.form['new_lan']
			userInfo = users.find_one({"userName":userName})
			languagePrefs = userInfo["languageTags"]
			languagePrefs.append(lan)
			users.find_one_and_update({"userName":userName}, 
										 {'$set': {"languageTags":languagePrefs}})
			return redirect(url_for('preferences', userName = userName))
		
		elif request.form['submit_btn'] == 'add a hobby' and request.form['new_hobby'] is not None:
			hobby = request.form['new_hobby']
			userInfo = users.find_one({"userName":userName})
			hobbyPrefs = userInfo["hobbyTags"]

			hobbyPrefs.append(hobby)
			users.find_one_and_update({"userName":userName}, 
										 {'$set': {"hobbyTags":hobbyPrefs}})
			return redirect(url_for('preferences', userName = userName))



@app.route("/messages", methods=["GET", "POST"])
def messages():
	return render_template("user_profile_msgbox.html")

if __name__ == '__main__':
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	db = client["local"]

	restaurants = db["restaurants"]
	users = db["users"]
	posts = db["posts"]
	responds = db["responds"]

	app.run(debug = True)
  