import unittest

from context import parse

class TestKEGG(unittest.TestCase):

    def test_parse_flat_file(self):

        with open("tests/path_hsa00010.txt") as file:
            kegg_flat_file = file.read()

        # Parse the KEGG pathway flat file
        pathway_parsed = parse.parse_flat_file(kegg_flat_file)
        name = pathway_parsed[0]
        description = pathway_parsed[1]
        classes = pathway_parsed[2]
        diseases = pathway_parsed[3]
        drugs = pathway_parsed[4]
        genes = pathway_parsed[5]
        compounds = pathway_parsed[6]

        self.assertEqual(name, "Glycolysis / Gluconeogenesis")
        self.assertEqual(
            description,
            "Glycolysis is the process of converting glucose into pyruvate and generating small amounts "
            "of ATP (energy) and NADH (reducing power). It is a central pathway that produces important "
            "precursor metabolites: six-carbon compounds of glucose-6P and fructose-6P and three-carbon "
            "compounds of glycerone-P, glyceraldehyde-3P, glycerate-3P, phosphoenolpyruvate, and pyruvate "
            "[MD:M00001]. Acetyl-CoA, another important precursor metabolite, is produced by oxidative "
            "decarboxylation of pyruvate [MD:M00307]. When the enzyme genes of this pathway are examined "
            "in completely sequenced genomes, the reaction steps of three-carbon compounds from glycerone-P "
            "to pyruvate form a conserved core module [MD:M00002], which is found in almost all organisms "
            "and which sometimes contains operon structures in bacterial genomes. Gluconeogenesis is a "
            "synthesis pathway of glucose from noncarbohydrate precursors. It is essentially a reversal of "
            "glycolysis with minor variations of alternative paths [MD:M00003]."
        )
        self.assertEqual(classes, ["Metabolism", "Carbohydrate metabolism"])
        self.assertEqual(diseases, [
            ("H00069", "Glycogen storage disease"),
            ("H00071", "Hereditary fructose intolerance"),
            ("H00072", "Pyruvate dehydrogenase complex deficiency"),
            ("H00114", "Fructose-1,6-bisphosphatase deficiency"),
            ("H00664", "Anemia due to disorders of glycolytic enzymes"),
            ("H01071", "Acute alcohol sensitivity"),
            ("H01096", "Pyruvate kinase deficiency"),
            ("H01267", "Familial hyperinsulinemic hypoglycemia"),
            ("H01760", "Hepatic glycogen storage disease"),
            ("H01762", "Muscle glycogen storage disease"),
            ("H01939", "Glycogen storage disease type I"),
            ("H01945", "Glycogen storage disease type VII"),
            ("H01946", "Glycogen storage disease type XI"),
            ("H01951", "Glycogen storage disease type X"),
            ("H01952", "Glycogen storage disease type XII"),
            ("H01953", "Glycogen storage disease type XIII"),
            ("H01954", "Glycogen storage disease type XIV"),
            ("H01997", "Pyruvate dehydrogenase E1-alpha deficiency"),
            ("H01998", "Pyruvate dehydrogenase E1-beta deficiency"),
            ("H01999", "Pyruvate dehydrogenase E2 deficiency"),
            ("H02000", "Dihydrolipoamide dehydrogenase deficiency")
        ])
        self.assertEqual(drugs, [
            ("D00123", "Cyanamide (JP17)"),
            ("D00131", "Disulfiram (JP17/USP/INN)"),
            ("D07257", "Lonidamine (INN)"),
            ("D08970", "Piragliatin (USAN)")
        ])
        self.assertEqual(compounds, [
            ("C00022", "Pyruvate"),
            ("C00024", "Acetyl-CoA"),
            ("C00031", "D-Glucose"),
            ("C00033", "Acetate"),
            ("C00036", "Oxaloacetate"),
            ("C00068", "Thiamin diphosphate"),
            ("C00074", "Phosphoenolpyruvate"),
            ("C00084", "Acetaldehyde"),
            ("C00103", "D-Glucose 1-phosphate"),
            ("C00111", "Glycerone phosphate"),
            ("C00118", "D-Glyceraldehyde 3-phosphate"),
            ("C00186", "(S)-Lactate"),
            ("C00197", "3-Phospho-D-glycerate"),
            ("C00221", "beta-D-Glucose"),
            ("C00236", "3-Phospho-D-glyceroyl phosphate"),
            ("C00267", "alpha-D-Glucose"),
            ("C00469", "Ethanol"),
            ("C00631", "2-Phospho-D-glycerate"),
            ("C00668", "alpha-D-Glucose 6-phosphate"),
            ("C01159", "2,3-Bisphospho-D-glycerate"),
            ("C01172", "beta-D-Glucose 6-phosphate"),
            ("C01451", "Salicin"),
            ("C05125", "2-(alpha-Hydroxyethyl)thiamine diphosphate"),
            ("C05345", "beta-D-Fructose 6-phosphate"),
            ("C05378", "beta-D-Fructose 1,6-bisphosphate"),
            ("C06186", "Arbutin"),
            ("C06187", "Arbutin 6-phosphate"),
            ("C06188", "Salicin 6-phosphate"),
            ("C15972", "Enzyme N6-(lipoyl)lysine"),
            ("C15973", "Enzyme N6-(dihydrolipoyl)lysine"),
            ("C16255", "[Dihydrolipoyllysine-residue acetyltransferase] S-acetyldihydrolipoyllysine")
        ])
        self.assertEqual(genes, [
            ("3101", "HK3", "hexokinase 3"),
            ("3098", "HK1", "hexokinase 1"),
            ("3099", "HK2", "hexokinase 2"),
            ("80201", "HKDC1", "hexokinase domain containing 1"),
            ("2645", "GCK", "glucokinase"),
            ("2821", "GPI", "glucose-6-phosphate isomerase"),
            ("5213", "PFKM", "phosphofructokinase, muscle"),
            ("5214", "PFKP", "phosphofructokinase, platelet"),
            ("5211", "PFKL", "phosphofructokinase, liver type"),
            ("2203", "FBP1", "fructose-bisphosphatase 1"),
            ("8789", "FBP2", "fructose-bisphosphatase 2"),
            ("230", "ALDOC", "aldolase, fructose-bisphosphate C"),
            ("226", "ALDOA", "aldolase, fructose-bisphosphate A"),
            ("229", "ALDOB", "aldolase, fructose-bisphosphate B"),
            ("7167", "TPI1", "triosephosphate isomerase 1"),
            ("2597", "GAPDH", "glyceraldehyde-3-phosphate dehydrogenase"),
            ("26330", "GAPDHS", "glyceraldehyde-3-phosphate dehydrogenase, spermatogenic"),
            ("5232", "PGK2", "phosphoglycerate kinase 2"),
            ("5230", "PGK1", "phosphoglycerate kinase 1"),
            ("5223", "PGAM1", "phosphoglycerate mutase 1"),
            ("5224", "PGAM2", "phosphoglycerate mutase 2"),
            ("441531", "PGAM4", "phosphoglycerate mutase family member 4"),
            ("2027", "ENO3", "enolase 3"),
            ("2026", "ENO2", "enolase 2"),
            ("2023", "ENO1", "enolase 1"),
            ("387712", "ENO4", "enolase 4"),
            ("5315", "PKM", "pyruvate kinase M1/2"),
            ("5313", "PKLR", "pyruvate kinase L/R"),
            ("5161", "PDHA2", "pyruvate dehydrogenase E1 alpha 2 subunit"),
            ("5160", "PDHA1", "pyruvate dehydrogenase E1 alpha 1 subunit"),
            ("5162", "PDHB", "pyruvate dehydrogenase E1 beta subunit"),
            ("1737", "DLAT", "dihydrolipoamide S-acetyltransferase"),
            ("1738", "DLD", "dihydrolipoamide dehydrogenase"),
            ("160287", "LDHAL6A", "lactate dehydrogenase A like 6A"),
            ("92483", "LDHAL6B", "lactate dehydrogenase A like 6B"),
            ("3939", "LDHA", "lactate dehydrogenase A"),
            ("3945", "LDHB", "lactate dehydrogenase B"),
            ("3948", "LDHC", "lactate dehydrogenase C"),
            ("124", "ADH1A", "alcohol dehydrogenase 1A (class I), alpha polypeptide"),
            ("125", "ADH1B", "alcohol dehydrogenase 1B (class I), beta polypeptide"),
            ("126", "ADH1C", "alcohol dehydrogenase 1C (class I), gamma polypeptide"),
            ("131", "ADH7", "alcohol dehydrogenase 7 (class IV), mu or sigma polypeptide"),
            ("127", "ADH4", "alcohol dehydrogenase 4 (class II), pi polypeptide"),
            ("128", "ADH5", "alcohol dehydrogenase 5 (class III), chi polypeptide"),
            ("130", "ADH6", "alcohol dehydrogenase 6 (class V)"),
            ("10327", "AKR1A1", "aldo-keto reductase family 1 member A1"),
            ("217", "ALDH2", "aldehyde dehydrogenase 2 family member"),
            ("224", "ALDH3A2", "aldehyde dehydrogenase 3 family member A2"),
            ("219", "ALDH1B1", "aldehyde dehydrogenase 1 family member B1"),
            ("501", "ALDH7A1", "aldehyde dehydrogenase 7 family member A1"),
            ("223", "ALDH9A1", "aldehyde dehydrogenase 9 family member A1"),
            ("221", "ALDH3B1", "aldehyde dehydrogenase 3 family member B1"),
            ("222", "ALDH3B2", "aldehyde dehydrogenase 3 family member B2"),
            ("220", "ALDH1A3", "aldehyde dehydrogenase 1 family member A3"),
            ("218", "ALDH3A1", "aldehyde dehydrogenase 3 family member A1"),
            ("84532", "ACSS1", "acyl-CoA synthetase short chain family member 1"),
            ("55902", "ACSS2", "acyl-CoA synthetase short chain family member 2"),
            ("130589", "GALM", "galactose mutarotase"),
            ("5236", "PGM1", "phosphoglucomutase 1"),
            ("55276", "PGM2", "phosphoglucomutase 2"),
            ("2538", "G6PC", "glucose-6-phosphatase catalytic subunit"),
            ("57818", "G6PC2", "glucose-6-phosphatase catalytic subunit 2"),
            ("92579", "G6PC3", "glucose-6-phosphatase catalytic subunit 3"),
            ("83440", "ADPGK", "ADP dependent glucokinase"),
            ("669", "BPGM", "bisphosphoglycerate mutase"),
            ("9562", "MINPP1", "multiple inositol-polyphosphate phosphatase 1"),
            ("5105", "PCK1", "phosphoenolpyruvate carboxykinase 1"),
            ("5106", "PCK2", "phosphoenolpyruvate carboxykinase 2, mitochondrial")
        ])


if __name__ == "__main__":
    print("Testing KEGG data...")
    unittest.main()
