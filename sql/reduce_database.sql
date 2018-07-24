
/* Temporary table of species we are interested in */

CREATE TEMP TABLE IF NOT EXISTS interesting_species (species_id int PRIMARY KEY);
INSERT INTO interesting_species(species_id) VALUES
	(9606), -- Homo sapiens
	(10090) -- Mus musculus
ON CONFLICT DO NOTHING;

/* Useful views */

-- Proteins in species we are interested in
CREATE OR REPLACE VIEW interesting_proteins AS
	SELECT *
	FROM items.proteins AS proteins
	WHERE proteins.species_id IN (
		SELECT species_id
		FROM interesting_species
	);

-- Neighborhood evidence in species we are interested
CREATE OR REPLACE VIEW interesting_runs AS
	SELECT *
	FROM items.runs AS runs
	WHERE runs.species_id IN (
		SELECT species_id
		FROM interesting_species
	);
		  
-- Mapping of orthologous groups to an un-interrupted group of genes on the chromosome
-- for species we are interesred in
CREATE OR REPLACE VIEW interesting_runs_orthgroups AS
	SELECT *
	FROM items.runs_orthgroups AS runs_orthgroups
	WHERE EXISTS (
		SELECT 1
		FROM interesting_runs
		WHERE interesting_runs.run_id = runs_orthgroups.run_id
	);

-- Mapping between the internal identifier of genes and proteins
-- for species we are interested in
CREATE OR REPLACE VIEW interesting_genes_proteins AS
	SELECT *
	FROM items.genes_proteins AS genes_proteins
	WHERE EXISTS (
		SELECT 1
		FROM interesting_proteins
		WHERE interesting_proteins.protein_id = genes_proteins.protein_id
	);

/*

Delete entries from the following tables based on protein_id (from interesting_proteins):
- proteins_linkouts
- proteins_smartlinkouts
- proteins_sequences
- proteins_hierarchical_ogs
- proteins_imagematches
- runs_genes_proteins
- genes_proteins

*/

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.proteins_linkouts AS proteins_linkouts;
-> 24 190 982 (total)

SELECT COUNT(protein_id)
FROM items.proteins_linkouts AS proteins_linkouts
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_linkouts.protein_id = interesting_proteins.protein_id
);
-> 179 900

SELECT COUNT(protein_id)
FROM items.proteins_linkouts AS proteins_linkouts
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_linkouts.protein_id = interesting_proteins.protein_id
);
-> 24 011 082

*/

-- DELETE
SELECT protein_id
FROM items.proteins_linkouts AS proteins_linkouts
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_linkouts.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.proteins_smartlinkouts AS proteins_smartlinkouts;
-> 9 643 763 (total)

SELECT COUNT(protein_id)
FROM items.proteins_smartlinkouts AS proteins_smartlinkouts
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_smartlinkouts.protein_id = interesting_proteins.protein_id
);
-> 43 125

SELECT COUNT(protein_id)
FROM items.proteins_smartlinkouts AS proteins_smartlinkouts
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_smartlinkouts.protein_id = interesting_proteins.protein_id
);
-> 9 600 638

*/

-- DELETE
SELECT protein_id
FROM items.proteins_smartlinkouts AS proteins_smartlinkouts
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_smartlinkouts.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.proteins_sequences AS proteins_sequences;
-> 9 643 763 (total)

SELECT COUNT(protein_id)
FROM items.proteins_sequences AS proteins_sequences
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_sequences.protein_id = interesting_proteins.protein_id
);
-> 43 125

SELECT COUNT(protein_id)
FROM items.proteins_sequences AS proteins_sequences
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_sequences.protein_id = interesting_proteins.protein_id
);
-> 9 600 638

*/

-- DELETE
SELECT protein_id
FROM items.proteins_sequences AS proteins_sequences
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_sequences.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.proteins_hierarchical_ogs AS proteins_hierarchical_ogs;
-> 35 060 390 (total)

SELECT COUNT(protein_id)
FROM items.proteins_hierarchical_ogs AS proteins_hierarchical_ogs
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_hierarchical_ogs.protein_id = interesting_proteins.protein_id
);
-> 411 868

SELECT COUNT(protein_id)
FROM items.proteins_hierarchical_ogs AS proteins_hierarchical_ogs
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_hierarchical_ogs.protein_id = interesting_proteins.protein_id
);
-> 34 648 522

*/

-- DELETE
SELECT protein_id
FROM items.proteins_hierarchical_ogs AS proteins_hierarchical_ogs
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_hierarchical_ogs.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.proteins_imagematches AS proteins_imagematches;
-> 1 010 841 (total)

SELECT COUNT(protein_id)
FROM items.proteins_imagematches AS proteins_imagematches
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_imagematches.protein_id = interesting_proteins.protein_id
);
-> 74 409

SELECT COUNT(protein_id)
FROM items.proteins_imagematches AS proteins_imagematches
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_imagematches.protein_id = interesting_proteins.protein_id
);
-> 936 432

