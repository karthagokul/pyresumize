import spacy

nlp = spacy.load("../output/pyresumize_employers/model-best")


def ent(doc):
    global nlp
    return [x for x in (nlp(doc)).ents if x.label_ == "ORG"]


text = "Gokul Kartha is an Indian"
doc = nlp(text)
for x in (nlp(doc)).ents:
    # if x.label_=="ORG":
    print(x.text)
    print(x.label_)

# company_names = ent(doc)
# print(company_names)
