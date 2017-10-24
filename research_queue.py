from technologies import Technologies



# Not optimally implemented 
class ResearchQueue(dict):
	# self[METADATA] = (completed_time, expires_time, icon)
	def __init__(self, techs):
		super(ResearchQueue, self).__init__()
		self.previous_game_time = 0
		self.techs = techs
		self.researched = []
		self.k = {}

	# Adds to dictionary the research ((NOTE CAN OVERWRITE))
	def add(self, research_metadata, completed_percentage, icon):
		try:
			tech_name, tech_research_time = self.techs[research_metadata] #
		except KeyError:
			self.k[research_metadata] = research_metadata
			return
		# Fixing buggy MAA (blinking blue/grey)
		if research_metadata in Technologies.MAA:
			research_metadata = Technologies.MAA[0] # Just one metadata are acceptable

		completed = int(tech_research_time * 0.01 * completed_percentage)
		expires = int(tech_research_time)
		self[research_metadata] = [completed, expires, icon]

	# Update its time OR remove it
	def update(self, game_time):
		difference = game_time - self.previous_game_time
		#print(difference)
		remove = []
		# Iterate through the dictionary 
		for key in self:
			# Add the completed time
			self[key][0] += difference
			if self[key][0] >= self[key][1]:
				remove += [key] # Cant change dictionary size while iterating
		for key in remove:
			# Add research into the researched list
			#  v Fixes if the list is empty   v Do not add the research if 
			if not len(self.researched) or self.researched[-1][0] != key:  
				self.researched += [(key, game_time, self[key][2])] 
				self.techs.check_research_bonuses(key)
				#TODO CHECK BONUSES IN THIS DICT
			self.pop(key)
		self.previous_game_time = game_time
