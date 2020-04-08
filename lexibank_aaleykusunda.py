import re
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
    Location = attr.ib(default=None)
    Remark = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "aaleykusunda"
    language_class = CustomLanguage
    form_spec = FormSpec(
        separators="~;,/",
        missing_data=['∅'],
        first_form_only=True
    )

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info('added sources')

        # add concept
        concepts = args.writer.add_concepts(id_factory=lambda c: c.id.split(
            "-")[-1] + "_" + slug(c.english), lookup_factory='Name')
        # fix concept (concepticon source, data concept)
        fix_concept = [
            ('the barley (tibetan or highland)',
             'the barley (Tibetan or highland)'),
            ('to plant (vegetals, rice)',
             'to plant (vegetables, rice)')]
        for c in fix_concept:
            if c[0] in concepts.keys():
                concepts[c[1]] = concepts[c[0]]
                del concepts[c[0]]
        args.log.info('added concepts')

        # add language
        languages = args.writer.add_languages(lookup_factory='Name')
        args.log.info('added languages')

        # read in data
        data = self.raw_dir.read_csv('Kusunda_2019_250_lexical_items.tsv',
                                     delimiter='\t', dicts=True)
        # add data
        for gloss, entry in pb(list(enumerate(data)),
                               desc='cldfify', total=len(data)):
            if entry['ENGLISH'] in concepts.keys():
                for key, val in languages.items():
                    args.writer.add_forms_from_value(
                        Language_ID=val,
                        Parameter_ID=concepts[entry['ENGLISH']],
                        Value=entry[key],
                        Source=['Bodt2019b']
                    )
