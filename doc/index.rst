=============================
Atomic Simulation Environment
=============================

The Atomic Simulation Environment (ASE) is a set of tools and Python_
modules for setting up, manipulating, running, visualizing and analyzing
atomistic simulations.  The code is freely available under the :ref:`GNU LGPL
license <license info>`.

.. _Python: https://www.python.org/

ASE provides interfaces to different codes through :mod:`Calculators
<ase.calculators>` which are used together with the central
:mod:`Atoms <ase.atoms>` object and the many available algorithms in
ASE.


>>> # Example: structure optimization of hydrogen molecule
>>> from ase import Atoms
>>> from ase.optimize import BFGS
>>> from ase.calculators.nwchem import NWChem
>>> from ase.io import write
>>> h2 = Atoms('H2',
...            positions=[[0, 0, 0],
...                       [0, 0, 0.7]])
>>> h2.calc = NWChem(xc='PBE')
>>> opt = BFGS(h2)
>>> opt.run(fmax=0.02)
BFGS:   0  19:10:49    -31.435229     2.2691
BFGS:   1  19:10:50    -31.490773     0.3740
BFGS:   2  19:10:50    -31.492791     0.0630
BFGS:   3  19:10:51    -31.492848     0.0023
>>> write('H2.xyz', h2)
>>> h2.get_potential_energy()
-31.492847800329216

Supported :mod:`Calculators <ase.calculators>`
==============================================

.. list-table::
   :header-rows: 0
   :widths: 33 33 33
   :class: calculator-table

   * - |ABACUS|

       `ABACUS <https://gitlab.com/1041176461/ase-abacus>`__

       Plane-wave and numerical atomic orbital DFT.

     - |abinit|

       `ABINIT <ase/calculators/abinit.html>`__

       Plane-wave DFT and many-body perturbation theory.

     - |Asap|

       `Asap <https://wiki.fysik.dtu.dk/asap>`__

       Fast classical potentials (EMT, EAM, ...).

   * - |Atomistica|

       `Atomistica <https://github.com/Atomistica/atomistica>`__

       Bond-order and reactive potentials.

     - |BigDFT|

       `BigDFT <https://bigdft.org/>`__

       Wavelet-based DFT.

     - |CASTEP|

       `CASTEP <ase/calculators/castep.html>`__

       Plane-wave pseudopotential DFT.

   * - |CP2K|

       `CP2K <ase/calculators/cp2k.html>`__

       Mixed Gaussian and plane-wave DFT and molecular dynamics.

     - |CRYSTAL|

       `CRYSTAL <ase/calculators/crystal.html>`__

       Periodic ab initio code with Gaussian basis sets.

     - |DeePMD-kit|

       `DeePMD-kit <https://github.com/deepmodeling/deepmd-kit>`__

       Machine-learned deep potential models.

   * - |deMon|

       `deMon <ase/calculators/demon.html>`__

       Gaussian-type orbital DFT (deMon2k).

     - |dftb|

       `DFTB+ <ase/calculators/dftb.html>`__

       Density functional tight binding.

     - |dftd4|

       `DFT-D4 <https://github.com/dftd4/dftd4/tree/master/python>`__

       Dispersion corrections for DFT.

   * - |DFTK|

       `DFTK <https://dftk.org/q/ase>`__

       Plane-wave DFT in Julia.

     - |elk|

       `Elk <http://elk.sourceforge.net/>`__

       All-electron full-potential LAPW DFT.

     - |exciting|

       `exciting <ase/calculators/exciting.html>`__

       All-electron full-potential LAPW DFT.

   * - |EMT|

       `EMT <ase/calculators/emt.html>`__

       Effective medium theory potential for metals.

     - |fhi-aims|

       `FHI-aims <ase/calculators/FHI-aims.html>`__

       All-electron DFT with numeric atom-centered orbitals.

     - |fleur|

       `FLEUR <ase/calculators/fleur.html>`__

       All-electron full-potential LAPW DFT.

   * - |gamess_us|

       `GAMESS-US <ase/calculators/gamess_us.html>`__

       Quantum chemistry package.

     - |gpaw|

       `GPAW <https://gpaw.readthedocs.io/>`__

       PAW DFT with real-space grid, plane-wave and LCAO modes.

     - |gromacs|

       `GROMACS <ase/calculators/gromacs.html>`__

       Classical molecular dynamics for biomolecular systems.

   * - |hotbit|

       `Hotbit <https://github.com/pekkosk/hotbit>`__

       Density functional tight binding.

     - |jdftx|

       `JDFTx <http://jdftx.org/ASE.html>`__

       Plane-wave DFT with joint density-functional solvation.

     - |kim|

       `KIM <ase/calculators/kim.html>`__

       Interatomic models from the OpenKIM repository.

   * - |lammps|

       `LAMMPS <ase/calculators/lammps.html>`__

       Classical molecular dynamics.

     - |mopac|

       `MOPAC <ase/calculators/mopac.html>`__

       Semi-empirical quantum chemistry.

     - |nwchem|

       `NWChem <ase/calculators/nwchem.html>`__

       Quantum chemistry and DFT package.

   * - |octopus|

       `Octopus <ase/calculators/octopus.html>`__

       Real-space and real-time TDDFT.

     - |onetep|

       `ONETEP <ase/calculators/onetep.html>`__

       Linear-scaling DFT.

     - |openmx|

       `OpenMX <ase/calculators/openmx.html>`__

       DFT with numerical pseudo-atomic orbitals.

   * - |plumed|

       `PLUMED <ase/calculators/plumed.html>`__

       Enhanced sampling and free-energy methods.

     - |psi4|

       `Psi4 <ase/calculators/psi4.html>`__

       Quantum chemistry package.

     - |qchem|

       `Q-Chem <ase/calculators/qchem.html>`__

       Quantum chemistry package.

   * - |q_espresso|

       `Quantum ESPRESSO <ase/calculators/espresso.html>`__

       Plane-wave pseudopotential DFT.

     - |siesta|

       `SIESTA <ase/calculators/siesta.html>`__

       DFT with numerical atomic orbitals.

     - |turbomole|

       `TURBOMOLE <ase/calculators/turbomole.html>`__

       Quantum chemistry package.

   * - |vasp|

       `VASP <ase/calculators/vasp.html>`__

       Plane-wave PAW DFT.

     - |xtb|

       `xtb <https://github.com/grimme-lab/xtb/tree/master/python>`__

       Semi-empirical GFN tight-binding methods.

     - |orca|

       `ORCA <ase/calculators/orca.html>`__

       Quantum chemistry package.

