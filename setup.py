from setuptools import setup, find_packages


setup(
    name='pycrate_sdsm',  # Package name
    version='0.1.0',  # Version number
    packages=find_packages(),  # List of all python modules to install
    install_requires=[  # List of package dependencies
        'pycrate'
    ],
    author='Tinghan Wang',
    author_email='tinghanw@umich.edu',
    description='Sensor data sharing message (SDSM) encoder and decoder based on the latest SAE J3224',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/michigan-traffic-lab/pyV2XLib',  # Link to your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
