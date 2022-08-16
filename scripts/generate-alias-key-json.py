#! python
#%%
import json
import yaml
import glob
import itertools

# A is implicitly aliased to itself
aliases = {'A': 'A'}

# Iterate through all lineage definition files
for yaml_file in glob.glob('lineages/*.yml'):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    if 'alias' in yaml_data:
        # Alias key json maps from alias to completely unaliased
        aliases[yaml_data['alias']] = yaml_data['unaliased_name']

# Write to json file
with open('auto-generated/alias_key.json', 'w') as outfile:
    aliases["A"] = "" # Empty string for consistency with pango-designation
    json.dump(aliases, outfile, sort_keys=True, indent=2)
    aliases["A"] = "A" # Restore back for rest of script

# %%
# Validate unaliased names
validation_failed = False
for yaml_file in glob.glob('lineages/*.yml'):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    # Unalias (aliased) name
    aliased_name = yaml_data['name']
    split_name = aliased_name.split('.')
    if len(split_name) > 1:
        aliased_prefix: list = aliased_name.split('.')[0]
        aliased_suffix: list = aliased_name.split('.')[1:]
    else:
        aliased_prefix: list = aliased_name
        aliased_suffix: list = []
    

    try:
        unaliased_name = [aliases[aliased_prefix]]
        unaliased_name.extend(aliased_suffix)
        unaliased_name = '.'.join(unaliased_name)
        if yaml_data['unaliased_name'] != unaliased_name:
            print(f"Aliasing validation failed for {yaml_file}")
            print(f"unaliased_name:{yaml_data['unaliased_name']} != deduced_unaliased:{unaliased_name}")
            validation_failed = True
    except KeyError:
        print(f"Aliasing validation failed for {yaml_file}")
        print(f"Name contains alias {aliased_prefix} that is not defined as alias anywhere")
        validation_failed = True

#%%
# Validate parents
validation_failed = False
for yaml_file in glob.glob('lineages/*.yml'):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    parent = yaml_data['parent']
    # Alias of (unaliased name's parent)
    # Unaliased parent name
    unaliased_name = yaml_data['unaliased_name']
    unaliased_name_split = unaliased_name.split('.')
    if len(unaliased_name_split) <= 1:
        if parent != 'None':
            print(f"Parent validation failed for {yaml_file}")
            print(f"parent:{parent} != None")
            validation_failed = True
    else:
        unaliased_parent_split = unaliased_name_split[0:-1]
        unaliased_parent_from_unaliased_name = '.'.join(unaliased_parent_split)

        parent_split = parent.split('.')
        parent_unaliased_split = itertools.chain.from_iterable([aliases[parent_split[0]].split('.'), parent_split[1:]])
        parent_unaliased = '.'.join(parent_unaliased_split)
        if parent_unaliased != unaliased_parent_from_unaliased_name:
            print(f"Parent validation failed for {yaml_file}")
            print(f"parent:{parent} != deduced_parent:{unaliased_parent_from_unaliased_name}")
            validation_failed = True

exit(1 if validation_failed else 0)