Contents
========

.. toctree::

    about
    install
    examples_generated/index
    howtos_generated/index
    gettingstarted/gettingstarted
    cmdline
    ase/gui/gui
    ase/ase
    tips
    releasenotes
    contact
    development/development
    faq

.. Keep all the ".. |name| image:: ..." substitution definitions and the
   ".. _Sphinx:" / ".. _Asap:" / ".. _CAMd:" targets from your original
   file below this point.

:mod:`ACE-Molecule <ase.calculators.acemolecule>`
:mod:`~ase.calculators.amber`
:mod:`DMol³ <ase.calculators.dmol>`
:mod:`Gaussian <ase.calculators.gaussian>`
:mod:`Grimme DFT-D3 <ase.calculators.dftd3>`
:mod:`~ase.calculators.gulp`
:mod:`~ase.calculators.qmmm`
:mod:`~ase.calculators.tip3p`
:mod:`deMon-Nano <ase.calculators.demonnano>`
`Skala <https://microsoft.github.io/skala/ase.html>`_


`Reference publication on ASE <https://iopscience.iop.org/article/10.1088/1361-648X/aa680e/meta>`__


.. _news:

News
====

* The website https://ase-lib.org/ now represents the broader ASE community,
  whereas the ASE documentation has been moved to https://docs.ase-lib.org. (23 Jun 2026)

* :ref:`ASE version 3.29.0 <releasenotes>` released (21 June 2026).

* Workshop on
  `ASE integration in the wider community
  <https://www.cecam.org/workshop-details/the-atomic-simulation-environment-integration-into-wider-community-projects-1509>`__
  held at CECAM, Mainz, Germany June 5-19 (21 Jun 2026).

* :ref:`ASE version 3.28.0 <releasenotes>` released (17 March 2026).

* :ref:`ASE version 3.27.0 <releasenotes>` released (28 December 2025).

* :ref:`ASE version 3.26.0 <releasenotes>` released (12 August 2025).

* ASE web page moved to `ase-lib.org <https://ase-lib.org/>`_ (8 August 2025).

* Workshop focusing on the `extended ASE ecosystem
  <https://www.cecam.org/workshop-details/the-atomic-simulation-environment-ecosystem-present-and-perspectives-1373>`_
  held at CECAM, EPFL, Switzerland June 23-27, 2025 (29 June 2025).

* :ref:`ASE version 3.25.0 <releasenotes>` released (11 April 2025).

* :ref:`ASE version 3.24.0 <releasenotes>` released (28 December 2024).

* :ref:`ASE version 3.23.0 <releasenotes>` released (31 May 2024).

* Workshop focusing on `Open Science with the Atomic Simulation Environment <https://www.cecam.org/workshop-details/open-science-with-the-atomic-simulation-environment-1245>`_ held at Daresbury Laboratory, UK April 24-28, 2023. (`Workshop site including tutorials <https://ase-workshop-2023.github.io/home/index.html>`_)

* :ref:`ASE version 3.22.1 <releasenotes>` released (1 December 2021).

