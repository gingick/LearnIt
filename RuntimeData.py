class RuntimeData: 
	loop = None
	temp_user = None
	knownUsers = None
	userState = None
	contador_user = None
	db = None

	def __init__(self):
		self.db = Database()
		self.loop = {}
		self.temp_user = {}
		self.knownUsers = db.get_known_users()
		self.userState = {}
		for user in knownUsers:
		self.userState[user] = '0'
		self.contador_user = {}

	def add_user(self,ID):
		m = self.db.add_user(ID)
		self.knownUsers.add(ID)
		self.set_state(ID,'0')
		return m
	
	def add_word(self,ID):
		try:
			return self.db.add_word(ID,temp_user[ID])
		except:
			print("There is no temp_user data for {}.".format(ID))
			return 'Error'
	
	def get_user_languages(self, ID):
		return self.get_user_languages(ID)
	
	def add_language(self, ID, language):
		self.db.add_language(ID,language)

	def erase_word(self,D, idiom, foreign_word):
		return self.db.erase_word(ID,idiom,foreign_word)

	def get_state(self, user):
		try:
			ret = self.userState[user]
			print("id:{}  state:{}".format(user,ret))
			return ret
		except:
			print("User {} doesn't exist".format(user))
			return 'Error'

	def set_state(self, user, new_state):
		self.userState[user] = new_state;