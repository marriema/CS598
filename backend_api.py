from flask import Flask, abort, request, jsonify, render_template
import pymongo
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["local"]

restaurants = db["restaurants"]
users = db["users"]
posts = db["posts"]
responds = db["responds"]


#SIGN UP--create a user account, store username and password to database
def addNewUserAccount(username, password):
	newUserAccount = {"userName":username, "password":password, "foodTags": [], "languageTags":[], "hobbyTags":[] }
	users.insert_one(newUserAccount)
	return

#LOG IN--check if password match the given username
def matchPassword(userName, inputPassword):
	userInfo = users.find_one({"userName":userName})
	foundPassword = userInfo["password"]
	return foundPassword == inputPassword


# addNewUserAccount("hahaha", "1234")
# print(matchPassword("tracy", 1234))
# print(matchPassword("tracy", 2143))

#Update users preference on user account
def updateUserPreferences(userName, userFoodTags, userLanguageTags, userHobbyTags):
	userInfo = users.find_one_and_update({"userName":userName}, 
										 {'$set': {"foodTags":userFoodTags, "languageTags":userLanguageTags, "hobbyTags":userHobbyTags}})
	return 

# updateUserPreferences("hahaha", ["No Green Onion"], ["Chinese, English"], ["Travel", "Movies"])

#get user profile Info
def getUserPreferences(userName):
	userInfo = users.find_one({"userName":userName})

	foodPrefs = userInfo["foodTags"]
	languagePrefs = userInfo["languageTags"]
	hobbyPrefs = userInfo["hobbyTags"]

	userPreferences = [foodPrefs, languagePrefs, hobbyPrefs]
	return jsonify(userPreferences)

# print(getUserPreferences("tracy"))


#get all resturants Infomation
def getAllRestaurantsInfo():
	RestaurantsInfo = Restaurants.find({})
	return jsonify(list(RestaurantsInfo))

# print(getAllRestaurantsInfo())


#get one Restaurant infomation given itsName 
def getOneRestaurantInfo(RestaurantName):
	RestaurantInfo = restaurants.find_one({"name": RestaurantName})

	# name = RestaurantInfo["name"]
	# cusineStyle = RestaurantInfo["type"]
	# street = RestaurantInfo["street"]
	# city = RestaurantInfo["city"]
	# state = RestaurantInfo["state"]
	# zipCode = RestaurantInfo["zipCode"]

	return jsonify(RestaurantInfo)

# print(getOneResturantInfo("Mid Summer Lounge"))


#get previous posts of a Restaurants 
def getAllPostsOfOneRestaurant(RestaurantName):
	cursor = posts.find({"restaurant": RestaurantName})
	restaurantPosts = []

	for post in cursor:
		restaurantPosts.append(post)
	return jsonify(restaurantPosts)

# print(getAllPostsOfOneRestaurant("Kongfu BBQ"))



#a user send a new response to a post
def addNewResponseToPost(postId, responseUserName, sentMsg):
	responses = posts.find_one({"id": postId})["respondedPeople"]
	if responseUserName not in responses:
		responses[responseUserName] = sentMsg

	posts.find_one_and_update({"id":postId}, {'$set':{"respondedPeople": responses}})
	newResponse = {"respondPeople": responseUserName, "respondMessage": sentMsg, "postID":postId}
	responds.insert_one(newResponse)

	return

# addNewResponseToPost("marrie Kongfu BBQ 10:30AM", "stanley", "Hello I am Stanley")


#add new post under a resturant page
def addNewPost(restaurantName, postUserName, time):
	newID = postUserName + " " + restaurantName + " " + time
	newPost = {"sender":postUserName, "restaurant":restaurantName, "time":time, "respondedPeople":[], "id": newID}
	posts.insert_one(newPost)
	return 

# addNewPost("Mid Summer Lounge", "marrie", "2:00 PM")

#get previous post of a user
def getHistoryPostsOfOneUser(userName):
	historyPosts =[]
	for post in posts.find({"sender":userName}):
		historyPosts.append(post)

	return jsonify(historyPosts)

# print(getHistoryPostsOfOneUser("marrie"))

#get previous sent message of a user
def getPreviousSentMessagesOfOneUser(userName):
	sentMessages = []
	for msg in responds.find({"respondPeople":userName}):
		sentMessages.append(msg)

	return sentMessages

# print(getPreviousSentMessagesOfOneUser("tracy"))

#update database according to one accepted response
def updatePostsAndSendAutomaticMsg(postId, postUser, selectedResponseUser):
	#delete the post from postUser's post section according to postId
	#send postUser's phone number to the selectedResponseUser








	

