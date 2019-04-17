from setuptools import setup

setup(
    name='Rotten-Eggs',
    packages=['eggs'],
    include_package_data=True,
    install_requires=[
        'flask', 'Flask-PyMongo'
    ],
)
