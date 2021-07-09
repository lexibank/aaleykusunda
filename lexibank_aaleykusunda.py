import pathlib

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    Location = attr.ib(default=None)
    Remark = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "aaleykusunda"
    language_class = CustomLanguage
    form_spec = pylexibank.FormSpec(separators="~;,/", missing_data=["∅"], first_form_only=True)

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )
        # fix concept lookup
        concepts["the barley (Tibetan or highland)"] = concepts["the barley (tibetan or highland)"]
        concepts["to plant (vegetables, rice)"] = concepts["to plant (vegetals, rice)"]
        args.log.info("added concepts")

        # add language
        languages = args.writer.add_languages(lookup_factory="Name")
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
            "Kusunda_2019_250_lexical_items.tsv", delimiter="\t", dicts=True
        )
        # add data
        for entry in pylexibank.progressbar(data, desc="cldfify", total=len(data)):
            if entry["ENGLISH"] in concepts.keys():
                for key, val in languages.items():
                    args.writer.add_forms_from_value(
                        Language_ID=val,
                        Parameter_ID=concepts[entry["ENGLISH"]],
                        Value=entry[key],
                        Source=["Bodt2019b"],
                    )
