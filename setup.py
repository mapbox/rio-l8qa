from codecs import open as codecs_open
from setuptools import setup, find_packages


long_description = """CLI and python module for working with Landsat 8 QA band

https://github.com/mapbox/rio-l8qa"""


# Parse the version from the fiona module.
with open('l8qa/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break


setup(name='rio-l8qa',
      version=version,
      description=u"CLI and python module for working with Landsat 8 QA band",
      long_description=long_description,
      author=u"Matthew Perry",
      author_email='perry@mapbox.com',
      url='https://github.com/mapbox/rio-l8qa',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio>=0.36'
      ],
      extras_require={
          'test': ['coveralls', 'pytest', 'pytest-cov'],
      },
      entry_points="""
      [rasterio.rio_plugins]
      l8qa=l8qa.cli:main
      """)
