class InputExample:
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text):
        """Constructs a InputExample.

    Args:
      guid: Unique id for the example.
      text_a: string. The untokenized text of the first sequence. For single
        sequence tasks, only this sequence must be specified.
    """
        self.guid = guid
        self.text = text

class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self,
        input_ids,
        input_mask):
        self.input_ids = input_ids
        self.input_mask = input_mask

def example2feature(example, tokenizer, max_seq_length):
    # convert examples to features

    # tokenize sentence
    tokens = tokenizer.tokenize(example.text)
    print("tokens:", tokens)
    if len(tokens) > max_seq_length - 2:
        tokens = tokens[0:(max_seq_length - 2)]
    # append [CLS] and [SEP] at beginning and end
    tokens = ["[CLS]"] + tokens + ["[SEP]"]
    # convert tokens to id
    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    # mask has 1 for real tokens and 0 for padding tokens
    input_mask = [1] * len(input_ids)

    # zero padding masks
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)

    return InputFeatures(input_ids, input_mask)