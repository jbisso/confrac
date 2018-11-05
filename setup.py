from distutils.core import setup

setup(name = 'ContinuedFractions',
      version = '0.0.1',
      description = 'Continued fractions',
      author = 'Jim Bisso',
      author_email = 'jbisso@gmail.com',
      url = 'http://bisso.biz/',
      packages = ['confrac'],
      package_dir = {'confrac' : 'src/confrac'},
     )