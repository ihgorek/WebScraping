from distutils.core import setup
import py2exe

# Change the path in the following line for webdriver.xpi
data_files = [('selenium\\webdriver\\Firefox',
               ['C:\\Igor\\Programm\\Python27\\Lib\\site-packages\\selenium\\webdriver\\firefox\\webdriver.xpi'])]

setup(
    name='ParserPin',
    version='1.0',
    description='pinterest parser',
    author='IgorU',
    author_email='author email',
    url='',
    console=[{'script': 'pinter_parser.py'}],   # the main py file
    data_files=data_files,
    options={
        'py2exe':
            {
                'skip_archive': True,
                'optimize': 2,
            }
    }
)