* :ref:`ASE version 3.22.0 <releasenotes>` released (24 June 2021).

* :ref:`ASE version 3.21.1 <releasenotes>` released (24 January 2021).

* :ref:`ASE version 3.21.0 <releasenotes>` released (18 January 2021).

* New bugfix releases :ref:`3.20.1 <releasenotes>` and :ref:`3.19.3
  <releasenotes>` (11 August 2020).

* :ref:`ASE version 3.20.0 <releasenotes>` released (8 August 2020).

* :ref:`ASE version 3.19.2 <releasenotes>` released (22 July 2020).

* :ref:`ASE version 3.19.1 <releasenotes>` released (4 April 2020).

* :ref:`ASE version 3.19.0 <releasenotes>` released (16 December 2019).

* :ref:`ASE version 3.18.2 <releasenotes>` released (15 December 2019).

* First `ASE Workshop <https://ase-workshop.materialsmodeling.org/>`_
  held at Chalmers University of Technology, Gothenburg, Sweden,
  November 19-22, 2019 (15 December 2019).

* :ref:`ASE version 3.18.1 <releasenotes>` released (20 September 2019).

* :ref:`ASE version 3.18.0 <releasenotes>` released (19 July 2019).

* :ref:`ASE version 3.17.0 <releasenotes>` released (12 November 2018).

* :ref:`ASE version 3.16.2 <releasenotes>` released (5 June 2018).

* :ref:`ASE version 3.16.0 <releasenotes>` released (21 March 2018).

* :ref:`ASE version 3.15.0 <releasenotes>` released (28 September 2017).

* Bugfix release: :ref:`ASE version 3.14.1 <releasenotes>` (28 June 2017).

* :ref:`ASE version 3.14.0 <releasenotes>` released (20 June 2017).

* :ref:`Reference paper <cite>` in
  J. Phys. Condens. Matter:
  :doi:`The Atomic Simulation Environment | A Python library for working with
  atoms <10.1088/1361-648X/aa680e>`
  (7 June 2017).

* :ref:`ASE version 3.13.0 <releasenotes>` released (7 February 2017).

* Psi-k *Scientific Highlight Of The Month*:
  `The Atomic Simulation Environment | A Python library for working with
  atoms <http://psi-k.net/download/highlights/Highlight_134.pdf>`__
  (20 January 2017).

* :ref:`ASE version 3.12.0 <releasenotes>` released (24 October 2016).

* :ref:`ASE version 3.11.0 <releasenotes>` released (10 May 2016).

* :ref:`ASE version 3.10.0 <releasenotes>` released (17 March 2016).

* Web-page now uses the `Read the Docs Sphinx Theme
  <https://github.com/readthedocs/sphinx_rtd_theme>`_ (20 February 2016).

* The source code is now on https://gitlab.com/ase/ase (18 September 2015).

* :ref:`ASE version 3.9.1 <releasenotes>` released (21 Juli 2015).

* :ref:`ASE version 3.9.0 <releasenotes>` released (28 May 2015).

* :ref:`ASE version 3.8.0 <releasenotes>` released (22 October 2013).

* :ref:`ASE version 3.7.0 <releasenotes>` released (13 May 2013).

* :ref:`ASE version 3.6.0 <releasenotes>` released (24 February 2012).

* Bugfix release: :ref:`ASE version 3.5.1 <releasenotes>` (24 May 2011).

* :ref:`ASE version 3.5.0 <releasenotes>` released (13 April 2011).

* :ref:`ASE version 3.4.1 <download_and_install>` released (11 August 2010).

* :ref:`ASE version 3.4 <download_and_install>` released (23 April 2010).

* :ref:`ASE version 3.3 <download_and_install>` released (11 January 2010).

* :ref:`ASE version 3.2 <download_and_install>` released (4 September 2009).

* ASE has reached revision 1000 (16 July 2009).

* :ref:`ASE version 3.1.0 <download_and_install>` released (27 March 2009).

* Improved :mod:`ase.vibrations` module: More accurate and
  possibility to calculate :ref:`infrared` (13
  March 2009).

* :ref:`ASE version 3.0.0 <download_and_install>` released (13 November 2008).

* Asap_ version 3.0.2 released (15 October 2008).

* An experimental abinit interface released (9 June 2008).

* Thursday April 24 will be ASE documentation-day.  Ten people from
  CAMd/Cinf will do a "doc-sprint" from 9 to 16.  (17 Apr 2008)

* The new ASE-3.0 Sphinx_ page is now up and running!  (2 Apr 2008)

* A beta version of the new ASE-3.0 will be used for the
  electronic structure course at CAMd_.  (10 Jan 2008)


Contents
========

.. toctree::

    about
    install
    examples_generated/index
    howtos_generated/index
    gettingstarted/gettingstarted
    cmdline
    ase/gui/gui
    ase/ase
    tips
    releasenotes
    contact
    development/development
    faq

