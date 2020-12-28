from setuptools import setup
import os.path

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.md')) as rdr:
    long_description = rdr.read()

setup(name='libevent',
      version='0.4.0',
      description='Library for sending events',
      long_description=long_description,
      url='http://github.com/adamvinueza/libevent',
      author='Adam Vinueza',
      author_email='adamvinueza@pm.me',
      license='MIT',
      packages=['libevent'],
      package_data={
          'libevent': ['py.typed']
      },
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9'
      ],
      zip_safe=False)
