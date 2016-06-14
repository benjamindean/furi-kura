from distutils.core import setup

setup(
    name='furi-kura',
    version='0.0.6',
    packages=['furikura'],
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
        ('/usr/share/furikura/icons/', ['furikura/icons/furi-active.png']),
        ('/usr/share/furikura/icons/', ['furikura/icons/furi-kura.png']),
        ('/usr/share/furikura/icons/', ['furikura/icons/furi-attention.png']),
        ('/usr/share/furikura/icons/', ['furikura/icons/furi-kura-logo.png']),
        ('/usr/share/furikura/ui/', ['furikura/ui/menu.xml']),
        ('/usr/share/furikura/ui/', ['furikura/ui/about.xml']),
        ('/usr/share/furikura/ui/login/', ['furikura/ui/login/login.html']),
        ('/usr/share/furikura/ui/login/', ['furikura/ui/login/success.html'])
    ]
)