.. |ABACUS| image:: static/abacus.png
   :target: https://gitlab.com/1041176461/ase-abacus
   :align: middle
   :height: 75 px
.. |abinit| image:: static/abinit.png
   :target: ase/calculators/abinit.html
   :align: middle
.. |Asap| image:: static/asap.png
   :target: https://wiki.fysik.dtu.dk/asap
   :align: middle
   :height: 75 px
.. |Atomistica| image:: static/atomistica.png
   :target: https://github.com/Atomistica/atomistica
   :align: middle
.. |BigDFT| image:: static/bigdft.png
   :target: https://bigdft.org/
   :align: middle
.. |CASTEP| image:: static/castep.png
   :target: ase/calculators/castep.html
   :align: middle
.. |CP2K| image:: static/cp2k.png
   :target: ase/calculators/cp2k.html
   :align: middle
.. |CRYSTAL| image:: static/crystal.png
   :target: ase/calculators/crystal.html
   :align: middle
.. |DeePMD-kit| image:: static/deepmd-kit.png
   :target: https://github.com/deepmodeling/deepmd-kit
   :align: middle
   :height: 75px
.. |deMon| image:: static/demon.png
   :target: ase/calculators/demon.html
   :align: middle
.. |dftd4| image:: static/dftd4.png
   :target: https://github.com/dftd4/dftd4/tree/master/python
   :align: middle
.. |elk| image:: static/elk.png
   :target: http://elk.sourceforge.net/
   :align: middle
.. |EMT| image:: static/emt.png
   :target: ase/calculators/emt.html
   :align: middle
.. |exciting| image:: static/exciting.png
   :target: ase/calculators/exciting.html
   :align: middle
.. |dftb| image:: static/dftb.png
   :target: ase/calculators/dftb.html
   :align: middle
.. |DFTK| image:: static/dftk.png
   :target: https://dftk.org/q/ase
   :align: middle
.. |fhi-aims| image:: static/fhi-aims.png
   :target: ase/calculators/FHI-aims.html
   :align: middle
.. |fleur| image:: static/fleur.png
   :target: ase/calculators/fleur.html
   :align: middle
.. |gamess_us| image:: static/gamess_us.png
   :target: ase/calculators/gamess_us.html
   :align: middle
.. |gpaw| image:: static/gpaw.png
   :target: https://gpaw.readthedocs.io/
   :align: middle
.. |gromacs| image:: static/gromacs.png
   :target: ase/calculators/gromacs.html
   :align: middle
.. |hotbit| image:: static/hotbit.png
   :target: https://github.com/pekkosk/hotbit
   :align: middle
.. |jdftx| image:: static/jdftx.png
   :target: http://jdftx.org/ASE.html
   :align: middle
.. |kim| image:: static/kim.png
   :target: ase/calculators/kim.html
   :align: middle
.. |lammps| image:: static/lammps.png
   :target: ase/calculators/lammps.html
   :align: middle
   :height: 75 px
.. |mopac| image:: https://openmopac.net/images/logo.png
   :target: ase/calculators/mopac.html
   :align: middle
   :height: 75 px
.. |nwchem| image:: static/nwchem.png
   :target: ase/calculators/nwchem.html
   :align: middle
.. |octopus| image:: static/octopus.png
   :target: ase/calculators/octopus.html
   :align: middle
.. |onetep| image:: static/onetep.png
   :target: ase/calculators/onetep.html
   :align: middle
.. |openmx| image:: static/openmx.png
   :target: ase/calculators/openmx.html
   :align: middle
.. |plumed| image:: static/plumed.png
   :target: ase/calculators/plumed.html
   :align: middle
.. |psi4| image:: static/psi4.png
   :target: ase/calculators/psi4.html
   :align: middle
.. |qchem| image:: static/qchem.png
   :target: ase/calculators/qchem.html
   :align: middle
   :scale: 40
.. |q_espresso| image:: static/espresso.png
   :target: ase/calculators/espresso.html
   :align: middle
   :scale: 50
.. |siesta| image:: static/siesta.png
   :target: ase/calculators/siesta.html
   :align: middle
.. |turbomole| image:: static/tm_logo_l.png
   :target: ase/calculators/turbomole.html
   :align: middle
.. |vasp| image:: static/vasp.png
   :target: ase/calculators/vasp.html
   :align: middle
.. |xtb| image:: static/xtb.png
   :target: https://github.com/grimme-lab/xtb/tree/master/python
   :align: middle
.. |orca| image:: static/orca_logo_mpi.png
   :target: ase/calculators/orca.html
   :align: middle

.. _Sphinx: https://www.sphinx-doc.org/
.. _Asap: https://wiki.fysik.dtu.dk/asap
.. _CAMd: https://www.fysik.dtu.dk/english/research/camd/
