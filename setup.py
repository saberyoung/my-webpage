from setuptools import setup, find_packages
import os
import io

long_description = io.open(
    os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read()

setup(
    name="syang_web",
    version="0.1.0",
    description="s. yang's webpage",
    long_description=long_description,

    # The project URL.
    url='https://github.com/saberyoung/my-webpage/',

    # Author details
    author='Sheng Yang',
    author_email='saberyoung@gmail.com',

    # Choose your license
    license='',

    classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Intended Audience :: Developers',
         'Natural Language :: English',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    include_package_data = True, # include files listed in MANIFEST.in
    install_requires=[
        'Flask', 'MarkupSafe', 'decorator', 'itsdangerous', 'six', 'brotlipy',
        'raven[flask]', 'flask_limiter'
    ],
)
