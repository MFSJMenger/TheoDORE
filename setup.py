#!/usr/bin/env python
from os import path
from setuptools import setup
import sys


here = path.abspath(path.dirname(__file__))

version = '2.0.1'

requirements = ['']

scripts = [
    'bin/analyze_correlations.py',
    'bin/analyze_NOs.py',
    'bin/analyze_sden.py',
    'bin/analyze_tden.py',
    'bin/analyze_tden_soc.py',
    'bin/babel.py',
    'bin/cc2molden.py',
    'bin/cc_check.py',
    'bin/cc_opt.py',
    'bin/convert_table.py',
    'bin/dgrid_prep.py',
    'bin/draw_moments.py',
    'bin/extract_molden.py',
    'bin/fcd.py',
    'bin/jmol_MOs.py',
    'bin/jmol_vibs.py',
    'bin/parse_libwfa.py',
    'bin/plot_frag_decomp.py',
    'bin/plot_graph_nx.py',
    'bin/plot_graph.py',
    'bin/plot_Om_bars.py',
    'bin/plot_OmFrag.py',
    'bin/spectrum.py',
    'bin/tden_OV.py',
    'bin/vmd_plots.py',
]

description = ""
readme = ""

packages = ['theodore' ]#, 'orbkit/orbkit']

setup(
    name='theodore',
    version=version,
    description=description,
    long_description=readme,
    author="Felix Plasser",
    author_email='maximilian.menger@univie.ac.at',
    url='https://sourceforge.net/projects/theodore-qc/',
    packages=packages,
    scripts=scripts,
    install_requires=requirements,
    license="GNU Lesser General Public v3 or later (LGPLv3+)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
