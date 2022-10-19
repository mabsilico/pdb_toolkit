from setuptools import setup

setup(
    name='pdb_toolkit',
    version='0.2',
    packages=['pdb_toolkit', 'pdb_toolkit.editor', 'pdb_toolkit.parser', 'pdb_toolkit.generic'],
    package_dir={'': 'src'},
    url='https://github.com/raoufkeskes/pdb_toolkit',
    license='MIT Licence',
    author='raouf-ks',
    author_email='raouf.keskes@mabsilico.com',
    description='a project to manipulate pdb files',
    python_requires='>=3.6',
    install_requires=['biopython',
                      'wget'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
)

