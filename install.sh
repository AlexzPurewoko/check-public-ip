#!/bin/bash

LIB_DIR=/usr/local/lib/check-ip-public
PROG=/usr/local/bin/check-public-ip

sudo mkdir -p $LIB_DIR

sudo cp requirements.txt $LIB_DIR/requirements.txt
sudo cp -r src $LIB_DIR/src
sudo -H pip3 install -r $LIB_DIR/requirements.txt

if [ -f $PROG ]; then
    sudo rm $PROG
fi
echo "#!/bin/bash" | sudo tee -a $PROG
echo "python3 $LIB_DIR/src/main.py \$@" | sudo tee -a $PROG

sudo chmod 0755 $PROG