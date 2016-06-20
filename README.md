# Furi Kura

Linux appindicator for reddit.

## Features

1. Notifications
2. Karma indicators
3. Furi
4. Kura

## Screenshot

![Furi Kura](https://cloud.githubusercontent.com/assets/5139993/15985274/a269ea60-2ff0-11e6-982b-a8a3904ef27a.png)

## Requirements

You can skip this list if you are installing it from a .deb package. 

1. Python 3 | `python3`
2. Flask | `python3-flask`
3. Requests | `python3-requests`
4. PyGObject | `python3-gi`

## Installation

### From a .deb package

```
wget https://github.com/benjamindean/furi-kura/releases/download/v0.0.7-beta/furi-kura_0.0.7-1_all.deb
sudo dpkg -i furi-kura_0.0.7-1_all.deb
```

In case you are getting a dependency errors:

```
sudo apt-get install -f
```

### From source

```
wget https://github.com/benjamindean/furi-kura/archive/v0.0.7-beta.zip
unzip v0.0.7-beta.zip && cd furi-kura-0.0.7-beta
sudo make install
```

## Contributing

Feel free to submit a pull request, report a bug, use some of my code to build your own indicator, complain about crappy implementation - whatever.

## NOTE

This project is still under development.
Karma indicators next to the icon may not work on all desktop environments and was tested on Unity only.