*/

-- DELETE
SELECT protein_id
FROM items.proteins_imagematches AS proteins_imagematches
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE proteins_imagematches.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.runs_genes_proteins AS runs_genes_proteins;
-> 5 814 759 (total)

SELECT COUNT(protein_id)
FROM items.runs_genes_proteins AS runs_genes_proteins
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE runs_genes_proteins.protein_id = interesting_proteins.protein_id
);
-> 0

SELECT COUNT(protein_id)
FROM items.runs_genes_proteins AS runs_genes_proteins
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE runs_genes_proteins.protein_id = interesting_proteins.protein_id
);
-> 5 814 759

*/

-- DELETE
SELECT protein_id
FROM items.runs_genes_proteins AS runs_genes_proteins
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE runs_genes_proteins.protein_id = interesting_proteins.protein_id
);

/*

------------------------------------------------------------------------------------------

SELECT COUNT(protein_id)
FROM items.genes_proteins AS genes_proteins;
-> 9 643 763 (total)

SELECT COUNT(protein_id)
FROM items.genes_proteins AS genes_proteins
WHERE EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE genes_proteins.protein_id = interesting_proteins.protein_id
);
-> 43 125

SELECT COUNT(protein_id)
FROM items.genes_proteins AS genes_proteins
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE genes_proteins.protein_id = interesting_proteins.protein_id
);
-> 9 600 638

*/

-- DELETE
SELECT protein_id
FROM items.genes_proteins AS genes_proteins
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_proteins
	WHERE genes_proteins.protein_id = interesting_proteins.protein_id
);

/*

Delete entries from the following tables based on orthgroup_id (from interesting_runs_orthgroups):
- orthgroups

*/

/*

------------------------------------------------------------------------------------------

SELECT COUNT(orthgroup_id)
FROM items.orthgroups AS orthgroups;
-> 190 803 (total)

SELECT COUNT(orthgroup_id)
FROM items.orthgroups AS orthgroups
WHERE EXISTS (
	SELECT 1
	FROM interesting_runs_orthgroups
	WHERE orthgroups.orthgroup_id = interesting_runs_orthgroups.orthgroup_id
);
-> 0

SELECT COUNT(orthgroup_id)
FROM items.orthgroups AS orthgroups
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_runs_orthgroups
	WHERE orthgroups.orthgroup_id = interesting_runs_orthgroups.orthgroup_id
);
-> 190 803

*/

-- DELETE
SELECT orthgroup_id
FROM items.orthgroups AS orthgroups
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_runs_orthgroups
	WHERE orthgroups.orthgroup_id = interesting_runs_orthgroups.orthgroup_id
);

/*

Delete entries from the following tables based on run_id (from interesting_runs):
- runs_orthgroups

*/

/*

------------------------------------------------------------------------------------------

SELECT COUNT(run_id)
FROM items.runs_orthgroups AS runs_orthgroups;
-> 4 833 636 (total)

SELECT COUNT(run_id)
FROM items.runs_orthgroups AS runs_orthgroups
WHERE EXISTS (
	SELECT 1
	FROM interesting_runs
	WHERE interesting_runs.run_id = runs_orthgroups.run_id
);
-> 0

SELECT COUNT(run_id)
FROM items.runs_orthgroups AS runs_orthgroups
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_runs
	WHERE interesting_runs.run_id = runs_orthgroups.run_id
);
-> 4 833 636

*/

-- DELETE
SELECT run_id
FROM items.runs_orthgroups AS runs_orthgroups
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_runs
	WHERE interesting_runs.run_id = runs_orthgroups.run_id
);

/*

Delete entries from the following tables based on gene_id (from interesting_genes_proteins):
- genes

*/

/*

------------------------------------------------------------------------------------------

SELECT COUNT(gene_id)
FROM items.genes AS genes;
-> 9 643 763 (total)

SELECT COUNT(gene_id)
FROM items.genes AS genes
WHERE EXISTS (
	SELECT 1
	FROM interesting_genes_proteins
	WHERE interesting_genes_proteins.gene_id = genes.gene_id
);
-> 43 125

SELECT COUNT(gene_id)
FROM items.genes AS genes
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_genes_proteins
	WHERE interesting_genes_proteins.gene_id = genes.gene_id
);
-> 9 600 638

*/

-- DELETE
SELECT gene_id
FROM items.genes AS genes
WHERE NOT EXISTS (
	SELECT 1
	FROM interesting_genes_proteins
	WHERE interesting_genes_proteins.gene_id = genes.gene_id
);

/*

Delete entries from the following tables based on species_id:
- proteins
- species
- species_nodes
- species_to_levels
- orthgroups_species
- runs
- proteins_names
- hierarchical_ogs_proteins
- proteins_orthgroups
- species_names

*/

-- DELETE
SELECT protein_id
FROM items.proteins AS proteins
WHERE proteins.species_id NOT IN (
	SELECT species_id
	FROM interesting_species
);
