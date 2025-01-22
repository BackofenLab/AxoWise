import logging
from typing import Dict, Any
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import PromptTemplate
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_data(text: str) -> str:
    """Extracts source code URLs and accession codes from scientific text."""
    
    prompt = f"""You are a highly precise extraction tool. Your task is to extract source code URLs and accession codes from scientific text.

Return the results **only** in valid JSON format with **no additional text**. Follow this format exactly:
{{
    "source_code": ["GitHub_URL", "Zenodo_URL"],
    "accession_codes": {{
        "database_name": ["accession_code1", "accession_code2"]
    }}
}}

Strict Extraction Rules:
1. Source Code URLs:
   - ONLY include GitHub or Zenodo URLs for sequencing data or source code that are explicitly mentioned
   - Do NOT include Github URLs for libraries or softwares
   - Do NOT infer or generate URLs that aren't in the text
   - If text states "no code" or similar, return empty list
   - Return empty list if no GitHub/Zenodo URLs found

2. Accession Codes - Extract ALL of these formats:
   - GEO: starts with GSE, GSM, GPL
   - SRA: starts with SRP, SRR, SRS, SRX, PRJNA
   - ENA: starts with ERA, ERP, ERR, ERS, ERX
   - EGA: starts with EGAS, EGAD, EGAF
   - GenBank: format like MN123456, NC_123456
   - ArrayExpress: starts with E-MTAB, E-GEOD
   - DDBJ: starts with DRA, DRP, DRR
   
3. Format Rules:
   - Include database name ONLY if it has codes
   - Remove any empty arrays or objects
   - Match database names exactly as written in text
   - Extract ALL accession numbers, even if multiple per database

Input Text to Process:
{text}
"""
    try:
        response = llm.complete(prompt).text.strip()
        result = json.loads(response)
        logger.info(result)
        
        # Validate structure
        if not isinstance(result.get('source_code', []), list):
            raise ValueError("source_code must be a list")
        if not isinstance(result.get('accession_codes', {}), dict):
            raise ValueError("accession_codes must be a dictionary")
            
        logger.info(f"Extraction result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return json.dumps({
            "source_code": [],
            "accession_codes": {}
        })



