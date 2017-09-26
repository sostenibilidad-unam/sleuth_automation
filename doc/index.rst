SLEUTH Automation
=================

This project aims to ease the running of the SLEUTH_ urban growth
model mostly by automating the creation of `scenario files`_ and by a
convenient object oriented interface that will do the necessary system
calls, including the use of MPI_ for multi-core parallel execution and
HT-Condor_ for distributed multi-host execution.

This software has been tested with Open MPI 1.6.5 and HT-Condor 8.4.6.

It is distributed through pypi_, a public repo is available at
GitHub_.

.. _SLEUTH: http://www.ncgia.ucsb.edu/projects/gig/
.. _pypi: https://pypi.python.org/pypi/sleuth-automation/
.. _GitHub: https://github.com/sostenibilidad-unam/sleuth_automation
.. _MPI: http://www.open-mpi.org/
.. _HT-Condor: https://research.cs.wisc.edu/htcondor/
.. _`scenario files`: http://www.ncgia.ucsb.edu/projects/gig/About/data_files/scenario_file.htm
.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   cli
   batch
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
