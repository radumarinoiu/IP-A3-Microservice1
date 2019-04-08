import pymongo

from pymongo import MongoClient
client = MongoClient()

db = client['tasks_db']
tasks = db['tasks']

def put_task(id, s)
	[nume, creare, expirare] = s.split('&')
	[nume, nume_val] = nume.split(':')
	[creare, creare_val] = creare.split(':')
	[expirare, expirare_val] = expirare.split(':')
	if nume_val != null :
		tasks.update({'_id': id}, {'nume': nume_val}, upsert = False)
	if creare_val != null:
		tasks.update({'_id': id}, {'creare': creare_val}, upsert = False)
	if expirare_val != null:
		tasks.update({'_id': id}, {'expirare': expirare_val}, upsert = False)

