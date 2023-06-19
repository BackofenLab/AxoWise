# Graph Model
## Node Types
1. Celltype
    * Properties:
        - name (String): Celltype Name
2. Study
    * Properties:
        - source (String): Source of the study (e.g. in-house)
3. Context
    * Properties:
        - Context (String): Specified context (e.g. 6h-0h, RC12h-12h etc.)
4. FT (Functional Term)
    * Properties:
        - Term (String): Term of entity (e.g. GO:0007275)
        - category (String): Category of FT (e.g. Biological Process (Gene Ontology))
        - name (String): Name of FT (e.g. Multicellular organism development)
5. MeanCount (Placeholder node)
    * Properties: None
6. OR (Open Region)
    * Properties:
        - nearest_index (String): 
        - annotation (String):
        - feature (String):
        - in_RNAseq (String):
        - seqnames (String):
        - strand (String):
        - summit (String):
7. Source (Placeholder / Aggregation Node)
    * Properties: None
8. TF (Transcription Factor) / TG (Target Gene)
    * Properties:
        - ENSEMBL (String): The ENSEMBL ID of the Entity
        - ENTREZID (Integer): The Entez Gene ID
        - SYMBOL (String): Symbol(s) of the Gene
        - annot (String): Annotation / More info on the Gene
    * Note: Transcription Factors have both TF and TG labels

## Relationships

### Source-specific

![DE Values](./figs/model/graph_v5.3_DE.png)
![DA Values](./figs/model/graph_v5.3_DA.png)
![Overview](./figs/model/graph_v5.3_overview.png)

1. HAS 
    * Between:
        - Celltype -> Source
        - Study -> Source
        - Source -> Context
        - Source -> MeanCount
    * Properties: None

2. MEANCOUNT
    * Between:
        - MeanCount -> TG
        - MeanCount -> OR
    * Properties:
        - Source (Integer): ID of Source node in DB
        - Value (Float): Mean count value found in experiment

3. DE
    * Between:
        - Context -> TG
    * Properties:
        - Source (Integer): ID of Source node in DB
        - Value (Float): DE Value found in experiment under specified Context
        - p (Float): p value associated with the DE value

4. DA
    * Between:
        - Context -> OR
    * Properties:
        - Source (Integer): ID of Source node in DB
        - Value (Float): DA Value found in experiment under specified Context
        - p (Float): p value associated with the DA value

5. CORRELATION
    * Between:
        - TF -> TG
        - OR -> TG
    * Properties:
        - Source (Integer): ID of Source node in DB
        - Correlation (Float): Correlation Value found in experiment between two entities

6. (MOTIF)
    * Between:
        - TF -> OR
    * Properties:
        - Motif (String): Motif of OR that TF binds to
    * Note: This information is not specific to the experiment

7. (DISTANCE)
    * Between:
        - OR -> TG
    * Properties:
        - Distance (Integer): Distance between OR and TG
    * Note: This information is not specific to the experiment


## Source unspecific

![FT-TG](./figs/model/graph_v5.3_ft_tg.png)
![FT-FT](./figs/model/graph_v5.3_ft_ft.png)

1. LINK
    * Between:
        - TG -> FT
    * Properties: None

2. OVERLAP
    * Between:
        - FT -> FT
    * Properties:
        - Score (Float): Overlap score as previously computed by Victor (?)

3. STRING
    * Between:
        - TG -> TG
    * Properties:
        - Score (Integer): STRING Association Score between two Genes