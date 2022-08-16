#! python
#%%
import json
import yaml
import glob

lineages = []
# Iterate through all lineage definition files
for yaml_file in sorted(glob.glob('lineages/*.yml')):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    lineages.append(yaml_data)

# Write to json file
with open('auto-generated/lineages.json', 'w') as outfile:
    json.dump(lineages, outfile, sort_keys=True, indent=2)
