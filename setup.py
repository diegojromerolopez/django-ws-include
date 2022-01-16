import os
from setuptools import setup, find_packages


root_dir_path = os.path.dirname(os.path.abspath(__file__))
long_description = open(os.path.join(root_dir_path, "README.md")).read()

setup(
    name="django-ws-include",
    version="0.3.0",
    author="Diego J. Romero López",
    author_email="diegojromerolopez@gmail.com",
    description=(
        "A simple application for Django to include " +
        "(and fetch) asynchronous templates by loading " +
        "templates with websocket connections."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=[
        "Django>=4.0.1",
        "channels>=3.0.4",
        "pycryptodome>=3.10.1",
        "jsonpickle>=2.0.0"
    ],
    license="MIT",
    keywords="django template asynchronous template_tag websockets",
    url="https://github.com/diegojromerolopez/django-ws-include",
    packages=find_packages(),
    include_package_data=True,
)
