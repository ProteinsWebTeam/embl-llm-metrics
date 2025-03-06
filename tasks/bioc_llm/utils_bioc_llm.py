from typing import Dict, List
import re
from functools import partial

def standardize(l: List[str]):
    new_l = []
    for e in l:
        new_e = e.strip()
        new_e = new_e.replace("'", "\"")
        new_l.append(new_e)
    return new_l

def compute_precision(target: List[str], results: List[str]):
    std_target = standardize(target)
    std_results = standardize(results)
    tp_list = list(set(std_target).intersection(set(std_results)))
    fp_list = list(set(std_results).difference(set(std_target)))
    tp = len(tp_list)
    fp = len(fp_list)
    if (tp + fp > 0):
        return tp/(tp + fp)
    else:
        return 0


def compute_f1(recall: float, precision: float):
    denominator = recall + precision
    if (denominator > 0):
        return 2*(recall*precision)/denominator
    else:
        return 0


def compute_accuracy(target: List[str], results: List[str]):
    pass


def compute_recall(target: List[str], results: List[str]):
    std_target = standardize(target)
    std_results = standardize(results)
    tp_list = list(set(std_target).intersection(set(std_results)))
    fn_list = list(set(std_target).difference(set(std_results)))
    tp = len(tp_list)
    fn = len(fn_list)
    if (tp + fn > 0):
        return tp/(tp + fn)
    else:
        return 0


def doc_to_target(doc: Dict) -> List[str]:
    ann_regex = re.compile("<annotation[^>]*>")
    targets = [x for x in ann_regex.findall(doc["annotations"])]
    return targets


def process_results(doc, resps):
    targets = doc_to_target(doc)
    recall = compute_recall(targets, resps[0])
    precision = compute_precision(targets, resps[0])
    f1 = compute_f1(recall, precision)
    print(recall, precision, f1)
    
    return {
         "recall": recall,
         "precision": precision,
         "f1": f1
    }

def doc_to_text(doc: Dict, type: str):
    sentence = doc["sentence"]
    message = f"""
            ### INTRO
            You are an ER extraction expert. 
            You will be provided with parts of scientific papers containing words or phrases classifiable with the following categories:
            protein_type,
            taxonomy_domain,
            protein,
            structure_element,
            evidence,
            protein_state,
            site,
            chemical,
            residue_name,
            experimental_method,
            species,
            residue_range,
            ptm,
            complex_assembly,
            mutant,
            residue_name_number,
            gene,
            oligomeric_state,
            residue_number

            ### INSTRUCTIONS

            You are going to output XML-formatted annotation in the following format. 

            <annotation entity="ENTITY_NAME" type="ENTITY_CATEGORY"/> 
            <annotation entity="ENTITY_NAME" type="ENTITY_CATEGORY"/>
            ......


            ### EXAMPLES
            Sentence
            Petal break-strength assays measure the force (expressed in gram equivalents) required to remove the petals from the flower of serk mutant plants compared to haesa/hsl2 mutant and Col-0 wild-type flowers.
            Annotations
            <annotation entity="serk" type="gene"/> 

            Sentence
            SDS PAGE analysis of the purified Arabidopsis thaliana HAESA ectodomain (residues 20–620) obtained by secreted expression in insect cells.
            Annotations
            <annotation entity="Arabidopsis thaliana" type="species"/> <annotation entity="20–620" type="residue_range"/> 

            Sentence
            A central hydroxyproline residue anchors IDA to the receptor.
            Annotations
            <annotation entity="hydroxyproline" type="residue_name"/> 

            Sentence
            Close-up views of (A) IDA, (B) the N-terminally extended PKGV-IDA and (C) IDL1 bound to the HAESA hormone binding pocket (in bonds representation, in yellow) and including simulated annealing 2Fo–Fc omit electron density maps contoured at 1.0 σ.
            Annotations
            <annotation entity="PKGV-IDA" type="mutant"/> 

            Sentence
            Crystal structures of HAESA in complex with IDA reveal a hormone binding pocket that accommodates an active dodecamer peptide.
            Annotations
            <annotation entity="Crystal structures" type="evidence"/> <annotation entity="in complex with" type="protein_state"/> <annotation entity="hormone binding pocket" type="site"/> <annotation entity="peptide" type="chemical"/> 

            Sentence
            Floral abscission is controlled by the leucine-rich repeat receptor kinase (LRR-RK) HAESA and the peptide hormone IDA.
            Annotations
            <annotation entity="HAESA" type="protein"/> 

            Sentence
            For subunit β1, this process was previously inferred to require that the propeptide residue at position (-2) of the subunit precursor occupies the S1 specificity pocket of the substrate-binding channel formed by amino acid 45 (for details see Supplementary Note 2).
            Annotations
            <annotation entity="(-2)" type="residue_number"/> 

            Sentence
            Here we show that IDA is sensed directly by the HAESA ectodomain.
            Annotations
            <annotation entity="ectodomain" type="structure_element"/> 

            Sentence
            Mechanistic insight into a peptide hormone signaling complex mediating floral organ abscission
            Annotations
            <annotation entity="peptide hormone" type="protein_type"/> 

            Sentence
            Note that Pro58IDA and Leu67IDA are the first residues defined by electron density when bound to the HAESA ectodomain. (D) Table summaries for equilibrium dissociation constants (Kd), binding enthalpies (ΔH), binding entropies (ΔS) and stoichiometries (N) for different IDA peptides binding to the HAESA ectodomain (± fitting errors; n.d.).
            Annotations
            <annotation entity="Pro58" type="residue_name_number"/> 

            Sentence
            Plants constantly renew during their life cycle and thus require to shed senescent and damaged organs.
            Annotations
            <annotation entity="Plants" type="taxonomy_domain"/> 

            Sentence
            Santiago et al. used protein biochemistry, structural biology and genetics to uncover how the IDA hormone activates HAESA.
            Annotations
            <annotation entity="protein biochemistry" type="experimental_method"/> 

            Sentence
            The HAESA LRR domain elutes as a monomer (black dotted line), as does the isolated SERK1 ectodomain (blue dotted line).
            Annotations
            <annotation entity="monomer" type="oligomeric_state"/> 

            Sentence
            The IDA-HAESA and SERK1-HAESA complex interfaces are conserved among HAESA and HAESA-like proteins from different plant species.
            Annotations
            <annotation entity="IDA-HAESA" type="complex_assembly"/> 

            Sentence
            The N- (residues 20–88) and C-terminal (residues 593–615) capping domains are shown in yellow, the central 21 LRR motifs are in blue and disulphide bonds are highlighted in green (in bonds representation). (C) Structure-based sequence alignment of the 21 leucine-rich repeats in HAESA with the plant LRR consensus sequence shown for comparison.
            Annotations
            <annotation entity="disulphide bonds" type="ptm"/> 


            ### INPUT
            Extract from the following text:
            {sentence}
            """

        return message

doc_to_text_api = partial(doc_to_text, type="api")
doc_to_text_hf = partial(doc_to_text, type="hf")

