========================
 Batch running of SLEUTH
========================

A script is included that will create a HT-Condor_ submit file.

.. _HT-Condor: https://research.cs.wisc.edu/htcondor/ 

Usage::

    create_sleuth_condor_batch.py [-h] --sleuth_path SLEUTH_PATH
                                       --locations_dir LOCATIONS_DIR
 				       --predict_start PREDICT_START
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
  --predict_start PREDICT_START
                        starting year of prediction interval
  --predict_end PREDICT_END
                        ending year of prediction interval
  --montecarlo_iterations MONTECARLO_ITERATIONS
                        monte carlo iterations


Running this script will create a **submit.condor** file in the
supplied **locations_dir**.


This file can be submited for execution::

    $ cd LOCATIONS_DIR
    $ condor_submit submit.condor

