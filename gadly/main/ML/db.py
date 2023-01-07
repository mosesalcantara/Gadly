import pyrebase

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
db=firebase.database()

# gen_sen = []
# f = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\main\ML\gen_sen.txt', 'r')
# for line in f:
#     gen_sen.append(line.strip())
# f.close()

# not_gen_sen = []
# f = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\main\ML\not_gen_sen.txt', 'r')
# for line in f:
#     not_gen_sen.append(line.strip())
# f.close()

# db_data = {
#     'sensitive':gen_sen,
#     'not_sensitive':not_gen_sen
# }

# db.child("data_set").set(db_data)
