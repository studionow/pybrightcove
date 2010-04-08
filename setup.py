from setuptools import setup, find_packages

setup(
    name='pybrightcove',
    version = '1.2',
    author='Patrick Altman',
    author_email='patrick@studionow.com',
    url='git://github.com/studionow/pybrightcove.git',
    description="""A Python interface for the Brightcove APIs""",
    packages=find_packages(),
    namespace_packages = [],
    include_package_data = True,
    zip_safe=False,
    license='MIT'
)

