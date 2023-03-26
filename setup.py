from setuptools import setup

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
    description="一个包含原创工具类及快捷函数的工具库。"
                "A original utility Python package.",
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
    packages=['zeraora'],
)
