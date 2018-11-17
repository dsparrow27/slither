from setuptools import setup, find_packages

setup(
    name="slither",
    version="0.1.0",
    description="Execution graph",
    author="David Sparrow",
    author_email="dsparrow27@gmail.com",
    url="https://github.com/dsparrow27/slither",
    license="GNU",
    install_requires=["blinker", "ffmpeg-python"],
    dependency_links=["https://github.com/dsparrow27/zoocore"],
    packages=find_packages(),
    zip_safe=False,
)
