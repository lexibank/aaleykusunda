import csv
import attr
import pathlib
import requests
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank.util import progressbar as pb
from pylexibank import Language, CONCEPTICON_CONCEPTS
from pylexibank.forms import FormSpec
from collections import defaultdict

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Location = attr.ib(default=None)
    Remark = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "aaleykusunda"
    language_class = CustomLanguage
    form_spec = FormSpec(
        brackets={"(": ")"},
        separators = ";,/~",
        missing_data=['*', '---', '-','∅'],
        strip_inside_brackets=True
    )

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        # add concept 
        concepts=args.writer.add_concepts(id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
                                        lookup_factory='Name')
        # add language
        languages=args.writer.add_languages(lookup_factory='Name')
        # add data
        data=self.raw_dir.read_csv('Kusunda_2019_250_lexical_items.tsv', 
                                 delimiter='\t',dicts=True)
        for gloss, entry in pb(list(enumerate(data)), desc='cldfify', total=len(data)):
            if entry['ENGLISH'] in concepts.keys():
                for key, val in languages.items():
                    args.writer.add_forms_from_value(
                        Language_ID=val,
                        Parameter_ID=concepts[entry['ENGLISH']],
                        Value=entry[key],
                        Source=['Bodt2019b']
                    )
            elif entry['ENGLISH'] == 'the barley (Tibetan or highland)':
                for key, val in languages.items():
                    args.writer.add_forms_from_value(
                        Language_ID=val,
                        Parameter_ID=concepts['the barley (tibetan or highland)'],
                        Value=entry[key],
                        Source=['Bodt2019b']
                    )
            elif entry['ENGLISH'] == 'to plant (vegetables, rice)':
                for key, val in languages.items():
                    args.writer.add_forms_from_value(
                        Language_ID=val,
                        Parameter_ID=concepts['to plant (vegetals, rice)'],
                        Value=entry[key],
                        Source=['Bodt2019b']
                    )
            else:
                print(entry['ENGLISH'])