#!/usr/bin/python3

from setuptools import setup

home_page = 'https://github.com/jk-aneirin/alidns'

requires = [
    'aliyun-python-sdk-core-v3>=2.5.2',
    'aliyun-python-sdk-alidns>=2.0.7'
    'docopt>=0.6.2'
]

packages = [
    'alidns'
]

setup(
    name='alidns',
    version='2.0.2',
    keywords=(
        'alidns',
        'aliyun',
        'ddns',
        'dns'
    ),
    author='aneirin',
    author_email='aeiouxu@163.com',
    url=home_page,
    license='GPLv3',
    description='Aliyun DNS Update Tool.',
    long_description='Detail: %s' % home_page,
    include_package_data=True,
    zip_safe=False,
    packages=packages,
    platforms='linux',
    python_requires=">=3.0",
    install_requires=requires,
    entry_points={
        'console_scripts':[
            'alidns = alidns.alidns:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
