#! bash
fail=false
DEFINITIONS_DIR='definitions/IIb/sh2017'
for file in $DEFINITIONS_DIR/*.yml; do
  ajv -s schemas/single_lineage/lineage_schema_1-0-0.yml -d $file || fail=true
done

if $fail; then exit 1; fi
