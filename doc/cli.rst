=================================
Simplified Command Line Interface
=================================

The full pipeline can be run by supplied script. Run thusly::

   sleuth_run.py [-h] --sleuth_path SLEUTH_PATH
		      --location_dir LOCATION_DIR
		      --location_name LOCATION_NAME
		      --predict_end PREDICT_END
		      [--mpi_cores MPI_CORES]
		      [--montecarlo_iterations MONTECARLO_ITERATIONS]
		      [--virtualenv VIRTUALENV]


Arguments:


  -h, --help            show this help message and exit
  --sleuth_path SLEUTH_PATH             path to SLEUTH directory
  --location_dir LOCATION_DIR           path to location directory
  --location_name LOCATION_NAME         name of location
  --mpi_cores MPI_CORES                 number of cores available for MPI, if 0 (default) don't use MPI
  --predict_end PREDICT_END             ending year of prediction interval
  --montecarlo_iterations MONTECARLO_ITERATIONS                     monte carlo iterations
  --virtualenv VIRTUALENV               path to python virtualenv. This is mostly useful for batch runs on distributed computers. No need to specify this if you already are in a virtual environment.
