# -*- coding: utf-8 -*-
from copy import deepcopy

class Technologies(dict):
	# Unique techs 
	UNIQUE_TECHS = {
		# T1 - Unique Castle Age Technology
		# T2 - Unique Imperial Age Technology
		# T3 - Unique Unit Upgrade
		# Civ           T1  T2  T3
		"Aztecs"     : [40, 60, 45],
		"Berbers"    : [40, 40, 45],
		"Britons"    : [60, 40, 60],
		"Burmese"    : [40, 40, 65],
		"Byzantines" : [40, 50, 50],
		"Celts"      : [30, 50, 45],
		"Chinese"    : [40, 60, 50],
		"Ethiopians" : [40, 40, 45],
		"Franks"     : [40, 60, 45],
		"Goths"      : [40, 40, 40],
		"Huns"       : [40, 60, 45],
		"Incas"      : [40, 40, 45],
		"Indians"    : [40, 40, 60],
		"Italians"   : [40, 60, 60],
		"Japanese"   : [40, 60, 60],
		"Khmer"      : [40, 40, 70],
		"Koreans"    : [40, 60, 75],
		"Magyars"    : [40, 40, 60],
		"Malay"      : [40, 40, 40],
		"Malians"    : [40, 40, 45],
		"Mayans"     : [40, 50, 45],
		"Mongols"    : [40, 60, 50],
		"Persians"   : [40, 50, 75],
		"Portuguese" : [40, 40, 45],
		"Saracens"   : [30, 50, 50],
		"Slavs"      : [40, 40, 60],
		"Spanish"    : [40, 60, 60],
		"Teutons"    : [60, 60, 50],
		"Turks"      : [60, 40, 55],
		"Vietnamese" : [40, 40, 45],
		"Vikings"    : [40, 40, 45]
	}
	
	TECHNOLOGIES = {
		"Town Center" : {
			(255, 75, 255, 0, 0, 47, 0)         : ["Feudal Age", 130],
			(255, 255, 84, 0, 0, 35, 0)         : ["Castle Age", 160],
			(255, 174, 255, 0, 0, 225, 0)       : ["Imperial Age", 190],
			(40, 197, 94, 53, 94, 74, 173)      : ["Loom", 25],
			(21, 103, 159, 130, 0, 0, 0)        : ["Wheelbarrow", 75],
			(89, 169, 21, 173, 114, 0, 6)       : ["Hand Cart", 55],
			(237, 0, 0, 21, 0, 208, 0)          : ["Town Watch", 25],
			(89, 135, 89, 135, 0, 67, 0)        : ["Town Patrol", 40],
		},
		"Blacksmith" : {
			(114, 135, 103, 184, 89, 67, 40)    : ["Forging", 50],
			(145, 223, 102, 255, 223, 106, 219) : ["Scale Mail Armor", 40],
			(241, 255, 219, 255, 223, 106, 219) : ["Scale Barding Armor", 45],
			(0, 144, 173, 0, 31, 0, 0)          : ["Fletching", 30],
			(141, 185, 114, 157, 176, 186, 157) : ["Padded Archer Armor", 40],
			(21, 114, 53, 144, 103, 0, 144)     : ["Iron Casting", 75],
			(185, 106, 102, 102, 0, 154, 0)     : ["Chain Mail Armor", 55],
			(255, 106, 145, 102, 0, 154, 0)     : ["Chain Barding Armor", 60],
			(53, 185, 145, 0, 0, 0, 0)          : ["Bodkin Arrow", 35],
			(162, 255, 47, 241, 129, 53, 176)   : ["Lether Archer Armor", 55],
			(123, 184, 184, 21, 21, 153, 21)    : ["Blast Furnance", 100],
			(145, 223, 102, 255, 145, 127, 223) : ["Plate Mail Armor", 70],
			(241, 199, 255, 255, 145, 127, 223) : ["Plate Barding Armor", 75],
			(191, 206, 103, 0, 0, 0, 0)         : ["Bracer", 40],
			(84, 223, 35, 6, 21, 84, 223)       : ["Ring Archer Armor", 70],
		},
		"Barrax" : {
			(0, 154, 195, 145, 0, 185, 0)       : ["Man-at-Arms", 40], 
			(0, 154, 247, 145, 0, 185, 0)       : ["Man-at-Arms", 40], # Icon is a gif (once blue once grey)
			(0, 223, 255, 145, 0, 185, 0)       : ["Long Swordsman", 45], # Icon is blinking (once blue once grey) But it has no effect on these values
			(0, 127, 145, 145, 0, 185, 0)       : ["Two/Handed Swordsman", 75],
			(0, 133, 127, 106, 0, 185, 0)       : ["Champion", 100],
			(0, 241, 0, 0, 0, 0, 0)             : ["Pikeman", 45],
			(87, 28, 87, 0, 0, 0, 0)            : ["Halberdier", 50],
			(237, 106, 127, 145, 0, 241, 53)    : ["Eagle Warrior", 50],
			(237, 106, 127, 145, 0, 241, 195)   : ["Elite Eagle Warrior", 40],
			(173, 130, 114, 173, 0, 144, 181)   : ["Tracking", 35],
			(84, 157, 47, 169, 0, 241, 0)       : ["Squires", 40],
			(146, 146, 208, 21, 35, 173, 71)    : ["Arson", 25],
		},
		"Archery Range" : {
			(102, 87, 0, 0, 0, 0, 0)            : ["Crossbowman", 35],
			(28, 145, 27, 145, 85, 0, 135)      : ["Elite Skirmisher", 50],
			(254, 47, 145, 127, 28, 0, 47)      : ["Imperial Skirmisher", 45],
			(223, 0, 0, 127, 31, 0, 0)          : ["Heavy Cavalry Archer", 35],
			(106, 0, 0, 114, 0, 0, 0)           : ["Arbalest", 50],
			(28, 87, 145, 0, 0, 67, 0)          : ["Thumb Ring", 45],
			(47, 47, 0, 0, 157, 0, 82)          : ["Parthian Tactics", 65],
		},
		"Stable" : {
			(61, 47, 47, 57, 133, 0, 129)       : ["Light Cavalry", 45], # Shares same icon with hussar.
			(62, 47, 47, 57, 133, 0, 129)       : ["Hussar", 50], # Shares the same icon with Light Cavalry
			(185, 66, 6, 40, 161, 0, 223)       : ["Cavalier", 100],
			(87, 9, 245, 237, 0, 0, 0)          : ["Heavy Camel", 125],
			(106, 82, 174, 67, 0, 0, 0)         : ["Elite Battle Elephant", 80],
			(208, 49, 6, 63, 181, 0, 208)       : ["Paladin", 170],
			(47, 181, 114, 0, 114, 47, 114)     : ["Bloodlines", 50],
			(103, 79, 79, 208, 82, 187, 77)     : ["Husbandry", 40],
			(87, 66, 245, 237, 0, 0, 0)         : ["Imperial Camel", 125],
		}, 
		"Siege Workshop" : {
			(106, 57, 21, 0, 0, 0, 0)           : ["Capped Ram", 50],
			(53, 130, 57, 84, 156, 0, 114)      : ["Onager", 75],
			(185, 0, 111, 28, 28, 0, 0)         : ["Heavy Scorpion", 50],
			(145, 145, 145, 67, 0, 0, 0)        : ["Siege Ram", 75],
			(0, 189, 0, 63, 117, 84, 114)       : ["Siege Onager", 150],
		},
		"Monastry" : {
			(232, 181, 114, 6, 35, 68, 35)      : ["Redemption", 50],
			(144, 28, 185, 59, 144, 107, 107)   : ["Atonement", 40],
			(35, 6, 117, 53, 117, 171, 106)     : ["Fervor", 50],
			(188, 90, 213, 0, 0, 0, 0)          : ["Sancity", 60],
			(47, 156, 209, 29, 38, 67, 11)      : ["Faith", 60],
			(223, 255, 255, 189, 189, 87, 141)  : ["Illumination", 65],
			(144, 102, 144, 0, 0, 0, 0)         : ["Block Printing", 55],
			(129, 129, 129, 129, 40, 173, 129)  : ["Heresy", 60],
			(84, 141, 129, 0, 82, 176, 0)       : ["Theocracy", 75],
			(168, 86, 87, 51, 106, 82, 53)      : ["Herbal Medicine", 35],
		},
		"Castle" : {
			(156, 0, 0, 0, 223, 0, 174)         : ["Unique Technology (Castle)", 40], # Research time is depended on civ.
			(103, 0, 0, 0, 223, 0, 145)         : ["Unique Technology (Imperial)", 40], # Research time is depended on civ.
			(0, 227, 245, 0, 0, 0, 0)           : ["Elite Unique Unit", 60], # Research time is depended on civ.
			(87, 223, 53, 129, 113, 0, 129)     : ["Hoardings", 75],
			(0, 67, 102, 0, 0, 0, 0)            : ["Sappers", 10],
			(191, 79, 173, 245, 0, 0, 0)        : ["Conscription", 60],
			(215, 6, 55, 219, 227, 77, 186)     : ["Spies/Treason", 1],
		},
		"Market" : {
			(0, 245, 181, 0, 0, 0, 0)           : ["Cartography", 1], 
			(114, 84, 232, 0, 0, 0, 129)        : ["Coinage", 70],
			(189, 0, 0, 0, 0, 173, 223)         : ["Guilds", 50],
			(53, 237, 21, 173, 130, 0, 31)      : ["Caravan", 40],
			(82, 0, 0, 114, 0, 0, 114)          : ["Banking", 70],
		},
		"University" : {
			(0, 191, 129, 0, 219, 161, 117)     : ["Masonry", 50],
			(144, 114, 0, 0, 0, 0, 0)           : ["Treadmill Crane", 50],
			(208, 208, 232, 40, 40, 40, 144)    : ["Heated Shot", 30],
			(255, 209, 103, 96, 53, 187, 28)    : ["Ballistics", 60],
			(47, 107, 255, 117, 67, 0, 78)      : ["Chemistry", 100],
			(87, 87, 6, 208, 87, 67, 227)       : ["Siege Engineers", 45],
			(106, 47, 185, 106, 106, 6, 0)      : ["Architecture", 70],
			(127, 28, 82, 87, 102, 106, 106)    : ["Arrowslits", 25],
			(83, 31, 187, 187, 103, 131, 61)    : ["Murder Holes", 60],
			(94, 168, 144, 178, 127, 255, 63)   : ["Guard Tower", 30],
			(187, 117, 28, 67, 47, 47, 154)     : ["Fortified Wall", 50],
			(117, 185, 0, 106, 178, 28, 0)      : ["Bombard Tower", 60],
			(28, 117, 81, 168, 67, 178, 102)    : ["Keep", 100],
		}, 
		"Mill" : {
			(255, 0, 0, 0, 0, 0, 0)             : ["Horse Collar", 20],
			(0, 173, 185, 0, 185, 6, 0)         : ["Heavy Plow", 40],
			(80, 183, 183, 130, 85, 70, 159)    : ["Crop Rotation", 70],
		},
		"Lumber camp" : {
			(87, 254, 255, 0, 57, 0, 0)         : ["Double-Bit Axe", 25],
			(0, 0, 0, 130, 0, 0, 255)           : ["Bow Saw", 50],
			(0, 255, 255, 0, 0, 0, 0)           : ["Two-Man Saw", 100],
		},
		"Quarry" : {
			(103, 114, 71, 89, 21, 0, 0)        : ["Gold Mining", 30],
			(144, 111, 31, 156, 113, 42, 0)     : ["Gold Shaft Mining", 75],
			(103, 114, 219, 89, 21, 0, 0)       : ["Stone Mining", 30],
			(144, 111, 31, 156, 87, 42, 183)    : ["Stone Shaft Mining", 75],
		},
		"Dock" : {
			(35, 46, 127, 46, 107, 65, 35)      : ["Gillnets", 45],
			(84, 114, 144, 255, 84, 145, 255)   : ["Careening", 50],
			(47, 223, 40, 0, 0, 0, 67)          : ["Shipwright", 60],
			(31, 53, 84, 63, 57, 130, 255)      : ["War Galley, Fire/Demo Ship", 50],
			(255, 114, 144, 255, 84, 145, 255)  : ["Dry Dock", 60],
			(114, 144, 114, 67, 21, 135, 47)    : ["Galleon", 65],
			(78, 103, 40, 24, 6, 47, 129)       : ["Heavy Demolition Sheep", 50],
			(129, 28, 47, 28, 0, 0, 0)          : ["Fast Fire Ship", 50],
			(21, 255, 6, 63, 71, 173, 47)       : ["Cannon Galleon", 50],
			(127, 63, 114, 57, 21, 135, 47)     : ["Elite Cannon Galleon", 30],
		}
	}
	
	UNIQUE_CASTLE_TECH = (156, 0, 0, 0, 223, 0, 174)
	UNIQUE_IMPERIAL_TECH = (103, 0, 0, 0, 223, 0, 145)
	ELITE_UNIT_UPGRADE_TECH = (0, 227, 245, 0, 0, 0, 0)
	LIGHT_CAVALRY = (61, 47, 47, 57, 133, 0, 129)
	HUSSAR = (62, 47, 47, 57, 133, 0, 129)
	MAA = [(0, 154, 195, 145, 0, 185, 0),
	       (0, 154, 247, 145, 0, 185, 0)]

	FEUDAL_AGE = (255, 75, 255, 0, 0, 47, 0)
	CASTLE_AGE = (255, 255, 84, 0, 0, 35, 0)
	IMPERIAL_AGE = (255, 174, 255, 0, 0, 225, 0)

	ORIGINAL_TECH_TIMES = {
		(0, 245, 181, 0, 0, 0, 0)           : ["Cartography", 60], 
		(114, 84, 232, 0, 0, 0, 129)        : ["Coinage", 50],
		(82, 0, 0, 114, 0, 0, 114)          : ["Banking", 50],
		(103, 79, 79, 208, 82, 187, 77)     : ["Husbandry", 50],
	}

	EXPANSIONS_TECH_TIMES = {
		(0, 245, 181, 0, 0, 0, 0)           : ["Cartography", 1], 
		(114, 84, 232, 0, 0, 0, 129)        : ["Coinage", 70],
		(82, 0, 0, 114, 0, 0, 114)          : ["Banking", 70],
		(103, 79, 79, 208, 82, 187, 77)     : ["Husbandry", 40],
	}

	def __init__(self, civ, dataset):
		super(Technologies, self).__init__()
		# Load Technologies
		for building in Technologies.TECHNOLOGIES:
			self.update(Technologies.TECHNOLOGIES[building])
		# Check the dataset
		self.set_dataset(dataset)
		# Add allies
		self.allied_civs = [civ]
		self.civ = civ
		# Check bonuses
		self.__check_init_bonuses()
		# Researched technologies
		self.researched_techs = []

		

	def set_dataset(self, dataset):
		if dataset == "Expansions":
			for tech in Technologies.EXPANSIONS_TECH_TIMES:
				self[tech] = Technologies.EXPANSIONS_TECH_TIMES[tech]
		elif dataset == "Original":
			for tech in Technologies.ORIGINAL_TECH_TIMES:
				self[tech] = Technologies.ORIGINAL_TECH_TIMES[tech]


	def set_allied_civs(self, civs):
		# TODO  Parsing allies is not implemented in this project.
		self.allied_civs += civs
				
	def swap_lc_and_hussar(self):
		self[Technologies.LIGHT_CAVALRY] , self[Technologies.HUSSAR] = self[Technologies.HUSSAR] , self[Technologies.LIGHT_CAVALRY]


	def __check_init_bonuses(self):
		# Run it only during init
		# BUGALERT if the game was started with FULL TECH TREE, the bonuses are NOT applied!
		if "Britons" in self.allied_civs:
			BONUS = 1.20
			for tech in Technologies.TECHNOLOGIES["Archery Range"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Archery Range"][tech][1] / BONUS
		if "Celts" in self.allied_civs:
			BONUS = 1.20
			for tech in Technologies.TECHNOLOGIES["Siege Workshop"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Siege Workshop"][tech][1] / BONUS
		if "Huns" in self.allied_civs:
			BONUS = 1.20
			for tech in Technologies.TECHNOLOGIES["Stable"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Stable"][tech][1] / BONUS
		if "Goths" in self.allied_civs:
			BONUS = 1.20 
			for tech in Technologies.TECHNOLOGIES["Barrax"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Barrax"][tech][1] / BONUS
		if "Malians" in self.allied_civs:
			BONUS = 1.80
			for tech in Technologies.TECHNOLOGIES["University"]:
				self[tech][1] = Technologies.TECHNOLOGIES["University"][tech][1] / BONUS
		if self.civ == "Malay":
			BONUS = 1.80
			self[Technologies.FEUDAL_AGE][1] = Technologies.TECHNOLOGIES["Town Center"][Technologies.FEUDAL_AGE][1] / BONUS
			self[Technologies.CASTLE_AGE][1] = Technologies.TECHNOLOGIES["Town Center"][Technologies.CASTLE_AGE][1] / BONUS
			self[Technologies.IMPERIAL_AGE][1] = Technologies.TECHNOLOGIES["Town Center"][Technologies.IMPERIAL_AGE][1] / BONUS


	def check_research_bonuses(self, research):
		# BUG ALERT! Check also the research queue. And upgrade old times with the new times.
		# BUG ALERT! If game starts with default age: Feudal age. The feudal bonus will not apply to Persians's TCs.
		#            And so in post imperial Franks will not get the bonus.
		if self.civ == "Franks" and research == Technologies.UNIQUE_CASTLE_TECH:
			BONUS = 1.40 + (0.20 if "Huns" in allied_civs else 0.00)
			for tech in Technologies.TECHNOLOGIES["Stable"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Stable"][tech][1] / BONUS
		if self.civ == "Goths" and research == Technologies.UNIQUE_IMPERIAL_TECH:
			BONUS = 2.20
			for tech in Technologies.TECHNOLOGIES["Barrax"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Barrax"][tech][1] / BONUS
		if self.civ == "Berbers" and research == Technologies.UNIQUE_CASTLE_TECH: #BUGALERT the bonus is applied for all the allies if berber researched it
			BONUS = 1.25  
			for tech in Technologies.TECHNOLOGIES["Castle"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Castle"][tech][1] / BONUS
		if self.civ == "Persians" and research == Technologies.FEUDAL_AGE: 
			BONUS = 1.10
			for tech in Technologies.TECHNOLOGIES["Town Center"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Town Center"][tech][1] / BONUS
		if self.civ == "Persians" and research == Technologies.CASTLE_AGE:
			BONUS = 1.15
			for tech in Technologies.TECHNOLOGIES["Town Center"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Town Center"][tech][1] / BONUS
		if self.civ == "Persians" and research == Technologies.IMPERIAL_AGE:
			BONUS = 1.20
			for tech in Technologies.TECHNOLOGIES["Town Center"]:
				self[tech][1] = Technologies.TECHNOLOGIES["Town Center"][tech][1] / BONUS
		# FIXING buggy hussar
		if research == Technologies.LIGHT_CAVALRY:
			self.swap_lc_and_hussar()

	def __get_research_info(self, img, civ):
		raise("DO NOT CALL THIS FUNCTION")
		# Expansions has icon location bit on right
		expansions = ["Berbers", "Burmese", "Ethiopians", "Incas", "Indians", "Italians", "Khmer", "Magyars", "Malay", "Malians", "Portuguese", "Slavs", "Vietnamese"]
		offset = 3 if civ in expansions else 0
		# Check buggy civs. 
		offset = -1 if civ == "Teutons" else offset
		offset = -3 if civ == "Goths" else offset
		# Get the icon position and  convert it to grayscale
		icon = img[-90:-55, 449+offset:485+offset]
		icon = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
		# Look-up for the technology.
		result = (icon[10,10], icon[17,17], icon[20,20], icon[30,30], icon[30,5], icon[5,30], icon[25, 3])
		print(result)
		return result

