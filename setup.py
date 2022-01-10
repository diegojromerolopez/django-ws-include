import os
from setuptools import setup, find_packages


root_dir_path = os.path.dirname(os.path.abspath(__file__))
long_description = open(os.path.join(root_dir_path, "README.md")).read()
templates_dir_relative_path = './ws_include/templates'

data_files = []
for dirpath, dirnames, filenames in os.walk("."):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        continue
    elif filenames:
        data_files.append(
            [dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name="django-ws-include",
    version="0.1.0",
    author="Diego J. Romero López",
    author_email="diegojromerolopez@gmail.com",
    description=(
        "A simple application for Django to include "
        "(and fetch) asynchronous templates by loading templates with websocket connections."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        "channels>=3.0.4",
        "pycryptodome>=3.10.1",
        "jsonpickle>=2.0.0"
    ],
    license="MIT",
    keywords="django template asynchronous template_tag websockets",
    url="https://github.com/diegojromerolopez/django-ws-include",
    packages=find_packages(),
    data_files=[
        (
            templates_dir_relative_path, (
                os.path.join(templates_dir_relative_path, "ws_include/spinner.html"),
                os.path.join(templates_dir_relative_path, "ws_include/template_tag.html"),
                os.path.join(templates_dir_relative_path, "ws_include/template_tag.html")
            )
        )
    ],
    include_package_data=True,
)
