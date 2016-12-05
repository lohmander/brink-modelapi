from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="brink_modelapi",
    version="0.1.0",
    description="Automating CRUD api creation for Brink models",
    long_description=long_description,
    url="https://github.com/lohmander/brink_modelapi",
    author="CH Lohmander",
    author_email="hannes@lohmander.me",
    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: BSD License",

        "Programming Language :: Python :: 3.6",
    ],

    keywords="sample setuptools development",

    packages=find_packages(exclude=["contrib", "docs", "tests"]),

    install_requires=["PyJWT"],

    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    }
)
