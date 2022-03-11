from setuptools import setup, find_packages
import sys, os
from vs2020._version import __version__ as VERSION

setup(name='vs2020',
      version=VERSION,
      description="CUI for VS2020",
      long_description="""\
This is a command-line user interface for VisualStage2020.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='command-line',
      author='Yusuke Yachi',
      author_email='yyachi@misasa.okayama-u.ac.jp',
      url='http://dream.misasa.okayama-u.ac.jp',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'pypiwin32',
            'psutil',
            'requests',
            "PyYAML",
#            "pillow",
            "paho-mqtt",
          # -*- Extra requirements: -*-
      ],
      entry_points={
            "console_scripts": [
                  "vs2020-sentinel = vs2020.mqtt_client:main",
            ]},
      test_suite='nose.collector',
      )
