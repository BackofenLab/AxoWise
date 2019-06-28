---
title: Merging KEGG PATHWAY and STRING
layout: page
permalink: /KEGG
no_nav: true
---

# 1. Get the organism identifiers
__[http://rest.kegg.jp/list/genome](http://rest.kegg.jp/list/genome)__

Example:
```
gn:T01001	hsa, HUMAN, 9606; Homo sapiens (human)
```

- KEGG string identifier: _hsa_
- NCBI Taxomony identifier: _9606_

# 2. Get all pathways in the organism
__http://rest.kegg.jp/list/pathway/[organism_id]__

Example:
[http://rest.kegg.jp/list/pathway/hsa](http://rest.kegg.jp/list/pathway/hsa)
```
path:hsa00010	Glycolysis / Gluconeogenesis - Homo sapiens (human)
```

# 3. Query each pathway
__http://rest.kegg.jp/get/[pathway_id]__  

- Get the following by parsing the flat file:
    - description
    - classes
    - diseases
    - drugs
    - genes
    - compounds

Example:
[http://rest.kegg.jp/get/path:hsa00010](http://rest.kegg.jp/get/path:hsa00010)
```
DESCRIPTION Glycolysis is the process of converting glucose into pyruvate...
...
CLASS       Metabolism; Carbohydrate metabolism
...
DISEASE     H00069  Glycogen storage disease
            H00071  Hereditary fructose intolerance
            H00072  Pyruvate dehydrogenase complex deficiency
...
DRUG        D00123  Cyanamide (JP17)
            D00131  Disulfiram (JP17/USP/INN)
            D07257  Lonidamine (INN)
...
GENE        3101  HK3; hexokinase 3 [KO:K00844] [EC:2.7.1.1]
            3098  HK1; hexokinase 1 [KO:K00844] [EC:2.7.1.1]
            3099  HK2; hexokinase 2 [KO:K00844] [EC:2.7.1.1]
...
COMPOUND    C00022  Pyruvate
            C00024  Acetyl-CoA
            C00031  D-Glucose
            C00033  Acetate
...
```

# 4. Turn the genes from the pathway into unique identifiers

Example:
- HK3 ---> _hsa:3101_
- HK1 ---> _hsa:3098_
- HK2 ---> _hsa:3099_

# 5. Use STRING API to map the gene names to the external IDs (also available in STRING)
__https://string-db.org/api/[output-format]/get_string_ids?identifiers=[identifiers]&[optional]__

- _output-format_ = tsv
- _optional_:
	- _species_ (NCBI Taxomony identifier; from step 1)
	- _limit_ = 1 (return the best match; do not use to see if there is a unique match or not)

Example:  
[https://string-db.org/api/tsv/get_string_ids?identifiers=hsa:3101%0dhsa:3098%0dhsa:3099&species=9606](https://string-db.org/api/tsv/get_string_ids?identifiers=hsa:3101%0dhsa:3098%0dhsa:3099&species=9606)
```
queryIndex	stringId	ncbiTaxonId	taxonName	preferredName	annotation
0	9606.ENSP00000292432	9606	Homo sapiens	HK3	Hexokinase 3 (white cell)
1	9606.ENSP00000384774	9606	Homo sapiens	HK1	Hexokinase 1
2	9606.ENSP00000290573	9606	Homo sapiens	HK2	Hexokinase 2
```
