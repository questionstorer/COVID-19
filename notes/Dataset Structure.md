# Dataset Structure

- paper_id: sha1 of PDF file

- metadata:
  
  - title:
  
  - authors: list of authors, each has
    
    - first
    
    - middle
    
    - last
    
    - sufix
    
    - affiliation
    
    - email
  
  - abstract: list of paragrpahs in abstract, each has
    
    - text:
    
    - cite_span: list of citation in the paragraph, each has
      
      - start:
      
      - end
      
      - text
      
      - ref_id
    
    - ref_spans: list of cross reference in the paragrpah, same as cite_span
    
    - section: "Abstract"
  
  - body_text: list of paragrpahs in full text, each has
    
    - text:
    
    - cite_spans:
    
    - ref_spans
    
    - eq_spans:
    
    - section:
  
  - bib_entries: dictionary of references in text:
    
    - 

```json
{    # 40-character sha1 of the PDF
    "paper_id": <str>,               

    "metadata": {
        "title": <str>,
        # list of author dicts, in order
        "authors": [               

            {
                "first": <str>,
                "middle": <list of str>,
                "last": <str>,
                "suffix": <str>,
                "affiliation": <dict>,
                "email": <str>
            },
            ...
        ],
        # list of paragraphs in the abstract
        "abstract": [           

            {
                "text": <str>,
                # list of character indices of inline citations e.g. citation "[7]" occurs at positions 151-154 in "text" linked to bibliography entry BIBREF3
                "cite_spans": [   
                    {
                        "start": 151,
                        "end": 154,
                        "text": "[7]",
                        "ref_id": "BIBREF3"
                    },
                    ...
                ],
                # e.g. inline reference to "Table 1"
                "ref_spans": <list of dicts similar to cite_spans>,     
                "section": "Abstract"
            },
            ...
        ],
        # list of paragraphs in full body
        "body_text": [                      
            # paragraph dicts look the same as above

            {
                "text": <str>,
                "cite_spans": [],
                "ref_spans": [],
                "eq_spans": [],
                "section": "Introduction"
            },
            ...
            {
                ...,
                "section": "Conclusion"
            }
        ],
        "bib_entries": {
            "BIBREF0": {
                "ref_id": <str>,
                "title": <str>,
                # same structure as earlier, but without `affiliation` or `email`

                "authors": <list of dict> 

                "year": <int>,
                "venue": <str>,
                "volume": <str>,
                "issn": <str>,
                "pages": <str>,
                "other_ids": {
                    "DOI": [
                        <str>
                    ]
                }
            },
            "BIBREF1": {},
            ...
            "BIBREF25": {}
        },
        "ref_entries":
            "FIGREF0": {
                # figure caption text
                "text": <str>,                  
                "type": "figure"
            },
            ...
            "TABREF13": {
                # table caption text
                "text": <str>,                  
                "type": "table"
            }
        },
        # same structure as body_text
        "back_matter": <list of dict>           
    }
}
```


