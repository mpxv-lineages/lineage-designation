#! bash

# Remove file in case it exists
rm auto-generated/reference_accessions.txt

# Extract reference sequence accessions
for file in lineages/*.yml; do
    yq '.reference_sequences | .[].accession' $file >>auto-generated/reference_accessions.txt
done

# Error if there are duplicates

if [ -n "$(sort auto-generated/reference_accessions.txt | uniq -cd)" ]; then
    echo "Duplicate accessions found"
    sort auto-generated/reference_accessions.txt | uniq -cd
fi

# Download and extract reference sequences
curl -fsSL \
    --compressed https://data.nextstrain.org/files/workflows/monkeypox/sequences.fasta.xz |
    xz -d |
    seqkit grep \
        -f auto-generated/reference_accessions.txt \
        -w0 \
        --quiet \
        >auto-generated/reference_sequences.fasta
