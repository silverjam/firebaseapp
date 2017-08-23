import pyrebase
import sys

apiKey = "AIzaSyCGUHS5j7g8CZXxJrKmOQnMKRVd-A5luUI"
authDomain = "silv3rjam-c86a2.firebaseapp.com"
databaseURL = "https://silv3rjam-c86a2.firebaseio.com"
projectId = "silv3rjam-c86a2"
storageBucket = "silv3rjam-c86a2.appspot.com"
messagingSenderId = "201351615676"

config = {
      "apiKey": apiKey,
      "authDomain": authDomain,
      "databaseURL": databaseURL,
      "storageBucket": storageBucket,
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

try:
    db.child("messages").push({"message": "should not work"})
except Exception as e:
    print(e)

auth = firebase.auth()
refreshToken = sys.argv[1]
user = auth.refresh(refreshToken)

print(user)

db.child("messages").push({"message": "this should work!"})
