from setuptools import setup

setup(
    name='pdb_toolkit',
    version='0.1',
    packages=['pdb_toolkit', 'pdb_toolkit.fixer', 'pdb_toolkit.parser', 'pdb_toolkit.generic'],
    package_dir={'': 'src'},
    url='https://github.com/raoufkeskes/pdb_toolkit',
    license='MIT Licence',
    author='raouf-ks',
    author_email='raouf.keskes@mabsilico.com',
    description='a project to manipulate pdb files',
    python_requires='>=3.6',
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
)
