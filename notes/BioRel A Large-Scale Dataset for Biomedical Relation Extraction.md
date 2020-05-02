# BioRel: A Large-Scale Dataset for Biomedical Relation Extraction

large dataset constructed using UMLS as knowledge base, Medline as corpus. Entity in sentences of Medline are identified and lined to UMLS using MetaMap..

Use distant supervision to recognize relation labels.

**Medline**: Medline is the U.S. National Library of Medicine (NLM) premier bibliographic database that contains more than 25 million references to journal articles in life sciences with a concentration on biomedicine, which is freely available on the Internet.

**UMLS**: The knowledge in Metathesaurus are orgnized into vocabularies associated with certain topics. In this work, we select only two vocabularies: NDFRT (National Drug File - Reference Terminology) and NCI (National Cancer Institute). NDFRT defines relations that connect drugs to diseases and NCI contains information related to genes and cancer.

**Metamap**: MetaMap, a highly configurable program to discover UMLS Metathesaurus entities referred to biomedical texts. MetaMap uses a knowledge-instensive approach based on symbolic, natural-language processing and computational-linguistic techniques.

## Approach

1. identify entities in Medline sentences using MetaMap and link them to UMLS

2. label relation between entities according to UMLS relations. For sentence in Medline containing head and tail entities $(e_1, e_2)$, if there exist $(e_1,e_2,r)$ for some $r$ in Metathesaurus, denote the sentence with that label $r$

3. Filter some relation based on some rule.
