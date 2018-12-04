Sleuth Automation
=================

This library is an object-oriented wrapper for the
`SLEUTH urban growth model <http://www.ncgia.ucsb.edu/projects/gig/>`_.

It will automatically create scenario files from directories
containing data layers and it can run simulations through
`MPI <https://www.open-mpi.org/>`_ and
`HT-Condor <https://research.cs.wisc.edu/htcondor/>`_.

Installation
------------

You may install this library and helper scripts using pip.

.. code-block:: bash

    $ pip install sleuth_automation


Application Programming Interface
---------------------------------

.. code-block:: python

    import sleuth_automation as sa

    # the library must be configured at least with the path to SLEUTH
    sa.configure(sleuth_path='/opt/sleuth',
		 use_mpi=True, mpi_cores=32)


    # a directory containing input layers is given to a location instance
    l = sa.Location('my_location',
		    '/path/to/my_location')

    l.calibrate_coarse()
    l.calibrate_fine()
    l.calibrate_final()

    l.sleuth_predict(end=2050)


Command Line Interface
----------------------

A single run may be achieved using the included **sleuth_run.py** script.

.. code-block:: shell

   $ sleuth_run.py --sleuth_path /opt/sleuth/ \
		   --location_dir /path/to/location/ \
		   --location_name my_location \
		   --mpi_cores 40 \
		   --montecarlo_iterations 50 \
		   --predict_end 2060


This will create scenario files for coarse, fine and final stages of
calibration, extracting parameters from the control_stats.log files,
and run predict.


If one wants to predict for several locations, one may group them in a
directory and run them as a batch.  Using the
**create_sleuth_condor_batch.py** one may create a batch run for the
HT-Condor queue management system.

.. code-block:: shell

    $ create_sleuth_condor_batch.py --sleuth_path /opt/sleuth/ \
				    --region_dir /path/to/locations_group/ \
				    --mpi_cores 32 \
				    --predict_end 2060

This will create a **submit.condor** file in the locations directory,
setup with the appropiate **sleuth_run.py** commands.


Documentation
-------------
.. image:: https://readthedocs.org/projects/sleuth-automation/badge/?version=latest

Full documentation at http://sleuth-automation.readthedocs.io
