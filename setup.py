from setuptools import setup, find_packages


setup(
    name="kodama",
    version="0.1",
    scripts=['kodama/producer.py', 'kodama/consumer.py'],
    packages=find_packages(),
)