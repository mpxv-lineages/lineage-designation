#! bash
# Check that file name equals lineage name
fail=false
for file in lineages/*.yml; do
    if [ "lineages/$(yq .name $file).yml" != "$file" ]; then
        echo "File name: $file does not match contained lineage name $(yq .name $file)"
        fail=true
    else
        echo "File name: $file matches contained lineage name $(yq .name $file)"
    fi
done

if $fail; then exit 1; fi
