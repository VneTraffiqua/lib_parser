# Book parser from tululu.org

### Description

The script print data about the selected books.

In parameters, you need to specify from which id and to which id to parse books.

### How to install?

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```commandline
pip install -r requirements.txt
```

Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project

### Launch.

Run `parse_tululu.py` with the parameters "id_from", "id_to", to print data about the selected books.
```commandline
python3 parse_tululu.py 5 10
```

=========================================================

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).