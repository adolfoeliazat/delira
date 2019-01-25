import os
import re
from setuptools import find_packages, setup
from setuptools.command.sdist import sdist
from setuptools.command.bdist_egg import bdist_egg


def resolve_requirements(file):
    requirements = []
    with open(file) as f:
        req = f.read().splitlines()
        for r in req:
            if r.startswith("-r"):
                requirements += resolve_requirements(
                    os.path.join(os.path.dirname(file), r.split(" ")[1]))
            else:
                requirements.append(r)
    return requirements


def read_file(file):
    with open(file) as f:
        content = f.read()
    return content


def find_version(file):
    content = read_file(file)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content,
                              re.M)
    if version_match:
        return version_match.group(1)


requirements = resolve_requirements(os.path.join(os.path.dirname(__file__),
                                                 'requirements.txt'))

requirements_extra_full = []

requirements_extra_torch = resolve_requirements(os.path.join(
    os.path.dirname(__file__), 'requirements_extra_torch.txt'))
requirements_extra_full += requirements_extra_torch

readme = read_file(os.path.join(os.path.dirname(__file__), "README.md"))
license = read_file(os.path.join(os.path.dirname(__file__), "LICENSE"))
delira_version = find_version(os.path.join(os.path.dirname(__file__), "delira",
                                           "__init__.py"))


class sdist_date(sdist):

    def run(self):
        suffix = self.get_datetime_suffix()
        self.distribution.metadata.version += "_%s" % suffix
        sdist.run(self)

    def get_datetime_suffix(self):
        import datetime
        return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

class bdist_egg_date(bdist_egg):
    def run(self):
        suffix = self.get_datetime_suffix()
        self.distribution.metadata.version += "_%s" % suffix
        sdist.run(self)

    def get_datetime_suffix(self):
        import datetime
        return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')


setup(
    name='delira',
    version=delira_version,
    packages=find_packages(),
    url='https://git.lfb.rwth-aachen.de/Radiology/Delira/',
    test_suite="pytest",
    long_description=readme,
    license=license,
    install_requires=requirements,
    tests_require=["pytest-cov"],
    python_requires=">3.5",
    extras_require={
        "full": requirements_extra_full,
        "torch": requirements_extra_torch
    },
    cmdclass={"bdist_egg": bdist_egg_date, "sdist": sdist_date}
)
