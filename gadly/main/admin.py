import pyrebase

from django.contrib import admin
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth'''

#admin sdk toh(instantiation palang)
#cred = credentials.Certificate("main\gadly-610fb-firebase-adminsdk-n2nse-ed658a6059.json")
#firebase_admin.initialize_app(cred)

config={
  "apiKey": "AIzaSyCnqRG_3w5Gb4JTlNwyMIVJs98crMBRULM",
  "authDomain": "gadly-610fb.firebaseapp.com",
  "databaseURL": "https://gadly-610fb-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "gadly-610fb",
  "storageBucket": "gadly-610fb.appspot.com",
  "messagingSenderId": "350424029795",
  "appId": "1:350424029795:web:9d900d96122c6d43f97656",
  "measurementId": "G-MQYBSZQ38P"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
dba=firebase.database()

#ito ayy sa pagreread ng users table from database para magamit sa paggawa ng table sa html
users =  dba.child("users").get()
print(users.val())

# Register your models here.