def review_data(text: str, extracted_data: str) -> str:
    """Validates extracted data against the original text."""

    prompt = f"""You are a validation tool. Return EXACTLY and ONLY a JSON object matching this structure - NO additional text or explanation:

{{
    "is_valid": true,
    "validation": {{
        "source_code": {{
            "valid_count": 0,
            "invalid_count": 0
        }},
        "accession_codes": {{
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
   
Input Text to validate against:
{text}

Extracted data to validate:
{extracted_data}

Return the results **only** in valid JSON format with **no additional text**. Follow this format exactly:
{{
    "source_code": ["GitHub_URL", "Zenodo_URL"],
    "accession_codes": {{
        "database_name": ["accession_code1", "accession_code2"]
    }}
}}
"""
        
    try:
        response = llm.complete(prompt).text.strip()
        # Remove any markdown code blocks if present
        response = response.replace('```json', '').replace('```', '').strip()
        
        logger.info(f"Review raw response: {response}")
        result = json.loads(response)
        logger.info(f"Review result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        logger.error(f"Review error: {e}")
        return json.dumps({
            "is_valid": False,
            "validation": {
                "source_code": {
                    "valid_count": 0,
                    "invalid_count": 0
                },
                "accession_codes": {
                    "valid_count": 0,
                    "invalid_count": 0
                }
            }
        })

# Create function tools
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

# Setup LLM and Agent
llm = Ollama(model="llama3.1:8b", temperature=0.1, request_timeout=60.0)
# llm = Ollama(model="deepseek-r1:8b", temperature=0.1,request_timeout=90.0)

agent = ReActAgent.from_tools(
    [extract_tool, review_tool],
    llm=llm,
    verbose=True,
    max_retries=2,    # Add retry limit
    max_execution_time=60,
    max_iterations=15
)

# Custom system prompt
system_prompt = """You are designed to extract and validate source code URLs and accession codes from scientific text.

## Tools
You have access to these tools:
{tool_desc}

## Process
1. First extract data using extract_data
2. Then validate using review_data
3. If validation fails, try extraction again

## Output Format
Please use this format:

Thought: I need to [action] because [reason]
Action: tool name
Action Input: {{"text": "input text"}}

Return **ONLY** the JSON object with no additional text before or after the JSON object.

When validation is successful:
Thought: Extraction and validation complete
Answer: [final extracted and validated data]

## Current Conversation
Below is the current conversation:
"""

# Update agent prompt
react_system_prompt = PromptTemplate(system_prompt)
agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

# Reset agent
agent.reset()

def process_paper(text: str) -> Dict[str, Any]:
    """Process a research paper to extract and validate data."""
    try:
        response = agent.chat(text)
        return json.loads(response.response)
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return {
            "source_code": [],
            "accession_codes": {}
        }

# Example usage
if __name__ == "__main__":

    # sample_text = "The whole-exome sequencing and whole genome sequencing datasets generated during this study are available at the Sequence Read Archive (SRA: PRJNA715377). The scRNA-seq and CITE-seq datasets generated during this study are available at the EGA European Genome-Phenome Archive (EGA: EGAS00001004837). High-throughput sequencing (HTS) of T cell receptor \u03b2 (TRB) and T cell receptor \u237a (TRA) dataset are available from Adaptive Biotechnologies (http://clients.adaptivebiotech.com/login; Email: beziat-review@adaptivebiotech.com ; Password: beziat2021review). Primary CD4+ naive T cell RNA-Seq datasets generated during this study are available at the gene expression omnibus: GEO: GSE139299. Lesions RNA-Seq datasets generated during this study are available at the GEO: GSE139259. The assembled genomes are available from GenBank under the accession numbers GenBank: MN605988 and MN605989 for HPV-2 (from P1) and HPV-4 (from P2 and P3), respectively. This study did not generate any unique code. Any other piece of data will be available upon reasonable request."
    
    sample_text = "All BAM files and associated sample information are deposited in dbGaP under accession phs001087.v4.p1. Single-cell RNA sequencing datasets from this study have been deposited in the Sequence Read Archive with the accession number SUB14118668 (BioProject PRJNA1061081). The analysis files from single-cell RNA sequencing, ecDNA amplicon reconstructions, Incucyte live-cell images, immunofluorescence pRPA and γH2AX foci images, and the according analysis files have been deposited into Zenodo https://doi.org/10.5281/zenodo.11121869129. The TCGA/PCAWG pan-cancer human cancer data22 used for CCND1 amplification analysis was obtained and modified from the supplementary information of that article22. Data for the CCND1 pan-cancer survival analysis was obtained from cBioPortal (https://bit.ly/4cjAYof). Source data are provided with this paper. The following open-source code and databases were used in this article: JaBbA (v.1.1) (https://github.com/mskilab/JaBbA), gGnome (commit c390d80) (https://github.com/mskilab/gGnome), AmpliconArchitect (https://github.com/virajbdeshpande/AmpliconArchitect), FishHook (commit 06e3927) (https://github.com/mskilab/fishHook), MutationTimeR (v.1.00.2) (https://github.com/gerstung-lab/MutationTimeR), deconstructSigs (v.1.9) (https://github.com/raerose01/deconstructSigs), SigProfilerClusters (v.1.1.2) (https://github.com/AlexandrovLab/SigProfilerClusters), Pileup (v.0.15.0) (https://github.com/pysam-developers/pysam), ShortAlignmentMarking (v.2.1) (https://github.com/nygenome/nygc-short-alignment-marking), BWA-MEM (v.0.7.15) (https://github.com/lh3/bwa), GATK (v.4.1.0) (https://github.com/broadinstitute/gatk), MuTect2 (v.4.0.5.1) (https://github.com/broadinstitute/gatk), Strelka2 (v.2.9.3) (https://github.com/Illumina/strelka), Lancet (v.1.0.7) (https://github.com/nygenome/lancet), Svaba (v.0.2.1) (https://github.com/walaj/svaba), Manta (v1.4.0) (https://github.com/Illumina/manta), Lumpy (v.0.2.13) (https://github.com/arq5x/lumpy-sv), SplazerS (v.1.1) (https://github.com/seqan/seqan/tree/master/apps/splazers), Ensembl (v.93) (https://www.ensembl.org), COSMIC (v.86) (https://cancer.sanger.ac.uk), COSMIC Cancer Gene Consensus (v.95) (https://cancer.sanger.ac.uk/census), ClinVar (201706) (https://www.ncbi.nlm.nih.gov/clinvar/), PolyPhen (v.2.2.2) (http://genetics.bwh.harvard.edu/pph2/index.shtml), SIFT (v.5.2.2) (http://sift-dna.org/sift4g), FATHMM (v.2.1) (http://fathmm.biocompute.org.uk), gnomAD (r.2.0.1) (https://gnomad.broadinstitute.org/), gnomAD-SV (v2.0.1) (https://gnomad.broadinstitute.org/, https://github.com/talkowski-lab/gnomad-sv-pipeline), dbSNP (v.150) (https://www.ncbi.nlm.nih.gov/snp/), Variant Effect Predictor (VEP) (v.93.2) (http://www.ensembl.org/vep), Database of Genomic Variants (DGV) (2020-02-25 release) (http://dgv.tcag.ca/), AscatNGS (v.4.2.1) (https://github.com/cancerit/ascatNgs), Sequenza (v.3.0.0) (http://www.cbs.dtu.dk/biotools/sequenza), LICHeE (v1.0) (https://github.com/viq854/lichee), fragCounter (https://github.com/mskilab/fragCounter), dryclean (commit bda8065) (https://github.com/mskilab/dryclean), RepeatMasker (created in 2010 with the original RepBase library from 2010-03-02 and RepeatMasker 3.0.1) (https://www.repeatmasker.org/species/hg.html). Scanpy (v.1.9.6) (https://github.com/scverse/scanpy), GSEApy (v.1.1.1) (https://github.com/zqfang/GSEApy), CycleViz (v.0.1.5) (https://github.com/AmpliconSuite/CycleViz) and CellRanger (v.7.1.0) (https://github.com/10XGenomics/cellranger). Custom analysis scripts and scripts to reproduce figures are available at GitHub (https://github.com/nygenome/UrothelialCancer_WGS_paper_figures). The JaBbA SV browser includes detailed interactive maps of our structure variant calls (https://urothelial-cancer-wcm-2023.nygenome.org/). Image Lab (Bio-Rad v6.1.0) (https://www.bio-rad.com/) was used for western blot image processing and analysis. CytoVision (v.7.3.1) (https://www.leicabiosystems.com/) was used for FISH imaging. Zeiss deconvolution software (Zen desk v.3.7) (https://www.zeiss.com/microscopy/en/products/software/zeiss-zen-desk.html), Fiji ImageJ (v.154f) (https://imagej.net/software/fiji/) and GraphPad Prism (v.10.2.0) (https://www.graphpad.com/) were used for immunofluorescence image processing and analysis. Incucyte software (2022B, Rev2) (https://www.sartorius.com) was used for competitive assays. FlowJo (v.10.10.0) (https://www.flowjo.com/) was used for the analysis of FACS data. R (v.4.0.0) software was used for statistical tests."


    result = process_paper(sample_text)
    print(f"Extracted and validated data: {json.dumps(result, indent=2)}")