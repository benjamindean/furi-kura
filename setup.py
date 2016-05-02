from distutils.core import setup

setup(
    name='furi-kura',
    version='0.0.1',
    packages=['furikura'],
    data_files=[
        ("furikura/icons/", ['furikura/icons/furi-active.png']),
        ("furikura/icons/", ['furikura/icons/furi-attention.png']),
        ("furikura/ui/", ['furikura/ui/menu.xml'])
    ],
    install_requires=[
        'Flask',
        'pygobject',
        'requests'
    ],
    scripts=["bin/furikura"],
    url='https://github.com/benjamindean/furi-kura',
    license='MIT',
    author='benjamindean',
    description='Linux appindicator for reddit'
)
