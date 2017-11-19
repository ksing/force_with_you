from setuptools import setup

setup(
    name='force_with_you',
    packages=['force_with_you_app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)