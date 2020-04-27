# Biomedical Knowledge graphs

- [Bio2RDF]([https://github.com/bio2rdf/bio2rdf-scripts/wiki](https://github.com/bio2rdf/bio2rdf-scripts/wiki) 

- [BioGrakn]([https://github.com/graknlabs/biograkn](https://github.com/graknlabs/biograkn) 

- [UMLS]([https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)

- [BioGraph]([http://biograph.pa.icar.cnr.it/#dbschema](http://biograph.pa.icar.cnr.it/#dbschema) 

## Bio2RDF

Semantic Network of linked data of life science.

## BioGrakn

KG of biomedical data

## BioGraph

bioinformatic KG built on top of OrientDB. Mostly about Gene and Protein.

Schema:

![](C:\Users\hongm\AppData\Roaming\marktext\images\2020-04-06-14-28-22-image.png)

| Nodes       | Properties                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gene        | geneId (String)<br>locusTag (String)<br>chromosome (String)<br>mapLocation (String)<br>description (String)<br>type (String)<br>nomenclatureAuthoritySymbol (String)<br>nomenclatureAuthorityFullName (String)<br>nomenclatureStatus (String)<br>otherDesignations (String)                                                                                                                                                                                                                                                           |
| GeneName    | symbol (String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Go          | goId (String)<br>name (String)<br>namespace (String)<br>definition (String)<br>obsolete (String)<br>comment (String)                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Protein     | name (String)<br>fullName (String)<br>alternativeName (String)<br>gene (String)<br>sequence (String)<br>sequenceLenght (Int)<br>sequenceMass (Int)                                                                                                                                                                                                                                                                                                                                                                                    |
| ProteinName | name (String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Pathway     | pathwayId (String)<br>name (String)<br>summation (String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Cancer      | name (String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| MiRNA       | accession (String)<br>name (String)<br>description (String)<br>comment (String)<br>sequence (String)                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| MiRNAmature | ...<br>location (String)<br>sequence (String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| MiRNASNP    | SNPid (String)<br>miRNA (String)<br>chr (String)<br>miRstart (Int)<br>miRend (Int)<br>lostNum (Int)<br>gainNum (Int)                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Interaction | transcriptId (String)<br>extTranscriptId (String)<br>mirAlignment (String)<br>alignment (String)<br>geneAlignment (String)<br>mirStart (Int)<br>mirEnd (Int)<br>geneStart (Int)<br>geneEnd (Int)<br>genomeCoordinates (String)<br>conservation (Double)<br>alignScore (Int)<br>seedCat (Int)<br>energy (Double)<br>mirSvrScore (String)<br><br>mirTarBaseId (String)<br>experiments (String)<br>supportType (String)<br><br>snpEnergy (Double)<br>basePair (String)<br>geneAve (Double)<br>mirnaAve (Double)<br><br>database (String) |

| Relations         | Properties                                                   |
| ----------------- | ------------------------------------------------------------ |
| ANNOTATES         | evidence (String)<br>qualifier (String)<br>category (String) |
| SYNONYM_OF        | -                                                            |
| CODING            | -                                                            |
| CONTAINS          | -                                                            |
| REFERS_TO         | -                                                            |
| CANCER2MIRNA      | profile (String)                                             |
| PRECURSOR_OF      | -                                                            |
| HAS_SNP           | -                                                            |
| INTERACTING_GENE  | -                                                            |
| INTERACTING_MIRNA | -                                                            |
| INTERACTING_SNP   | -                                                            |
