========================
 Batch running of SLEUTH
========================

A script is included that will create a HT-Condor_ submit file.

.. _HT-Condor: https://research.cs.wisc.edu/htcondor/

Usage::

    create_sleuth_condor_batch.py [-h] --sleuth_path SLEUTH_PATH
				       --locations_dir LOCATIONS_DIR
				       --predict_end PREDICT_END
				       [--mpi_cores MPI_CORES]
				       [--montecarlo_iterations MONTECARLO_ITERATIONS]


Arguments:

  -h, --help            show this help message and exit
  --sleuth_path SLEUTH_PATH
			path to SLEUTH directory
  --locations_dir LOCATIONS_DIR
			path to regions dir
  --mpi_cores MPI_CORES
			number of cores available for MPI, if 0 (default) don't use mpi
  --predict_end PREDICT_END
			ending year of prediction interval
  --montecarlo_iterations MONTECARLO_ITERATIONS
			monte carlo iterations


Running this script will create a submit.condor_ file in the
supplied **LOCATIONS_DIR**, with proper invocations of the sleuth_run.py script.

.. _submit.condor: http://research.cs.wisc.edu/htcondor/manual/v8.4/2_5Submitting_Job.html

This file can then be submited for execution::

    $ cd LOCATIONS_DIR
    $ condor_submit submit.condor
