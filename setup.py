from setuptools import setup, find_packages

setup(
    name='mixpanel_export',
    version='0.0.2',
    author='Devin Fee',
    author_email='devin.fee@gmail.com',
    packages=find_packages(),
    url='https://github.com/dfee/mixpanel_export',
    description="""Python API client library to consume mixpanel.com analytics
                data.""",
    long_description=open('README.rst').read(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
