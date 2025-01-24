import logging
from typing import Dict, Any
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import PromptTemplate
import json
import time

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

def get_shared_llm():
    """Returns a shared LLM instance for all agents."""
    return Ollama(
        model="llama3.1:8b", 
        temperature=0
    )

def extract_data(text: str) -> str:
    """Extracts source code URLs and accession codes from scientific text."""
    
    prompt = f"""
        You are a highly precise extraction tool. I will provide you with a scientific text and you have to extract source code and sequencing data URLs, and accession codes for sequencing data from it.
        Your task:
        1. Extract **only** explicitly stated sequencing data accession codes and their respective database names (e.g., GEO, ENA, SRA, etc.). Do **not** infer or guess accession codes if they are not explicitly mentioned in the text.
        2. Identify **all** sequencing data URLs, including URLs from **Zenodo**. For Zenodo, include any URL explicitly mentioned. Sequencing data URLs are of hosting services where sequencing data in the field of Bioinformatics is uploaded.
        3. Identify **all** source code URLs, including URLs from **GitHub** and **Zenodo**. Source code URLs are those where custom code or custom scripts are uploaded.

        Return the results **only** in valid JSON format, with no additional text or explanation. Do **not** include any introductory or closing statements.

        The returned JSON should strictly follow the following format:
        {{
            "accession_codes": {{
                "database_name_1": ["accession_code_1", "accession_code_2"],
                "database_name_2": ["accession_code_3"]
            }},
            "sequencing_data": ["sequencing_data_URL1", "sequencing_data_URL2"],
            "source_code": ["GitHub_URL", "Zenodo_URL"]
        }}

        Example Input:
        <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. Sequencing data is available on Zenodo at https://zenodo.org/record/12345 and https://doi.org/10.1010/zenodo.1234567. 
        Additional analysis scripts are hosted on Zenodo at https://zenodo.org/record/67890 and GitHub at https://github.com/example/repo. The following open-source code and databases were used in this article: JaBbA (v.1.1) (https://github.com/mskilab/JaBbA), 
        gGnome (commit c390d80) (https://github.com/mskilab/gGnome), AmpliconArchitect (https://github.com/virajbdeshpande/AmpliconArchitect). High-throughput sequencing (HTS) of T cell receptor β (TRB) and T cell receptor ⍺ (TRA) dataset are available from Adaptive Biotechnologies (http://clients.adaptivebiotech.com/login) <<END DATA>>

        Example Output:
        {{
            "accession_codes": {{
                "GEO": ["GSE12345", "GSE67890"]
            }},
            "sequencing_data": [
                "https://zenodo.org/record/12345",
                "https://doi.org/10.1010/zenodo.1234567",
                "http://clients.adaptivebiotech.com/login"
            ],
            "source_code": [
                "https://github.com/example/repo",
                "https://zenodo.org/record/67890"
            ]
        }}

        Strict Rules:
        1. accession_codes: Include ONLY valid formats:
            - Accession codes must strictly follow common formats (e.g., GSE followed by numbers for GEO, PRJ followed by alphanumeric strings for SRA, etc.)
            - ONLY include accession codes that match valid formats
            - If no accession codes are available, leave the "accession codes" section empty: "accession_codes": {{}}.

        2. sequencing_data: Include URLs for databases:
            - ONLY include sequencing data URLs that are explicitly stated in the input text
            - If no sequencing data URLs are available, leave the "sequencing data" section empty: "sequencing_data": [].

        3. source_code: Include ONLY:
        - Github URLs with code/scripts
        - Zenodo URLs with code/scripts
        - Do **NOT** add any database/software/tool repositories
        - If no source code URLs are available, leave the "source code" section empty: "source_code": [].

        - ONLY return the JSON structure as shown, with **no additional text or explanation**.

        Input Text to Process:
        <<DATA>> {text} <<END DATA>>
        """
    try:
        llm=get_shared_llm()
        response = llm.complete(prompt).text.strip()
        result = json.loads(response)
        # logger.info(result)
        
        # Validate structure
        if not isinstance(result.get('accession_codes', {}), dict):
            raise ValueError("accession_codes must be a dictionary")
        if not isinstance(result.get('sequencing_data', []), list):
            raise ValueError("sequencing_data must be a list")
        if not isinstance(result.get('source_code', []), list):
            raise ValueError("source_code must be a list")
            
        # logger.info(f"Extraction result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        # logger.error(f"Extraction error: {e}")
        return json.dumps({
            "accession_codes": {},
            "sequencing_data": [],
            "source_code": []
        })



