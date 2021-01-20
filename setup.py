from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='sleuth_automation',
      version='3.0.3',
      description='Python wrapper for SLEUTH urban growth model.',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.7',
          'Operating System :: Unix',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering'],
      url='http://github.com/sostenibilidad-unam/sleuth_automation',
      author='Fidel Serrano, Rodrigo Garcia',
      author_email='rgarcia@iecologia.unam.mx',
      license='GPLv3',
      packages=['sleuth_automation'],
      package_data={'templates': ['sleuth_automation/templates/condor_submit.jinja',
                                  'sleuth_automation/templates/scenario.jinja']},

      include_package_data=True,
      install_requires=['pandas', 'jinja2', 'sh'],
      python_requires='>=3.7',
      scripts=['bin/sleuth_run.py',
               'bin/create_sleuth_condor_batch.py'],
      zip_safe=False)
