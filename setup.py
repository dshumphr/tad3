from setuptools import setup, find_packages

setup(
    name="tad",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["anthropic==0.34.2", "prompt_toolkit==3.0.47"],
    entry_points={"console_scripts": ["tad = tad.cli:run"]},
    description="TAD: Tool-Assisted Developer",
)