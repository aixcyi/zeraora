@echo off
echo https://twine.readthedocs.io/en/stable/#configuration
twine upload --non-interactive ./dist/* --repository testpypi
twine upload --non-interactive ./dist/*
