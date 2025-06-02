"""Setup script for Project Simone"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-simone",
    version="0.1.0",
    author="Project Simone Team",
    description="Intelligent Philosophical Content Analysis System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/project-simone",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.29.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "openai>=1.6.0",
        "tiktoken>=0.5.0",
        "scikit-learn>=1.3.0",
        "networkx>=3.2",
        "plotly>=5.18.0",
        "click>=8.1.0",
        "tqdm>=4.66.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "simone=project_simone.__main__:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "project_simone": ["config/*.yaml"],
    },
)