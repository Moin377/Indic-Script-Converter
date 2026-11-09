import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        line.strip()
        for line in requirements_txt
        if line.strip() and not line.strip().startswith('#')
    ]

# Read meta-data
about = {}
exec(open('indo_arabic_transliteration/__version.py').read(), about)

# Install
setup(
    name="indo-arabic-transliteration",
    version=about["__version__"],
    description="Script Conversion for Indo-Pakistani languages",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GokulNC/Indic-PersoArabic-Script-Converter",
    author="Gokul NC",
    packages=["indo_arabic_transliteration"],
    # packages=find_packages(exclude=("tests",)),
    package_data={"indo_arabic_transliteration": ["data/*.csv"]},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries"
    ],
)
