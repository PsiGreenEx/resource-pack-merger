import os
import json
from itertools import groupby

pack1_name = input("What is the folder name for the first pack? ")
pack2_name = input("What is the folder name for the second pack? ")
new_pack_name = input("What should the folder name for the output pack be? ")

pack1_path = "./packs/" + pack1_name + "/assets/minecraft/models/item"
pack2_path = "./packs/" + pack2_name + "/assets/minecraft/models/item"
new_pack_path = "./packs/" + new_pack_name + "/assets/minecraft/models/item"
new_pack_path_array = ["packs",new_pack_name,"assets","minecraft","models","item"]

def create_new_pack(path_array):
    path_string = "./"
    for folder in path_array:
        path_string += folder + "/"
        if not os.path.exists(path_string):
            os.mkdir(path_string)

# Make new folder for new pack.
create_new_pack(new_pack_path_array)

# Grab the set of item models in the packs
pack1_model_set = set(os.listdir(pack1_path))
pack2_model_set = set(os.listdir(pack2_path))

# Make a set of intersecting models
conflicting_models_set = pack1_model_set.intersection(pack2_model_set)

for model_file_name in conflicting_models_set:
    with open(pack1_path + "/" + model_file_name) as p1_model_file:
        p1_model_file_dict = json.load(p1_model_file)

    with open(pack2_path + "/" + model_file_name) as p2_model_file:
        p2_model_file_dict = json.load(p2_model_file)
    
    p1_model_overrides = p1_model_file_dict["overrides"]
    p2_model_overrides = p2_model_file_dict["overrides"]

    combined_model_overrides = p1_model_overrides + p2_model_overrides

    # Remove Duplicate CMD Overrides
    seen = set()
    unsorted_model_overrides = []

    for override in combined_model_overrides:
        custom_model_data = override["predicate"]["custom_model_data"]
        if custom_model_data in seen:
            continue
        
        unsorted_model_overrides.append(override)
        seen.add(custom_model_data)
    
    # Sort Overrides by CMD
    new_model_override = sorted(unsorted_model_overrides, key = lambda k: k["predicate"]["custom_model_data"])

    # Create new dictionary
    new_model_file_dict = p1_model_file_dict
    new_model_file_dict["overrides"] = new_model_override
    print(new_model_file_dict)

    # Create new file
    with open(new_pack_path + "/" + model_file_name, "w+") as new_model_file:
        json.dump(new_model_file_dict, new_model_file)


print("Pack Successfully Generated.")
print("Place the {} pack in your resource pack folder and put it at the top of your packs.".format(new_pack_name))
input("Press Enter to close this program...")
