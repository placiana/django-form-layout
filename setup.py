from setuptools import setup, find_packages

setup(
    name='django-form-layout',
    version='0.1.dev',
    author='Joni Bekenstein, Ivan Raskovsky (rasca)',
    # find_packages() encontrará form_layout y form_layout.templatetags
    packages=find_packages(), 
    include_package_data=True, # Importante para incluir templates HTML si los hay
    license='BSD',
    description='',
    long_description=open('README.txt').read(),
    install_requires=['six'],
)
