# Monkeypox virus phylogenetic lineage designation

This repository has information, updates, and details about monkeypox virus lineage designations.
These lineages are meant to help assist genomic epidemiology of monkeypox in humans and provide a fine-grained systematic nomenclature to refer to different circulating lineages.
These lineage only apply to recent human cases and are distinct from broader clades of monkeypox viruses circulating in the animal reservoir I, IIa, and IIb, see [Happi et al](https://virological.org/t/urgent-need-for-a-non-discriminatory-and-non-stigmatizing-nomenclature-for-monkeypox-virus/853) and the recent [announcement by the WHO](https://worldhealthorganization.cmail20.com/t/ViewEmail/d/422BD62D623B6A3D2540EF23F30FEDED/F75AF81C90108C72B4B1B1F623478121?alternativeLink=False)).
The recent outbreak among humans originated from clade IIb.

## Designation of lineages
New lineages are designated as more cases are sequenced and the outbreak gets more diverse.
The criteria for lineage designation will evolve as the outbreak continues.
Currently, we aim to designate a new lineage if

 - has spread internationally
 - contains at least 15 sequences or plausibly represent undersampled diversity
 - clear common phylogenetic structure (no uncertainty about possibly being designated as 2 lineages instead of 1)
 - at least one freely available high quality reference sequence

Each new lineage is defined by a `yaml` file according the [schema](schemas/lineage_schema.yml).
For lineage [B.1](lineages/B.1.yml), for example, this looks like this
```
# yaml-language-server: $schema=../schemas/lineage_schema.yml
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

You can find markdown documents describing the rational of lineage designation (including which lineages and why) in the "designation_records" folder.

 - [2022-08-08: B.1.1-B.1.5](designation_records/B.1.1-B.1.5_2022-08-08.md)

### Lineage proposals
To propose additional lineages, open a github issue in this repository.

