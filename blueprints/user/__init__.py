import datetime

class User():

	def __init__(self):
		self.reset()

	def reset(self):
		self.id = 0
		self.name = None
		self.age = 0
		self.sex = None
		self.client_id = None

	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'age': self.age,
			'sex': self.sex,
			"client_id": self.client_id
		}

#### Class for save data temporelly
class Users():

	users = []

	def __init__(self):
		pass

	def getall(self):
		return self.users

	def getone(self, id):
		for _, value in enumerate(self.users):
			if int(value['id']) == int(id):
				return value
		return None

	def add(self, user):
		self.users.append(user.serialize())

	def update(self, id, name, age, sex, client_id):
		for index, value in enumerate(self.users):
			if int(value['id']) == int(id):
				user = User()
				user.id = id
				user.name = name if name != None else value['name'] 
				user.age = age if age != None else value['age']
				user.sex = sex if sex != None else value['sex']
				user.client_id = client_id if client_id != None else value['client_id']
				self.users[index] = user.serialize()
				return user
		return None
	
	def delete(self, id):
		for index, value in enumerate(self.users):
			if int(value['id']) == int(id):
				user = User()
				user = value
				self.users[index] = user
				return user
		return None
