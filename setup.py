from setuptools import setup, find_packages

setup(
    name="scryptoslib",
    version="0.0.1",
    description="A CTF Library",
    author="scryptos",
    url="https://github.com/scryptos/scryptos/",
    packages=find_packages(),
    test_suite="test.suite",
    install_requires=["gmpy2", "pycryptodome"],
)
