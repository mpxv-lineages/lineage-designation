#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
import json
import urllib.request
import urllib.parse

import yaml


def load_lineage_files(lineages_dir):
    """Load all lineage YAML files from the directory."""
    lineages = {}
    lineages_path = Path(lineages_dir)

    for yaml_file in lineages_path.glob("*.yml"):
        if yaml_file.name.startswith("lineage_schema"):
            continue

        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)
            lineages[data["name"]] = data

    return lineages


def get_pathoplexus_accessions(insdc_accessions):
    """Query LAPIS API to get pathoplexus accessions for INSDC accessions."""
    if not insdc_accessions:
        return {}
    
    # Build query for multiple accessions
    query_parts = [f"insdcAccessionBase={acc}" for acc in insdc_accessions]
    advanced_query = " OR ".join(query_parts)
    
    # URL encode the query
    encoded_query = urllib.parse.quote(advanced_query)
    url = f"https://lapis.pathoplexus.org/mpox/sample/details?advancedQuery={encoded_query}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        
        # Build mapping from INSDC to pathoplexus accession
        insdc_to_pathoplexus = {}
        for entry in data.get("data", []):
            insdc_base = entry.get("insdcAccessionBase")
            pathoplexus_acc = entry.get("accession")
            if insdc_base and pathoplexus_acc:
                insdc_to_pathoplexus[insdc_base] = pathoplexus_acc
        
        return insdc_to_pathoplexus
    
    except Exception as e:
        print(f"Warning: Could not fetch pathoplexus accessions: {e}")
        return {}


def lineage_sort_key(lineage_name):
    """Generate a sort key for lineage names with numerical sorting of parts."""
    parts = lineage_name.split(".")
    key_parts = []

    for part in parts:
        # Extract letter and number parts
        letters = ""
        numbers = ""
        for char in part:
            if char.isalpha():
                letters += char
            elif char.isdigit():
                numbers += char

        # Create sort key: letters first, then numbers as integers
        if numbers:
            key_parts.append((letters, int(numbers)))
        else:
            key_parts.append((letters, 0))

    return key_parts


def build_hierarchy(lineages):
    """Build parent-child relationships and sort lineages topologically."""
    children = defaultdict(list)
    parents = {}

    for name, data in lineages.items():
        parent = data.get("parent")
        if parent and parent != "None":
            children[parent].append(name)
            parents[name] = parent
        else:
            parents[name] = None

    # Sort children lists numerically for each parent
    for parent in children:
        children[parent].sort(key=lineage_sort_key)

    # Topological sort to ensure parents come before children
    sorted_lineages = []
    visited = set()

    def visit(lineage):
        if lineage in visited:
            return
        visited.add(lineage)

        parent = parents.get(lineage)
        if parent and parent != "None":
            visit(parent)

        sorted_lineages.append(lineage)

        # Visit children in numerical order
        for child in children[lineage]:
            visit(child)

    # Start with root lineages (those with no parents) in numerical order
    root_lineages = [
        name
        for name in lineages
        if parents.get(name) is None or parents.get(name) == "None"
    ]
    root_lineages.sort(key=lineage_sort_key)

    for root in root_lineages:
        visit(root)

    return sorted_lineages, parents


def generate_output_files(lineages_dir, clades_output_file, color_ordering_output_file, lineage_accessions_output_file):
    """Generate clades.tsv, color_ordering.tsv, and lineage_accessions.tsv files from lineage YAML files."""
    lineages = load_lineage_files(lineages_dir)
    sorted_lineages, parents = build_hierarchy(lineages)

    with open(clades_output_file, "w") as f:
        # Write header
        f.write(
            "# Nuc coordinates valid for reference NC_063383 (MPXV-M5312_HM12_Rivers)\n"
        )
        f.write("clade\tgene\tsite\talt\n")

        # Add outgroup and root clade entries based on the example
        f.write("unassigned\tnuc\t54013\tG\n")
        f.write("\nclade IIb\tnuc\t48148\tC\n")

        # Process each lineage in topological order
        for lineage_name in sorted_lineages:
            lineage_data = lineages[lineage_name]
            parent = parents.get(lineage_name)

            # Write parent relationship (if not root)
            if parent and parent != "None":
                f.write(f"\n{lineage_name}\tclade\t{parent}\n")
            elif lineage_name == "A":
                # Special case for lineage A which descends from clade IIb
                f.write(f"\n{lineage_name}\tclade\tclade IIb\n")

            # Write defining SNPs
            if "defining_snps" in lineage_data:
                for snp in lineage_data["defining_snps"]:
                    pos = snp["pos"]
                    nucleotide = snp["nucleotide"]
                    f.write(f"{lineage_name}\tnuc\t{pos}\t{nucleotide}\n")

    with open(color_ordering_output_file, "w") as f:
        for lineage_name in sorted_lineages:
            f.write(f"lineage\t{lineage_name}\n")

    # Collect all INSDC accessions first for batch querying
    all_insdc_accessions = set()
    for lineage_name in sorted_lineages:
        lineage_data = lineages[lineage_name]
        if "reference_sequences" in lineage_data:
            for ref_seq in lineage_data["reference_sequences"]:
                accession = ref_seq.get("accession", "")
                if accession:
                    all_insdc_accessions.add(accession)
    
    # Get pathoplexus accessions mapping
    print("Fetching pathoplexus accessions...")
    insdc_to_pathoplexus = get_pathoplexus_accessions(list(all_insdc_accessions))

    with open(lineage_accessions_output_file, "w") as f:
        # Write header
        f.write("lineage\taccession\tstrain\tpathoplexus_accession\n")
        
        # Process each lineage in sorted order
        for lineage_name in sorted_lineages:
            lineage_data = lineages[lineage_name]
            
            # Get reference sequences
            if "reference_sequences" in lineage_data:
                for ref_seq in lineage_data["reference_sequences"]:
                    accession = ref_seq.get("accession", "")
                    strain = ref_seq.get("isolate", "")
                    
                    # Only include entries with accessions (INSDC accessions)
                    if accession:
                        pathoplexus_acc = insdc_to_pathoplexus.get(accession, "")
                        f.write(f"{lineage_name}\t{accession}\t{strain}\t{pathoplexus_acc}\n")


def main():
    script_dir = Path(__file__).parent.parent
    lineages_dir = script_dir / "lineages"
    autogen_dir = script_dir / "auto-generated"
    clades_output_file = autogen_dir / "clades_IIb.tsv"
    color_ordering_output_file = autogen_dir / "color_ordering.tsv"
    lineage_accessions_output_file = autogen_dir / "lineage_accessions.tsv"

    if not lineages_dir.exists():
        print(f"Error: Lineages directory not found at {lineages_dir}")
        return 1

    generate_output_files(lineages_dir, clades_output_file, color_ordering_output_file, lineage_accessions_output_file)
    print(f"Generated clades.tsv at {clades_output_file}")
    print(f"Generated color_ordering.tsv at {color_ordering_output_file}")
    print(f"Generated lineage_accessions.tsv at {lineage_accessions_output_file}")
    return 0


if __name__ == "__main__":
    exit(main())