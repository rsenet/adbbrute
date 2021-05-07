from setuptools import setup, find_packages


def parse_requirements(file):
    required = []
    with open(file) as f:
        for req in f.read().splitlines():
            if not req.strip().startswith('#'):
                required.append(req)
    return required


requirements = parse_requirements('requirements.txt')

long_description = "ADBBrute allows bruteforcing Android LockScreen"

setup(
    name="ADBBrute",
    version="0.1",
    description="Android LockScreen Bruteforce",
    long_description=long_description,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS'
        'Topic :: Utilities',
        'Topic :: Security',
    ],

    packages=find_packages(),
    install_requires=requirements,

    python_requires='>3.6',

    scripts=['ADBBrute.py'],
)