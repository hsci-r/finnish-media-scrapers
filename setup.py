from setuptools import setup, find_packages

with open('README.md') as fp:
    README = fp.read()

setup(
    name='finnish-media-scrapers',
    version='0.1.0',
    author='Human Sciences - Computing Interaction Research GRoup',
    author_email='eetu.makela@helsinki.fi',
    description='Scrapers for extracting articles from Finnish journalistic media websites.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages('.', exclude=['tests', 'tests.*']),
    package_dir={'': '.'},
    test_suite='tests',
    install_requires=['lxml','requests','beautifulsoup4','selenium'],
    entry_points={
        'console_scripts' : [
            'query-yle = finnish_media_scrapers.scripts.query_yle:main',
            'query-is = finnish_media_scrapers.scripts.query_is:main'
        ]
    }
)


