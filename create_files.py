import json

with open('data/races.json') as json_file_races:
	all_races_data = json.load(json_file_races)
	races_data = []
	for entry in all_races_data['race']:
		if entry['source'] == 'PHB':
			races_data.append(entry)

with open('phb_data/races.json', 'w') as f:
  json.dump(races_data, f, indent=2)


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

for name, file_name in phb_class_index.items():
	with open(f"data/class/{file_name}") as json_file_class:
		that_class = json.load(json_file_class)
		class_data[name] = that_class

with open('phb_data/classes.json', 'w') as f:
  json.dump(class_data, f, indent=2)