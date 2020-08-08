import json


with open('data/races.json') as json_file_races:
	all_races_data = json.load(json_file_races)
	races_data = []
	for entry in all_races_data['race']:
		if entry['source'] == 'PHB':
			races_data.append(entry)

#writes new file in own folder: as list
with open('phb_data/races.json', 'w') as f:
  json.dump(races_data, f, indent=2)

#defines all phb classes:
phb_class_index = {
	"barbarian": "class-barbarian.json",
	"bard": "class-bard.json",
	"cleric": "class-cleric.json",
	"druid": "class-druid.json",
	"fighter": "class-fighter.json",
	"monk": "class-monk.json",
	"paladin": "class-paladin.json",
	"ranger": "class-ranger.json",
	"rogue": "class-rogue.json",
	"sorcerer": "class-sorcerer.json",
	"warlock": "class-warlock.json",
	"wizard": "class-wizard.json"
}

class_data = {}

#loopt über die phb klassen, öffnet das jeweilige file und fügt die klasse class_data hinzu, als dict
for name, file_name in phb_class_index.items():
	with open(f"data/class/{file_name}") as json_file_class:
		that_class = json.load(json_file_class)
		class_data[name] = that_class

#writes new file in own foder as dict
with open('phb_data/classes.json', 'w') as f:
  json.dump(class_data, f, indent=2)

#loopt über backgrounds und fügt nur die PHB backgrounds hinzu
with open('data/backgrounds.json') as json_file_backgrounds:
	all_backgrounds_data = json.load(json_file_backgrounds)
	backgrounds_data = []
	for entry in all_backgrounds_data['background']:
		if entry['source'] == 'PHB':
			backgrounds_data.append(entry)

with open('phb_data/backgrounds.json','w') as f:
	json.dump(backgrounds_data, f, indent=2)
