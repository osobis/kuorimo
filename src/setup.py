import os
from setuptools import setup, find_packages


setup(
    name='kuorimo',
    version='0.0.1',
    packages=find_packages(),
    author='Leszek Skoczylas',
    install_requires=[],
    author_email='leszek.skoczylas@mac.com',
    description='Kuorimo Order System',
    entry_points={'console_scripts': [
        "kuorimo-orders = kuorimo.menu:menu",
    ]}
)