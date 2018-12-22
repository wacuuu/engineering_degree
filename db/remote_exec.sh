#!/bin/bash
VIRUTALENV=/root/venv/bin/activate
THREADS=$(nproc)
FILENAME="$THREADS-$(hostname)-$(date +%s)"
# source env
git clone git@gitlab.com:jwalecki-inz/db.git
cp config.yml.example config.yml
/bin/sed -i "s%THREADS%$THREADS%" $PWD/config.yml
/bin/sed -i "s%ADDRESS%$1%" $PWD/config.yml
# run tests
source $VIRUTALENV 2>&1 >> /dev/null
python terrorist.py --output $FILENAME.csv 

# tar
tar cf $FILENAME.tar $FILENAME.csv 2>&1 >> /dev/null
tar cf served.tar served.csv 2>&1 >> /dev/null
gzip $FILENAME.tar 2>&1 >> /dev/null
gzip served.tar 2>&1 >> /dev/null
if [ ! -d /tmp/out ]; then
    mkdir -p /tmp/out
fi
cp $FILENAME.tar.gz /tmp/out
cp served.tar.gz /tmp/out
echo "$FILENAME.tar.gz"
cd ..