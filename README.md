# ghwho

GitHub-based user information lookup.

## Prerequisites

```
pip install pycurl
pip install json
```

## Installation

```
curl -L http://github.com/henokmikre/ghwho/raw/master/ghwho.py > ghwho
```

Make it executable:

```
chmod +x ghwho
```

Move it to a bin:

```
mv ghwho /usr/local/share/ghwho
```

## Usage

Print user's first name:

```
ghwho -u henokmikre -p first
```

Replace the string `{fullname}` with the user's full name:

```
sed "s/{fullname}/$(ghwho -p fullname)/g" test.txt
```

