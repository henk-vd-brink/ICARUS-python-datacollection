from setuptools import setup, find_packages

setup(
    name="ICARUS Data Collection Server",
    version="0.1.0",
    packages=find_packages(
        include=[
            "icarus-webserver"
        ]
    )
)