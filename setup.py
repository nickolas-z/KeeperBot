from setuptools import setup, find_packages

setup(
    name="KeeperBot",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[

        'colorama==0.4.6',
        'prompt_toolkit==3.0.47',
        'pyreadline3==3.4.1',
        'tabulate==0.9.0',
        'wcwidth==0.2.13',
    ],
    entry_points={
        'console_scripts': [
            'keeperbot = keeperbot.main:main',
        ],
    },
    author="KeeperTeam",
    author_email="nickolasz@gmail.com",
    description="Intelligent CLI contact manager",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/KeeperBot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)