from setuptools import setup, find_packages

with open("./zeraora/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("version"):
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
    description="为了跨平台跨项目复用代码而开发的工具库。"
                "A utility Python package for our personal and corporate projects, with long time support.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/aixcyi/zeraora",
        "Tracker": "https://github.com/aixcyi/zeraora/issues",
    },
    python_requires='>=3.7',
    packages=find_packages(where=".", exclude=['test*', 'dataset']),
)
