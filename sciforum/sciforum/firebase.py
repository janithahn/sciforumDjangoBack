import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/work/CS304/project/sciforumDjangoBack/sciforumchat-firebase-adminsdk-a4c26-5cac033bb0.json")
firebase_admin.initialize_app(cred)