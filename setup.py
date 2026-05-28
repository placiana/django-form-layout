from distutils.core import setup

setup(
    name='django-form-layout',
    version='0.1.dev',
    author='Joni Bekenstein, Ivan Raskovsky (rasca)',
    author_email='joni@mindpulse.net',
    packages=['form_layout',],
    license='BSD',
    description='',
    long_description=open('README.txt').read(),
    install_requires=['six'],
)
