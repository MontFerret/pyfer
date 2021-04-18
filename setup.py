import setuptools

import info


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name=info.name,
    version=info.version,
    author=info.author,
    author_email=info.email,
    description=info.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    data_files=[
        ('header-file', ['pferret/lib/libferret.h']),
        ('so-file', ['pferret/lib/libferret.so']),
        ('go-file', ['pferret/lib/main.go']),
        ('go-mod-file', ['pferret/lib/go.mod']),
        ('go-sum-file', ['pferret/lib/go.sum']),
    ],
    url=f'https://github.com/pyfer/{info.name}',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
