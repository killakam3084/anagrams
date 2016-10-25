from setuptools import setup

setup(name='anagrams',
      version='0.4',
      description='Find anagrams in tweets',
      url='http://github.com/killakam3084/anagrams',
      author='Cameron Rison',
      author_email='cameron.rison@utexas.edu',
      license='MIT',
      packages=['anagrams'],
      install_requires=['ijson'],
      scripts=['bin/find-anagrams', 'bin/make-tweet-data'],
      zip_safe=False)
