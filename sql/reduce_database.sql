CREATE OR REPLACE VIEW human_mouse_proteins AS
	SELECT *
	FROM items.proteins AS proteins
	WHERE proteins.species_id = 9606 OR 
		  proteins.species_id = 10090;

CREATE OR REPLACE VIEW human_mouse_runs AS
	SELECT *
	FROM items.runs AS runs
	WHERE runs.species_id = 9606 OR 
		  runs.species_id = 10090;
		  
CREATE OR REPLACE VIEW human_mouse_runs_orthgroups AS
	SELECT *
	FROM items.runs_orthgroups AS runs_orthgroups
	WHERE EXISTS (
		SELECT 1
		FROM human_mouse_runs
		WHERE human_mouse_runs.run_id = runs_orthgroups.run_id
	);

CREATE OR REPLACE VIEW human_mouse_genes_proteins AS
	SELECT *
	FROM items.genes_proteins AS genes_proteins
	WHERE EXISTS (
		SELECT 1
		FROM human_mouse_proteins
		WHERE human_mouse_proteins.protein_id = genes_proteins.protein_id
	);

/*
Delete entries from the following tables based on species_id:
- species
- species_nodes
- species_to_levels
- orthgroups_species
- runs

Delete entries from the following tables based on protein_id (from human_mouse_proteins):
- proteins_names
- proteins_linkouts
- proteins_smartlinkouts
- proteins_names
- proteins_sequences
- hierarchical_ogs_proteins
- proteins_hierarchical_ogs
- proteins_orthgroups
- proteins_imagematches

- runs_genes_proteins
- genes_proteins

Delete entries from the following tables based on species_id (from human_mouse_runs):
- runs_orthgroups

Delete entries from the following tables based on orthgroup_id (from human_mouse_runs_orthgroups):
- orthgroups
- orthgroups_species

Delete entries from the following tables based on gene_id (from human_mouse_genes_proteins):
- genes

*/


-- DELETE
SELECT protein_id
FROM items.proteins_smartlinkouts AS smartlinkouts
WHERE NOT EXISTS (
	SELECT 1
	FROM human_mouse_proteins
	WHERE smartlinkouts.protein_id = human_mouse_proteins.protein_id
);
