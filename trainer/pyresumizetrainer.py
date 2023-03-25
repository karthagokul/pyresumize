from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import sys

sys.path.append("../src")
from pyresumize.utilities import Utilities

nlp = spacy.blank("en")  # For new model creation
# nlp = spacy.load("en_core_web_sm")  # To train the existing model with new parameters


class BaseTrainer:
    def __init__(self, nlp) -> None:
        self.nlp = nlp
        self.training_data = []

    def set_data(self, csv_folder, column_index, entity_name):
        pyresutil = Utilities()
        items = pyresutil.generate_keywords_from_csv_files(csv_folder, column_index)
        for item in items:
            item_str = str(item)
            tupledetails = {}
            entry_tuple = ()
            entity_list = []
            schema_tuple = (0, len(item_str), entity_name)
            entity_list.append(schema_tuple)
            tupledetails["entities"] = entity_list
            entry_tuple = (item_str, tupledetails)
            self.training_data.append(entry_tuple)

        print(self.training_data)

        print("Created a data set of  %d entries as %s" % (len(items), entity_name))
        return

    def generate(self, filename):
        for text, annot in tqdm(self.training_data):
            doc = self.nlp.make_doc(text)  # create doc object from text
            ents = []
            for start, end, label in annot["entities"]:  # add character indexes
                # print(start)
                # print(end)
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print("Skipping entity")
                else:
                    ents.append(span)
                    # print("Appending")
                    # print(span)
                    # print(label)
            doc.ents = ents  # label the text with the ents
            db.add(doc)
        db.to_disk(filename)


db = DocBin()
trainer = BaseTrainer(nlp)
trainer.set_data("../data/employers/", 0, "ORG")
trainer.generate("./pyresumize_employers.spacy")
