#! python
#%%
import json
import yaml
import glob
import datetime

VERSION = ("1", "0", "0")

result = {
    "$schema": f"https://raw.githubusercontent.com/mpxv-lineages/lineage-designation/master/schemas/all_lineages/lineages_schema-{'-'.join(VERSION)}.yml#",
    "schemaVersion": ".".join(VERSION),
    "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds"),
}

lineages = []
# Iterate through all lineage definition files
for yaml_file in sorted(glob.glob('lineages/*.yml')):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    lineages.append(yaml_data)

result['lineages'] = lineages

# Write to json file
with open('auto-generated/lineages.json', 'w') as outfile:
    json.dump(result, outfile, sort_keys=True, indent=2)
    outfile.write('\n')
