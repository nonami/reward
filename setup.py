# export FLASK_APP=reward_app
# export FLASK_ENV=development
# flask run


from setuptools import find_packages, setup

setup(
    name='reward_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'pymysql'
    ],
)
