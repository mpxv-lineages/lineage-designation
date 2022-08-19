# Monkeypox virus phylogenetic lineage designation

This repository contains updates and details about monkeypox virus lineage designations.
These lineages are meant to assist genomic epidemiology of monkeypox in humans and provide a fine-grained systematic nomenclature to refer to different circulating lineages.
They do not imply any phenotypic differences.
These lineages only apply to recent human cases and are distinct from broader clades of monkeypox viruses circulating in the animal reservoir I, IIa, and IIb, see [Happi et al](https://virological.org/t/urgent-need-for-a-non-discriminatory-and-non-stigmatizing-nomenclature-for-monkeypox-virus/853) and the recent [announcement by the WHO](https://worldhealthorganization.cmail20.com/t/ViewEmail/d/422BD62D623B6A3D2540EF23F30FEDED/F75AF81C90108C72B4B1B1F623478121?alternativeLink=False)).
The recent outbreak among humans originated from clade IIb.

## [Lineage summary](auto-generated/lineages.md)

## Designation of lineages
New lineages are designated as more cases are sequenced and the outbreak gets more diverse.
The criteria for lineage designation will evolve as the outbreak continues.
Currently, we aim to designate a new lineage if it

 - has spread internationally
 - has at least 1 mutation above its parent
 - contains at least 15 sequences or plausibly represents undersampled diversity
 - has a clear common phylogenetic structure (no uncertainty about possibly being designated as 2 lineages instead of 1)
 - has at least one freely available high quality reference sequence

Each new lineage is defined by a `yaml` file according the [schema](schemas/single_lineage/lineage_schema_1-0-0.yml).
For lineage [B.1](lineages/B.1.yml), for example, this looks like this
```
# yaml-language-server: $schema=../schemas/single_lineage/lineage_schema_1-0-0.yml
name: B.1
unaliased_name: A.1.1.1
parent: A.1.1
designation_date: "2022-06-10"
defining_snps:
  - pos: 77383
    nucleotide: A
reference_sequences:
  - source: genbank
    accession: ON563414
    isolate: MPXV_USA_2022_MA001
```

An automatically generated `json` file which merges these `yaml` designations can be found [here](auto-generated/lineages.json), and a file with a key of the alias names can be found [here](auto-generated/alias_key.json).
A human readable summary of all designated lineages can be found [here](auto-generated/lineages.md) .

You can find markdown documents describing the rationale of lineage designation (including which lineages and why) in the "designation_records" folder.

 - [2022-08-08: B.1.1-B.1.5](designation_records/B.1.1-B.1.5_2022-08-08.md)

### Lineage proposals
To propose additional lineages, open a github issue in this repository.

