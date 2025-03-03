from setuptools import setup, find_packages

setup(
    name='browsergym',
    version='1.0',
    packages=['bgym', 'browsergym', 'browsergym.experiments', 'browsergym.core', 'browsergym.webmall'],
    package_dir={
        'bgym': 'browsergym/experiments/src/bgym',
        'browsergym': 'browsergym/experiments/src/browsergym',
        'browsergym.core': 'browsergym/core/src/browsergym/core',
        'browsergym.webmall': 'browsergym/webmall/src/browsergym/webmall',
    },
    install_requires=[
        # List any dependencies here
    ],
)