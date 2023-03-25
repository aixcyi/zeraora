from setuptools import setup

import zeraora

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='Zeraora',
    version=zeraora.version,
    packages=['zeraora'],
    python_requires='>=3.7',
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
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/aixcyi/zeraora",
        "Tracker": "https://github.com/aixcyi/zeraora/issues",
    }
)
