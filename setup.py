from setuptools import setup

setup(
    name='critiquel',
    packages=['critique'],
    include_package_data=True,
    install_requires=[
        'flask', 'Flask-PyMongo'
    ],
)
