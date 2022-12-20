import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytelemetry",
    version="0.1.0",
    author="Diego Saouda",
    author_email="dsaouda@gmail.com",
    description="A simple and default open telemetry log formatter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsaouda/pytelemetry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)