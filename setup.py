from setuptools import setup

setup(
    name="ipxactral",
    version="0.1",
    packages=["ipxactral"],
    entry_points={"console_scripts": ["ipxactral = ipxactral.main:main",]},
    install_requires=["jinja2",],
)
