from setuptools import setup, find_namespace_packages

setup(
    name='cloud-storage',
    version="1.2.0",
    packages=find_namespace_packages(include=['papermerge.*']),
    license='Proprietary',
    url='https://papermerge.com/',
    author='Eugen Ciur',
    author_email='eugen@papermerge.com',
    python_requires='>=3.7',
)
