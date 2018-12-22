#!/bin/bash
VIRUTALENV=/root/venv/bin/activate
THREADS=$(( $(nproc) * 3 ))
FILENAME="$THREADS-$(hostname)-$(date +%s)"
# source env
git clone git@gitlab.com:jwalecki-inz/db.git
cd db
cp config.yml.example config.yml
/bin/sed -i "s%THREADS%$THREADS%" $PWD/config.yml
/bin/sed -i "s%ADDRESS%$1%" $PWD/config.yml
# run tests
source $VIRUTALENV 2>&1 >> /dev/null && python terrorist.py --output $FILENAME.csv 2>&1 >> /dev/null
# tar
tar cf $FILENAME.tar $FILENAME.csv 2>&1 >> /dev/null
gzip $FILENAME.tar 2>&1 >> /dev/null
if [ ! -d /tmp/out/ ]; then
    mkdir -p /tmp/out/
fi
mv $FILENAME.tar.gz /tmp/out/
echo "$FILENAME.tar.gz"
cd ..
rm -fr db