def review_data(text: str, extracted_data: str) -> str:
    """Validates extracted data against the original text."""

    prompt = f"""You are a validation tool. Return EXACTLY and ONLY a JSON object matching this structure - NO additional text or explanation:

        {{
            "is_valid": true,
            "validation":
            {{
                "accession_codes": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},

                "source_code": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},
                "sequencing_data": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }}
            }}
        }}

        Validation Rules:
        1. Return ONLY the JSON - no text before or after
        2. Source code is **ONLY** GitHub/Zenodo URLs.
        3. Count each individual accession code that matches format:
        - GEO: GSE*, GSM*, GPL*
        - SRA: SRP*, SRR*, SRS*, PRJNA*
        - EGA: EGAS*, EGAD*
        - GenBank: MN*, NC_*

        Strict rules:
        - Do **NOT** add anything to the output that is not explicitly mentioned in the extracted_data.
        
        Input Text to validate against:
        {text}

        Extracted data to validate:
        {extracted_data}

        Return the results **only** in valid JSON format with **no additional text**. Follow this format exactly:
        {{
            "accession_codes": {{
                "database_name_1": [],
                "database_name_2": []
            }},
            "sequencing_data": [],
            "source_code": []
        }}
    """
        
    try:
        llm=get_shared_llm()
        response = llm.complete(prompt).text.strip()
        response = response.replace('```json', '').replace('```', '').strip()   # remove any markdown code blocks if present
        
        # logger.info(f"Review raw response: {response}")
        result = json.loads(response)
        # logger.info(f"Review result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        # logger.error(f"Review error: {e}")
        return json.dumps({
            "is_valid": False,
            "validation": {
                "accession_codes": {
                    "valid_count": 0,
                    "invalid_count": 0
                },

                "source_code": {
                    "valid_count": 0,
                    "invalid_count": 0
                },
                "sequencing_data": {
                    "valid_count": 0,
                    "invalid_count": 0
                }
            }
        })

def get_agent():

    extract_tool = FunctionTool.from_defaults(
        fn=extract_data,
        name="extract_data",
        description="Extracts source code URLs and accession codes from scientific text"
    )

    review_tool = FunctionTool.from_defaults(
        fn=review_data,
        name="review_data",
        description="Validates extracted data against the original text"
    )


    system_prompt = """You are designed to extract and validate source code URLs and sequencing data URLs, and accession codes from scientific text.

    ## Tools
    You have access to these tools:
    {tool_desc}

    ## Process
    1. extract data using extract_data
    2. validate using review_data
    3. If validation fails, try extract_data again

    ## Output Format
    Please use this format:

    ```
    Thought: I need to [action] because [reason]
    Action: tool name
    Action Input: {{"text": "input text"}}
    ```

    Please ALWAYS start with a Thought.

    Return **ONLY** the JSON object with no additional text before or after the JSON object.

    If this format is used, the user will respond in the following format:

    ```
    Observation: tool response
    ```

    You should keep repeating the above format until you have all the extracted information. At that point, you MUST respond
    in the the following format:

    ```
    Thought: I can answer without using any more tools.
    Answer: [your answer here]
    ```


    When validation is successful:
    Thought: Extraction and validation complete
    Answer: [final extracted and validated data]

    ## Current Conversation
    Below is the current conversation consisting of interleaving human and assistant messages.
    """

    llm = Ollama(model="llama3.1:8b", temperature=0.1, request_timeout=60.0)
    # llm = Ollama(model="deepseek-r1:8b", temperature=0.1,request_timeout=90.0)

    agent = ReActAgent.from_tools(
        [extract_tool, review_tool],
        llm=llm,
        verbose=True,
        max_retries=2,
        max_execution_time=60,
        max_iterations=15
    )

    react_system_prompt = PromptTemplate(system_prompt)
    agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})


    return agent

