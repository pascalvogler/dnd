import json
from os import system, name 
from time import sleep
from collections import Counter

# define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_race_dict(race_name):
	for item in races:
		if item['name'] == race_name:
			return item

with open('phb_data/classes.json') as class_raw:
	classes = json.load(class_raw)

with open('phb_data/races.json') as race_raw:
	races = json.load(race_raw)

class character:
	def __init__(self,race,subrace,class_,name, ability_scores):
		self.race = race
		self.subrace = subrace
		self.class_ = class_
		self.name = name
		self.specific_race_dict = get_race_dict(race)
		self.specific_subrace_dict = None
		self.ability_score_bonus = None
		self.calc_ability_score_bonus()
		self.ability_scores = ability_scores


		

	def calc_ability_score_bonus(self):
		if self.subrace == None:
			self.ability_score_bonus = self.specific_race_dict['ability'][0]
		else:
			for subrace in self.specific_race_dict['subraces']:
				if subrace['name'] == self.subrace:
					self.specific_subrace_dict = subrace

			subrace_bonus = self.specific_subrace_dict['ability']
			self.ability_score_bonus = dict(Counter(self.specific_race_dict['ability'][0]) + Counter(self.specific_subrace_dict['ability'][0]))
			

	@classmethod
	def create(cls):
		clear()
		print('---')
		print("LET'S PLAY DUNGEONS AND DRAGONS!!!")
		print('---')
		#sleep(1)
		print('No worries, I will guide you through the creation process of your character.')
		print('---')
		#sleep(1)
		print('Which class do you want to play? The following are possible:')
		print('---')
		for item in classes:
			print(item)
		print('---')
		#CLASS
		class_input = input('Type in the class you want to play: ')
		if class_input.lower() not in [class_ for class_, class_info in classes.items()]:
			print('Think again adventurer... this is not a valid class. Take one from the list above.')
		while class_input.lower() not in [class_ for class_, class_info in classes.items()]:
			class_input = input('Type in the class you want to play: ')
			if class_input.lower() in [class_ for class_, class_info in classes.items()]:
				break
			print('Think again adventurer... this is not a valid class. Take one from the list above.')
		class_input = class_input.lower().title()
		print(f"Nice, so a {class_input.lower()} it is.")
		#sleep(1)
		print('---')
		print('Now you have to select a race. Check the possibilities:')
		for x in [name['name'] for name in races]:
			print(x)
		print('---')
		#RACE
		race_input = input('Type in the race you want to play: ')
		if race_input.lower() not in [name['name'].lower() for name in races]:
			print(f"{race_input}??? I have never heard of that people. Can you try again?")
		while race_input.lower() not in [name['name'].lower() for name in races]:
			race_input = input('Type in the race you want to play: ')
			if race_input.lower() in [name['name'].lower() for name in races]:
				break
			print(f"{race_input}??? I have never heard of that people. Can you try again?")
		race_input = race_input.lower().title()
		print('---')
		#SUBRACE
		subrace_count = 0
		subraces_name_list = []
		for race in races:
			if race['name'].lower() == race_input.lower():
				if race.get('subraces') is not None:
					for subrace in race['subraces']:
						if subrace.get('source') is None and subrace.get('name') is not None:
							#print(subrace.get('name','not available'))
							subrace_count += 1
							subraces_name_list.append(subrace.get('name').lower())
		if subrace_count == 0:	
			print(f"Hurray, so you will be playing a {race_input.lower()}.")	
			subrace_input = None		
		else:
			print(f"Understood. Please specify which kind of {race_input.lower()} you are. Choose from the following:")
			for _ in subraces_name_list:
				print(_)
			print('---')
			subrace_input = input('Tell me your subrace: ')
			if subrace_input.lower() not in subraces_name_list:
				print(f"{subrace_input} is not a valid subrace. Be honest...")
			while subrace_input.lower() not in subraces_name_list:
				subrace_input = input('Tell me your subrace: ')
				if subrace_input.lower() in subraces_name_list:
					break
				print(f"{subrace_input} is not a valid subrace. Be honest...")
			subrace_input = subrace_input.lower().title()
		#NAME
		print(f"Alright {race_input}, how you you call yourself?")
		name_input = input("Tell me your full name: ")
		name_input = name_input.lower().title()
		#ABILITY SCORE
		print('---')
		print('Alright, time to distribute your ability score points.')
		score_list_value = [15,14,13,12,10,8]
		score_list_dict = {
			'str':0,
			'dex':0,
			'con':0,
			'int':0,
			'wis':0,
			'cha':0
		}
		print('you can distribute 15,14,13,12,10,8 to your ability scores. You have the following:')
		print('---')
		print('Strength')
		print('Dexterity')
		print('Constitution')
		print('Intelligence')
		print('Wisdom')
		print('Charisma')
		print('---')
		for ability_name, score in score_list_dict.items():
			ability_score_input = input(f"Chose your {ability_name} score: ")
			#score_list_dict[ability_name] = int(input(f"Chose your {ability_name} score: "))
			#print(f"{int(score_list_dict[ability_name])} - {type(int(score_list_dict[ability_name]))}")
			if ability_score_input not in [str(x) for x in score_list_value]:
				#score_list_dict[ability_name] = 0
				print(f"Oops1, that is not possible. Choose from {score_list_value}.")
				#score_list_dict[ability_name] = int(input(f"Chose your {ability_name} score: "))
				ability_score_input = input(f"Chose your {ability_name} score: ")
			while ability_score_input not in [str(x) for x in score_list_value]:
				#score_list_dict[ability_name] = 0
				print(f"Oops2, that is not possible. Choose from {score_list_value}.")
				#score_list_dict[ability_name] = int(input(f"Chose your {ability_name} score: "))
				ability_score_input = input(f"Chose your {ability_name} score: ")
				if ability_score_input in [str(x) for x in score_list_value]:
					score_list_value.remove(int(ability_score_input))
					score_list_dict[ability_name] = int(ability_score_input)
					break
			score_list_value.remove(int(ability_score_input))
			score_list_dict[ability_name] = int(ability_score_input)

		print(score_list_dict)
		
		#CREATION
		char = cls(race=race_input,subrace=subrace_input,class_=class_input,name=name_input,ability_scores=score_list_dict)
		return char




	def __str__(self):
		if self.subrace == None:
			subrace_string = ''
		else:
			subrace_string = f"{self.subrace} "
		return f"A {subrace_string}{self.race} named {self.name}."


char1 = character.create()

print(char1)