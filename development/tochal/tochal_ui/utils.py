import yaml


def read_bytes(f):
    nlu = yaml.load(f)['nlu']
    texts = []
    for intent in nlu:
        examples = intent['examples']
        for example in examples.split("\n"):
            example = example.replace("-", "")
            if example.strip() != "":
                texts.append(example.strip())

    return texts
