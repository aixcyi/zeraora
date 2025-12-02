from setuptools import find_packages, setup

with open("./zeraora/__init__.py", encoding='UTF-8') as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='Zeraora',
    version=version,
    url='https://github.com/aixcyi/zeraora',
    license='MIT',
    author='aixcyi',
    author_email='75880483+aixcyi@users.noreply.github.com',
    description="Personal infrastructure toolkit with long-term maintenance.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/aixcyi/zeraora",
        "Tracker": "https://github.com/aixcyi/zeraora/issues",
    },
    python_requires='>=3.10',
    packages=find_packages(where=".", exclude=['docs*', 'test*']),
)
