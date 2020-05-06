import subprocess
import os

setting = {"semrep_path":"path","semrep_cmd":"cmd"}

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

