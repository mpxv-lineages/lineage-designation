#! python
#%%
import json
import yaml
import glob
import datetime

def generate_lineage_md(lineage):
    lines = []
    lines.append(f"## {lineage['name']}")
    lines.append(f" * parent: [{lineage['parent']}]({lineage['parent']})")
    snp_str = ','.join(f"{x['pos']}{x['nucleotide']}" for x in lineage['defining_snps'])
    lines.append(f" * defining SNPs: {snp_str}")
    ref_seqs = [f"[{x.get('isolate', x['accession'])}](https://www.ncbi.nlm.nih.gov/nuccore/{x['accession']})" for x in lineage['reference_sequences'] if x['source']=='genbank']
    if len(ref_seqs)==1:
        lines.append(f" * reference sequences: {ref_seqs[0]}")
    else:
        lines.append(f" * reference sequences:")
        for r in ref_seqs:
            lines.append(f"   - {r}")

    return '\n'.join(lines) + '\n'

lineages = []
# Iterate through all lineage definition files
for yaml_file in sorted(glob.glob('lineages/*.yml')):
    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    lineages.append(yaml_data)

lineages.sort(key=lambda x:x['name'])

# Write to json file
with open('auto-generated/lineages.md', 'w') as outfile:
    outfile.write("#Summary of designated lineages\n")

    for lineage in lineages:
        outfile.write(generate_lineage_md(lineage) + '\n')

