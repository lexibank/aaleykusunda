from setuptools import setup


setup(
    name='cldfbench_aaleykusunda',
    py_modules=['cldfbench_aaleykusunda'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'aaleykusunda=cldfbench_aaleykusunda:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
