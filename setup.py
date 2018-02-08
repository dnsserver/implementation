from setuptools import setup, find_packages

setup(
    name='opal3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'flask',
        'flask_sqlalchemy',
        'flask_admin',
        'flask_oidc',
        'flask_bootstrap',
        'flask_nav',
        'flask-cors',
        'pyopenssl',
        'pyjwt',
        'bcrypt',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
