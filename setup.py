from setuptools import setup, find_packages

long_desc = ""
try:
    import pypandoc
    long_desc = pypandoc.convert('README.md', 'rst', extra_args = ('--eol', 'lf'))
except(IOError, ImportError):
    long_desc = open('README.md').read()

setup(
    name = "aav.upcoming-games",
    version = "0.1.0",
    description = "Reddit bot to provide updates for video games.",
    long_description = long_desc,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points = {
        'console_scripts': [
            'upcoming-games = upcoming_games:main'
        ]
    },
    keywords = "aav upcoming games reddit bot",
    author = "aav-bots",
    url = "https://github.com/aav-bots/upcoming-games",
    license = "MIT",
    packages = find_packages(),
    install_requires = [
        "praw",
        "requests",
        "ruamel.yaml",
        "parsedatetime",
        "beautifulsoup4"
    ],
    python_requires = '>=3.6',
)