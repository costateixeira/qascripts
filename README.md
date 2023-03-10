
1. Look in datatypes page for normatives:
  Check for <a> that have href="versions.html#std-process", title="Standards Status = Normative"
  Get the id of the table (greatgrandparent of the <a> element)
  => output/t1-normativedatatypes.yaml

2. Look in documentation page for normatives: 
  Check for all <a> that have href="versions.html#std-process", title="Normative Content")
  Get the content of the preceding <a> element
  => output/t2-normativesindocumentation.yaml

3. Look in resourcelist for normatives:
  Check for all <a> that have href="versions.html#std-process", title="Normative Content"), 
  Get the text of the parent <a> element - and remove the extra stuff because the <a>s are nested here.
  => output/t3-normativesinreslist.yaml

4. Put those all together
  => 1-NormativesInPages.yaml

5. Find the Normative resources:
  Go through the package JSONs, identify the SDs with Normative status
  => output/2-normativeSDs.yaml

6. Compare the entries in the two lists (normative SDs and normatives found in docs) and create a new YAML file with three lists:
  Entries that can be found in both files
  Entries that can be found in the pages but not in the SDs
  Entries that can be found in the SDs but not in the pages
  => output/R3-comparison.yaml


7. Find ValueSets that should not be normative
  Go through the StructureDefs that have Normative status, 
  For all valueset bindings, get the normative status from the corresponding ValueSet JSON
  => output/2-Normative_sd_valuesets.yaml


8. List valuesets that need not be normative
  Go through all the ValueSet JSONs that are Normative (from 1)
  List those that are not referenced in the normative resources
  => output/3-unexpected_normative_valuesets.yaml



