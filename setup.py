from distutils.core import setup

setup(
    name = 'wowza',
    packages = ['wowza'],
    version = '0.1.0',
    description = 'Python API wrapper for Wowza API',
    license = 'MIT',
    author = 'Mark Tur',
    author_email = 'mark.tur@turner.com',
    url = 'https://github.com/atlusio/wowza',
    download_url = 'https://github.com/atlusio/wowza/archive/0.1.0.tar.gz',
    keywords = 'wowza api wrapper python live streaming',
    classifiers = [],
    install_requires = ['vcrpy', 'requests', 'pytest']
)
