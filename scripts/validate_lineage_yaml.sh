#! bash
fail=false
for file in lineages/*.yml; do
  ajv -s schemas/lineage_schema.yml -d $file || fail=true
done

if $fail; then exit 1; fi