def process_paper(text: str) -> Dict[str, Any]:
    """Process a research paper to extract and validate data."""
    try:
        agent = get_agent()
        response = agent.chat(text)

        # reset if do not want to maintain history between each JSON entry (faster)
        agent.reset()

        return json.loads(response.response)
    except Exception as e:
        # logger.error(f"Processing error: {e}")
        return {
            "accession_codes": {},
            "sequencing_data": [],
            "source_code": []
        }



if __name__ == "__main__":

    # sample_text = "The whole-exome sequencing and whole genome sequencing datasets generated during this study are available at the Sequence Read Archive (SRA: PRJNA715377). The scRNA-seq and CITE-seq datasets generated during this study are available at the EGA European Genome-Phenome Archive (EGA: EGAS00001004837). High-throughput sequencing (HTS) of T cell receptor \u03b2 (TRB) and T cell receptor \u237a (TRA) dataset are available from Adaptive Biotechnologies (http://clients.adaptivebiotech.com/login; Email: beziat-review@adaptivebiotech.com ; Password: beziat2021review). Primary CD4+ naive T cell RNA-Seq datasets generated during this study are available at the gene expression omnibus: GEO: GSE139299. Lesions RNA-Seq datasets generated during this study are available at the GEO: GSE139259. The assembled genomes are available from GenBank under the accession numbers GenBank: MN605988 and MN605989 for HPV-2 (from P1) and HPV-4 (from P2 and P3), respectively. This study did not generate any unique code. Any other piece of data will be available upon reasonable request."

    # sample_text =     {
    #     "DOI": "https://doi.org/10.1186/s12943-023-01876-x",
    #     "header": "Availability of data and materials",
    #     "paragraph": "\nThe raw sequence data reported in this paper have been deposited in the Genome Sequence Archive in National Genomics Data Center, China National Center for Bioinformation / Beijing Institute of Genomics, Chinese Academy of Sciences (GSA-Human: HRA004998) that are publicly accessible at https://ngdc.cncb.ac.cn/gsa-human. The integrated ST data from 22 tissue slices and their corresponding scRNA-seq data have been deposited in Synapse under the accession code syn51758773 (https://www.synapse.org/#!Synapse:syn51758773/). The analysis and visualization of CAFs in pan-cancer can be performed at https://chenxisd.shinyapps.io/pancaf/. Reanalyzed publicly available scRNA-seq data can be accessed from the GEO database under accession codes: GSE176078 [97], GSE166555 [98], GSE149614 [99], GSE184880 [100], GSE203612 [101], GSE207422 [18], GSE215120 [19], GSE181919 [7]. The scRNA-seq data of PRAD from Chen et al. were downloaded from http://www.pradcellatlas.com/. The scRNA-seq data of BRCA patients receiving pembrolizumab from Bassez et al. were downloaded from https://lambrechtslab.sites.vib.be/en/single-cell [41]. Reanalyzed publicly available ST data can be accessed from the GEO database under accession codes: GSE176078 [97], GSE203612 [101]. The ST data of CRC from Wu et al. were downloaded from http://www.cancerdiversity.asia/scCRLM/ [79]. The ST data for LIHC1, LIHC2, LIHC3, and LIHC4 from Wu et al. were downloaded from http://lifeome.net/supp/livercancer-st/data.htm [102]. The ST data for OVCA_10x were downloaded from https://www.10xgenomics.com/resources/datasets/human-ovarian-cancer-1-standard. The ST data for PRAD1 were downloaded from https://www.10xgenomics.com/resources/datasets/human-prostate-cancer-acinar-cell-carcinoma-ffpe-1-standard. The ST data for PRAD2 were downloaded from https://www.10xgenomics.com/resources/datasets/human-prostate-cancer-adenocarcinoma-with-invasive-carcinoma-ffpe-1-standard-1-3-0. Reanalyzed publicly available RNA-seq data of melanoma patients undergoing immunotherapy (Riaz cohort) can be accessed from the GEO database under accession code GSE91061 [85]. Reanalyzed publicly available RNA-seq data of melanoma patients undergoing immunotherapy (Gide cohort [86] and Nathanson cohort [87]) were downloaded from TIDE database (http://tide.dfci.harvard.edu/) [88].\n",
    #     "PubMed_ID": "77777777"
    # }

    # sample_text={
    #     "DOI": "https://doi.org/10.1186/s12943-024-02017-8",
    #     "header": "Data availability",
    #     "paragraph": "\nNo datasets were generated or analysed during the current study.\n",
    #     "PubMed_ID": "33333333"
    # }

    # sample_text = "All BAM files and associated sample information are deposited in dbGaP under accession phs001087.v4.p1. Single-cell RNA sequencing datasets from this study have been deposited in the Sequence Read Archive with the accession number SUB14118668 (BioProject PRJNA1061081). The analysis files from single-cell RNA sequencing, ecDNA amplicon reconstructions, Incucyte live-cell images, immunofluorescence pRPA and γH2AX foci images, and the according analysis files have been deposited into Zenodo https://doi.org/10.5281/zenodo.11121869129. The TCGA/PCAWG pan-cancer human cancer data22 used for CCND1 amplification analysis was obtained and modified from the supplementary information of that article22. Data for the CCND1 pan-cancer survival analysis was obtained from cBioPortal (https://bit.ly/4cjAYof). Source data are provided with this paper. The following open-source code and databases were used in this article: JaBbA (v.1.1) (https://github.com/mskilab/JaBbA), gGnome (commit c390d80) (https://github.com/mskilab/gGnome), AmpliconArchitect (https://github.com/virajbdeshpande/AmpliconArchitect), FishHook (commit 06e3927) (https://github.com/mskilab/fishHook), MutationTimeR (v.1.00.2) (https://github.com/gerstung-lab/MutationTimeR), deconstructSigs (v.1.9) (https://github.com/raerose01/deconstructSigs), SigProfilerClusters (v.1.1.2) (https://github.com/AlexandrovLab/SigProfilerClusters), Pileup (v.0.15.0) (https://github.com/pysam-developers/pysam), ShortAlignmentMarking (v.2.1) (https://github.com/nygenome/nygc-short-alignment-marking), BWA-MEM (v.0.7.15) (https://github.com/lh3/bwa), GATK (v.4.1.0) (https://github.com/broadinstitute/gatk), MuTect2 (v.4.0.5.1) (https://github.com/broadinstitute/gatk), Strelka2 (v.2.9.3) (https://github.com/Illumina/strelka), Lancet (v.1.0.7) (https://github.com/nygenome/lancet), Svaba (v.0.2.1) (https://github.com/walaj/svaba), Manta (v1.4.0) (https://github.com/Illumina/manta), Lumpy (v.0.2.13) (https://github.com/arq5x/lumpy-sv), SplazerS (v.1.1) (https://github.com/seqan/seqan/tree/master/apps/splazers), Ensembl (v.93) (https://www.ensembl.org), COSMIC (v.86) (https://cancer.sanger.ac.uk), COSMIC Cancer Gene Consensus (v.95) (https://cancer.sanger.ac.uk/census), ClinVar (201706) (https://www.ncbi.nlm.nih.gov/clinvar/), PolyPhen (v.2.2.2) (http://genetics.bwh.harvard.edu/pph2/index.shtml), SIFT (v.5.2.2) (http://sift-dna.org/sift4g), FATHMM (v.2.1) (http://fathmm.biocompute.org.uk), gnomAD (r.2.0.1) (https://gnomad.broadinstitute.org/), gnomAD-SV (v2.0.1) (https://gnomad.broadinstitute.org/, https://github.com/talkowski-lab/gnomad-sv-pipeline), dbSNP (v.150) (https://www.ncbi.nlm.nih.gov/snp/), Variant Effect Predictor (VEP) (v.93.2) (http://www.ensembl.org/vep), Database of Genomic Variants (DGV) (2020-02-25 release) (http://dgv.tcag.ca/), AscatNGS (v.4.2.1) (https://github.com/cancerit/ascatNgs), Sequenza (v.3.0.0) (http://www.cbs.dtu.dk/biotools/sequenza), LICHeE (v1.0) (https://github.com/viq854/lichee), fragCounter (https://github.com/mskilab/fragCounter), dryclean (commit bda8065) (https://github.com/mskilab/dryclean), RepeatMasker (created in 2010 with the original RepBase library from 2010-03-02 and RepeatMasker 3.0.1) (https://www.repeatmasker.org/species/hg.html). Scanpy (v.1.9.6) (https://github.com/scverse/scanpy), GSEApy (v.1.1.1) (https://github.com/zqfang/GSEApy), CycleViz (v.0.1.5) (https://github.com/AmpliconSuite/CycleViz) and CellRanger (v.7.1.0) (https://github.com/10XGenomics/cellranger). Custom analysis scripts and scripts to reproduce figures are available at GitHub (https://github.com/nygenome/UrothelialCancer_WGS_paper_figures). The JaBbA SV browser includes detailed interactive maps of our structure variant calls (https://urothelial-cancer-wcm-2023.nygenome.org/). Image Lab (Bio-Rad v6.1.0) (https://www.bio-rad.com/) was used for western blot image processing and analysis. CytoVision (v.7.3.1) (https://www.leicabiosystems.com/) was used for FISH imaging. Zeiss deconvolution software (Zen desk v.3.7) (https://www.zeiss.com/microscopy/en/products/software/zeiss-zen-desk.html), Fiji ImageJ (v.154f) (https://imagej.net/software/fiji/) and GraphPad Prism (v.10.2.0) (https://www.graphpad.com/) were used for immunofluorescence image processing and analysis. Incucyte software (2022B, Rev2) (https://www.sartorius.com) was used for competitive assays. FlowJo (v.10.10.0) (https://www.flowjo.com/) was used for the analysis of FACS data. R (v.4.0.0) software was used for statistical tests."

    # sample_text = {
    #     "DOI": "https://doi.org/10.1126/scitranslmed.adg5252",
    #     "header": "Data and materials availability:",
    #     "paragraph": "All data associated with this study are in the paper or Supplementary Materials. Sequencing data have been deposited in Genome Expression Omnibus (GEO) under accession number GSE235743 (www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE235743). Scripts for reproducing the analysis can be accessed via Zenodo (DOI 10.5281/zenodo.8011746).",
    #     "PubMed_ID": "37878672",
    #     "journal": "Science Translational Medicine"
    # }


    files = ["test_file_input.json"]

    for file in files:
        print("Filename:", file)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            results = []
            for entry in data:
                doi = entry.get("DOI", "")
                sample_text = entry.get("paragraph", "")
                pmid = entry.get("PubMed_ID", "")

                start_time = time.time()
                result = process_paper(sample_text)
                end_time = time.time()

                results.append({
                        "DOI": doi,
                        "PubMed_ID": pmid,
                        "results": result
                })

            print(f"Extracted and validated data: {results}")
            print("Total execution time: ", end_time-start_time)

            output_path = "test_file_output.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)



    # result = process_paper(sample_text["paragraph"])
    # end_time = time.time()
    # print(f"Extracted and validated data: {json.dumps(result, indent=2)}")
    # print("total execution time: ", end_time-start_time)
