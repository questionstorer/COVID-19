import subprocess
import os
import mysql.connector


setting = {"semrep_path":"path","semrep_cmd":"cmd"}
entity_types = set(['T047', 'T028', 'T121', 'T103', 'T184'])
# mapping for parsing results
mappings = {
        "text": {
            "sent_id": 4,
            "sent_text": 6
        },
        "entity": {
            'cuid': 6,
            'label': 7,
            'sem_types': 8,
            'score': 15
        },
        "relation": {
            'subject__cui': 8,
            'subject__label': 9,
            'subject__sem_types': 10,
            'subject__sem_type': 11,
            'subject__score': 18,
            'predicate__type': 21,
            'predicate': 22,
            'negation': 23,
            'object__cui': 28,
            'object__label': 29,
            'object__sem_types': 30,
            'object__sem_type': 31,
            'object__score': 38,
        }
    }


def runProcess(cmd):
    # retrieve result from SemRep
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        shell=True)
    binary_lines = p.stdout.readlines()
    lines = [line.decode('ascii') for line in binary_lines]
    return lines

class SemRep:
    def __init__(self):
        self.setting = setting
    def extract_relation(self, text):
        # construct cmd
        cmd = "echo" + text + " | " + os.path.join(setting["semrep_path"], setting["semrep_cmd"])
        # get lines
        lines = runProcess(cmd)
        # parse lines
        result = self.__parse_lines(lines)

        return result
    def __parse_lines(self, lines):
        results = {'relations': [], 'text': text}
        for line in lines:
            # If Sentence
            if line.startswith('SE'):
                if elements[5] == 'relation':
                    tmp = {}
                    for key, ind in mappings['relation'].items():
                        if 'sem_types' in key:
                            tmp[key] = elements[ind].split(',')
                        else:
                            tmp[key] = elements[ind]
                    results['relations'].append(tmp)
        return results


def filter_relations(cursor, relations):
    '''
        filter relations based on entity type.
        current valid entity types are in entity_types
        relation is a list consisting of dictionary with keys: subject_cui, object_cui, predicate
    '''
    filtered_relations = []
    
    for relation in relations:
        if verify_entity(cursor, relation[0],entity_types) and verify_entity(cursor, relation[2],entity_types):
            # split relation by ( to get rid of (SPEC), (INFE)
            relation = (relation[0], relation[1].split("(")[0], relation[2])
            filtered_relations.append(relation)
        
            
    return filtered_relations

def filter_entities(cursor, entities):
    filtered_entities = []
    for entity in entities:
        if verify_entity(cursor, entity[2], entity_types):
            filtered_entities.append(entity)
    return filtered_entities



def get_types(cursor, cui):
    '''
        get semantic type of an entity
    '''
    query = ("select tui from umls.mrsty where cui=%s")
    cursor.execute(query, (cui,))
    
    tuis = set()
    
    for message in cursor:
        tuis.add(message[0])
    return tuis
    
def get_oneof_type(cursor, cui,entity_types):
    '''
        get one of the semantic type in the entity_type if multiple types are returned
    '''
    tuis = get_types(cursor, cui)
    types = tuis.intersection(entity_types)
    return types
    
    
def verify_entity(cursor, cui, entity_types):
    '''
        verify cui is one of the entity_types
    '''
    tuis = get_types(cursor, cui)
    
    if tuis.isdisjoint(entity_types):
        return False
    else:
        return True