from setuptools import setup
import json

with open("metadata.json") as fp:
    metadata = json.load(fp)

setup(
    name='lexibank_aaleykusunda',
    py_modules=['lexibank_aaleykusunda'],
    include_package_data=True,
    url=metadata.get("url",""),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'aaleykusunda=lexibank_aaleykusunda:Dataset',
        ]
    },
    install_requires=[
        "pylexibank>=2.1"
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
