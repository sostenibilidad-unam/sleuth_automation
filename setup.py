from setuptools import setup

setup(name='sleuth_automation',
      version='0.2',
      description='Python wrapper for comfy running of SLEUTH',
      url='http://github.com/sostenibilidad-unam/sleuth_automation',
      author='Fidel Serrano, Rodrigo Garcia',
      author_email='rgarcia@iecologia.unam.mx',
      license='GPLv3',
      packages=['sleuth_automation'],
      scripts=['bin/sleuth_run.py',
               'bin/create_sleuth_condor_batch.py'],
      zip_safe=False)
