# Image-Extract

Extract image from website and store its into local

## Setup

- On project initialisation, clone the repository using

```sh
git clone https://github.com/parthjetani/Image-Extract.git
```

> _Note:_ This needs to be done only once

## Create and activate virtual environment

Create virtual environment

```sh
python -m venv venv
```

After creating a virtual environment (optional), activate it by running

For windows, activate it this way

```sh
venv/Scripts/activate
```

For other operating system like Linux and MacOS, use

```sh
source venv/bin/activate
```

## Installing project dependencies

To install the project dependencies, use

```sh
pip install -r requirements.txt
```

## Run script to get extracted data

```sh
python extract-image.py url="enter url" -p="enter folder path"
```