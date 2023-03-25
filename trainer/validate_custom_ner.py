import spacy

nlp = spacy.load(R"../output/pyresumize_employers/model-best")  # load the drug pipeline


doc = nlp("India is a beautiful country , Indians are brothers and sisters .Gokul Work in Emudhra")
for ent in doc.ents:
    print(ent.text)
    print(ent.label_)
