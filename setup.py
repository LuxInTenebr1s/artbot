#!/usr/bin/env python3
"""Setup script."""

from setuptools import setup, find_packages

DESCRIPTION = """/
A simple bot to control lights with USB DMX controller.
"""

setup(name='ArtBot',
      version='0.0.1',
      description=DESCRIPTION,
      author='Lux',
      author_email='sr.Lux1nt@gmail.com',
      url='https://github.com/LuxInTenebr1s/art_bot',
      packages=find_packages(),
      datapackage_data={
          '': ['*.ini'],
      },
      include_package_data=True,
      entry_points={
          'console_scripts': ['artbot = artbot.artbot:main',
                              'artbot_test = artbot.artbot:test']
      },
)
