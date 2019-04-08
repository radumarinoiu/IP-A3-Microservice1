import pymongo
import datetime

from pymongo import MongoClient

client = MongoClient()
db = client['tasks_db']

def post_task(s)

	[nume, creare, expirare] = s.split('&')
	[nume, nume_val] = nume.split(':')
	[creare, creare_val] = creare.split(':')
	[expirare, expirare_val] = expirare.split(':')


	if nume == 'nume' and creare == 'creare' and expirare == 'expirare' :
		post = {nume: nume_val, creare: creare_val, expirare: expirare_val}
		posts = db.tasks
		post_id = posts.insert_one(post).inserted_id
