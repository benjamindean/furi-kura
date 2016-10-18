# Furi Kura

Linux application indicator for reddit.

[![Build Status](https://travis-ci.org/benjamindean/furi-kura.svg?branch=master)](https://travis-ci.org/benjamindean/furi-kura) [![codecov](https://codecov.io/gh/benjamindean/furi-kura/branch/master/graph/badge.svg)](https://codecov.io/gh/benjamindean/furi-kura)

## Features

1. Notifications
2. Karma indicators
3. Show hot/top/new/random posts from any subreddit
4. Unity launcher integration
5. Furi
6. Kura

## Screenshot

![Furi Kura](https://cloud.githubusercontent.com/assets/5139993/16649712/e3e223f2-4442-11e6-9600-fe1d22391b91.png)

## Requirements

You can skip this list if you are installing it from a .deb package. 

1. Python 3 | `python3` (^3.4)
2. Flask | `python3-flask`
3. Requests | `python3-requests`
4. PyGObject | `python3-gi`

## Installation

### From a .deb package

```
wget https://github.com/benjamindean/furi-kura/releases/download/v0.0.9/furi-kura_0.0.9-1_all.deb
sudo dpkg -i furi-kura_0.0.9-1_all.deb
```

In case you are getting a dependency errors:

```
sudo apt-get install -f
```

### From source

```
wget https://github.com/benjamindean/furi-kura/archive/v0.0.9.zip
unzip v0.0.9.zip && cd furi-kura-0.0.9
sudo make install
```

## Contributing

Feel free to submit a pull request, report a bug, use some of my code to build your own indicator, complain about crappy implementation - whatever.

## NOTE

This project is still under development.
Karma indicators next to the icon may not work on all desktop environments and was tested on Unity only.
