import json
from os import system, name 
from time import sleep
from collections import Counter
import math
import random
import re

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

def get_class_dict(class_name):
	for key,value in classes.items():
		if key.lower() == class_name.lower():
			return value

def get_back_ground_dict(background_name):
	for background in backgrounds:
		if background['name'].lower() == background_name.lower():
			return background

def get_modifier_string(number):
	calculated_trunc_int = math.trunc((number - 10)/2)
	if calculated_trunc_int > -1:
		return f"+{calculated_trunc_int}"
	else:
		return f"{calculated_trunc_int}"

def get_nice_stat_name(stat_name):
	nice_dict = {
		'str': 'Strength',
		'dex': 'Dexterity',
		'con': 'Constitution',
		'int': 'Intelligence',
		'wis': 'Wisdom',
		'cha': 'Charisma'
	}
	return nice_dict.get(stat_name)

with open('phb_data/classes.json') as class_raw:
	classes = json.load(class_raw)

with open('phb_data/races.json') as race_raw:
	races = json.load(race_raw)

with open('phb_data/backgrounds.json') as backgrounds_raw:
	backgrounds = json.load(backgrounds_raw)


class character:
	def __init__(self,race,subrace,class_,name, ability_scores,proficiency_list,background, alignment):
		self.race = race
		self.subrace = subrace
		self.class_ = class_
		self.name = name
		self.specific_race_dict = get_race_dict(race)
		self.specific_subrace_dict = None
		self.specific_class_dict = get_class_dict(class_)
		self.ability_score_bonus = None
		self.calc_ability_score_bonus()
		self.ability_scores = ability_scores
		self.update_ability_scores(self.ability_score_bonus)
		self.proficiency_list = proficiency_list
		self.specific_background_dict = get_back_ground_dict(background)
		self.background = background
		self.alignment = alignment

		
	#ABILITY SCORE BONUS CALCULATION

	def calc_ability_score_bonus(self):
		if self.subrace == None:
			self.ability_score_bonus = self.specific_race_dict['ability'][0]
		else:
			for subrace in self.specific_race_dict['subraces']:
				if subrace['name'] == self.subrace:
					self.specific_subrace_dict = subrace
			subrace_bonus = self.specific_subrace_dict['ability']
			self.ability_score_bonus = dict(Counter(self.specific_race_dict['ability'][0]) + Counter(self.specific_subrace_dict['ability'][0]))
	
	def update_ability_scores(self,as_dict):
		self.ability_scores = dict(Counter(self.ability_scores) + Counter(self.ability_score_bonus))

	def get_basic_ability_modifiers(self):
		for key,value in self.ability_scores.items():
			print(f"{get_nice_stat_name(key)}: {get_modifier_string(self.ability_scores[key])} ({self.ability_scores[key]})")


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
		input("Press Enter to continue...")
		clear()
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
		sleep(2)
		clear()
		#print('---')
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
		print(f"a proud {race_input.lower()}. What a good choice.")
		sleep(2)
		clear()
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
			print(f"Yeah, so you will be playing a {race_input.lower()}.")	
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
			print(f"Yeah, so you will be playing a {subrace_input.lower()} {race_input.lower()}.")
		sleep(2)
		clear()
		#NAME

		print(f"Alright {race_input}, how you you call yourself?")
		name_input = input("Tell me your full name: ")
		name_input = name_input.lower().title()
		sleep(1)
		clear()
		print(f"{name_input.lower().title()}...")
		sleep(2)
		clear()
		print("What a dumb fucking name. But ok, your game.")
		sleep(2)
		clear()
		#ABILITY SCORE
		

		print(f'Alright dear {name_input.lower().title()}, time to distribute your ability score points.')
		print('')
		print('You can choose now to either distribute a preset array (15,14,13,12,10,8)')
		sleep(1)
		print('')
		print('Ooooor you can roll it out, much more fun, I promise (or not).')
		as_method_input = input('Type "random" or "preset": ')
		if as_method_input == 'random':
			clear()
			print("Alright let us see how you roll:")
			print("")
			sleep(2)
			score_list_value = []
			for i in range(6):
				as_values = []
				for x in range(4):
					as_values.append(random.randint(1,6))
				smallest_value = min(as_values)
				#print(f"i rolled: {as_values}")
				#print(f"smalles value is {smallest_value}")
				as_values.remove(smallest_value)
				if sum(as_values) > 14:
					print(f"{i+1}. value: {sum(as_values)}  (good shot bro)")
				elif sum(as_values) < 8:
					print(f"{i+1}. value: {sum(as_values)}  (hahahaha you suck)")
				else:
					print(f"{i+1}. value: {sum(as_values)}")
				sleep(2)
				score_list_value.append(sum(as_values))
			score_list_value.sort(reverse=True)
		elif as_method_input == 'preset':
			clear()
			score_list_value = [15,14,13,12,10,8]

		score_list_dict = {
			'str':0,
			'dex':0,
			'con':0,
			'int':0,
			'wis':0,
			'cha':0
		}
		sleep(1)
		clear()
		print(f"So now you can distribute {score_list_value[0]},{score_list_value[1]},{score_list_value[2]},{score_list_value[3]},{score_list_value[4]},{score_list_value[5]} to your ability scores. You have the following:")
		print('---')
		print('Strength')
		print('Dexterity')
		print('Constitution')
		print('Intelligence')
		print('Wisdom')
		print('Charisma')
		print('---')
		for ability_name, score in score_list_dict.items():
			ability_score_input = input(f"Chose your {get_nice_stat_name(ability_name)} score: ")
			#if not found
			if ability_score_input not in [str(x) for x in score_list_value]:
				print(f"Oops first if, that is not possible. Choose from {score_list_value}.")
				ability_score_input = input(f"Chose your {ability_name} score: ")
			while ability_score_input not in [str(x) for x in score_list_value]:
				print(f"Oops while, that is not possible. Choose from {score_list_value}.")
				ability_score_input = input(f"Chose your {ability_name} score: ")
				if ability_score_input in [str(x) for x in score_list_value]:
					print(f"FOUND - removing {ability_score_input}")
					score_list_value.remove(int(ability_score_input))
					print(f"NEW LIST: {score_list_value}")
					score_list_dict[ability_name] = int(ability_score_input)
					break
			#if found in the first place
			else:				
				score_list_value.remove(int(ability_score_input))
				score_list_dict[ability_name] = int(ability_score_input)

		class_dict = get_class_dict(class_input.lower())
		prof_list = class_dict['class'][0]['proficiency']
		sleep(1)
		clear()
		#BACKGROUND

		print('Aaaight, choose your background from one of the following:')
		print('---')
		for background in backgrounds:
			if '_copy' not in background:
				print(f"{background['name']} - (Page: {background['page']})")
		print('---')
		background_input = input('Your background choice: ')
		background_check_count = 0
		for background in backgrounds:
			#print(f"BACKGROUND FROM FILE: {background['name']}")
			if background_input.lower() == background['name'].lower():
				print(f"{background_input}s usually are proficient in {background['entries'][0]['items'][0]['entry']}")
				background_prof_list = background['entries'][0]['items'][0]['entry'].split(',')
				for background_prof in background_prof_list:
					background_prof_nice = re.search('\{@skill (.*)\}', background_prof, re.IGNORECASE)
					print(f"Nice: {background_prof_nice.group(1)}")
					prof_list.append(background_prof_nice.group(1).lower())
				background_check_count += 1
		if background_check_count == 0:
			raise Exception("Background not found. Type more accurately.")
		
		
		print('')
		sleep(1)
		clear()
		# CLASS PROFICIENCIES

		class_prof = class_dict['class'][0]['startingProficiencies']['skills'][0]['choose']
		print(f"{class_input}s typically choose {class_prof['count']} from the following proficiencies:")
		print('Dont take the ones from your background obviously...')
		for prof in class_dict['class'][0]['startingProficiencies']['skills'][0]['choose']['from']:
			if prof in prof_list:
				print(f"{prof} (you already have that!)")
			else:
				print(prof)
		
		for i in range(class_prof['count']):
			prof_list.append(input(f'your {i+1}. choice: '))
		sleep(1)
		clear()
		# ALIGNMENT

		print(f"Ok, time to choose your allginment, {name_input}.")
		print("From those options below, where do you see yourself the most?")
		print("Good")
		print("Neutral")
		print("Evil")
		alignment_x_input = input("Your answer: ")

		print(f"Uuuh... {alignment_x_input} it is then.")
		print("Now how does your character usually acts?")
		print("Lawful")
		print("Neutral")
		print("Chaotic")
		alignment_y_input = input("Your answer: ")

		alignment_input = f"{alignment_y_input} {alignment_x_input}"
		sleep(1)
		clear()
		#CREATION
		char = cls(
			race=race_input,
			subrace=subrace_input,
			class_=class_input,
			name=name_input,
			ability_scores=score_list_dict,
			proficiency_list=prof_list,
			background=background_input,
			alignment=alignment_input
			)
		return char

	def __str__(self):
		if self.subrace == None:
			subrace_string = ''
		else:
			subrace_string = f"{self.subrace} "
		return f"A {subrace_string}{self.race} {self.class_} named {self.name}.\nBackground: {self.background}\nAlignment: {self.alignment}"


char1 = character.create()

print('-----')
print('-----')
print('-----')
print(char1)
print('')
#print(f"ability score set: {char1.ability_scores}")
print(f"proficiency list: {char1.proficiency_list}")
print('')
char1.get_basic_ability_modifiers()