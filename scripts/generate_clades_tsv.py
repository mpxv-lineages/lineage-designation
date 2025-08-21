#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path

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


def generate_clades_tsv(lineages_dir, output_file):
    """Generate clades.tsv file from lineage YAML files."""
    lineages = load_lineage_files(lineages_dir)
    sorted_lineages, parents = build_hierarchy(lineages)

    with open(output_file, "w") as f:
        # Write header
        f.write(
            "# Nuc coordinates valid for reference NC_063383 (MPXV-M5312_HM12_Rivers)\n"
        )
        f.write("clade\tgene\tsite\talt\n")

        # Add outgroup and root clade entries based on the example
        f.write("outgroup\tnuc\t54013\tG\n")
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


def main():
    script_dir = Path(__file__).parent.parent
    lineages_dir = script_dir / "lineages"
    output_file = script_dir / "auto-generated" / "clades_IIb.tsv"

    if not lineages_dir.exists():
        print(f"Error: Lineages directory not found at {lineages_dir}")
        return 1

    generate_clades_tsv(lineages_dir, output_file)
    print(f"Generated clades.tsv at {output_file}")
    return 0


if __name__ == "__main__":
    exit(main())
