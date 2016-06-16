import glob
from distutils.core import setup


setup(
    name='furi-kura',
    version='0.0.6',
    packages=['furikura', 'furikura/desktop'],
    install_requires=[
        'Flask',
        'pygobject',
        'requests'
    ],
    scripts=['bin/furi-kura'],
    url='https://github.com/benjamindean/furi-kura',
    license='MIT',
    author='Benjamin Dean',
    description='Furi Kura for reddit',
    data_files=[
        ('/usr/share/applications/', ['furikura.desktop']),
        ('/usr/share/furikura/icons/', glob.glob("furikura/icons/*.png")),
        ('/usr/share/furikura/icons/light/', glob.glob("furikura/icons/light/*.png")),
        ('/usr/share/furikura/icons/dark/', glob.glob("furikura/icons/dark/*.png")),
        ('/usr/share/furikura/ui/', glob.glob("furikura/ui/*.xml")),
        ('/usr/share/furikura/ui/login/', glob.glob("furikura/ui/login/*.html")),
    ]
)