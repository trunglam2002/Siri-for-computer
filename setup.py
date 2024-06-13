import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.0.0'

REPO_NAME = 'siri for computer'
AUTHOR_USER_NAME = 'trunglam2002'
SRC_REPO = 'siri for computer'
AUTHOR_EMAIL = 'trunglam2002@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='python package for siri computer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/trunglam2002/Siri-for-computer',
    project_urls={
        'Bug Tracker': 'https://github.com/trunglam2002/Siri-for-computer/issues',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src')
)
