[![Pylint](https://github.com/Rosa-Luxemburgstiftung-Berlin/zammadls/actions/workflows/pylint.yml/badge.svg)](https://github.com/Rosa-Luxemburgstiftung-Berlin/zammadls/actions/workflows/pylint.yml)

# zammadls
zammad helper scripts

## install

### virtualenv

```
virtualenv .zammadls
source .zammadls/bin/activate
pip install -r requirements.txt
```

## config

create a configuration (see `config.yml.sample`)

the default locations the config is expected are: `config.yml` and `config/config.yml`

(the account used requires admin **and** agent rights)

## scripts

### retag

Zammad helper script to delete or change tags

#### Examples:

```
  ./retag.py -l INFO -t TESTREPLACETAG -a NEWREPLACETAG
  ./retag.py -l INFO -t TESTREPLACETAG ANOTHETRTAGTOREPLACE -a NEWREPLACETAG
```

#### Options:

```
  -h, --help            show this help message and exit
  -t, --tags TAGS [TAGS ...]
                        tag to remove
  -r, --donotdelete     do not delete tags, just remove them from tickets
  -a, --addtags ADDTAGS [ADDTAGS ...]
                        tag to add to all tickets that have the old tag
  -l, --loglevel {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        set loglevel
  -c, --config CONFIG [CONFIG ...]
                        config file
  -n, --dryrun          dry run, do not perform changes
```
