#!/bin/bash

LIB_DIR=/usr/local/lib/check-ip-public
PROG=/usr/local/bin/check-public-ip
PROG_UPDATE_IP=/usr/local/bin/update-ip

sudo mkdir -p $LIB_DIR

sudo cp -rf requirements.txt $LIB_DIR/requirements.txt
sudo cp -rf src $LIB_DIR/
sudo -H pip3 install -r $LIB_DIR/requirements.txt

if [ -f $PROG ]; then
    sudo rm $PROG
fi

if [ -f $PROG_UPDATE_IP ]; then
    sudo rm $PROG_UPDATE_IP
fi
echo "#!/bin/bash" | sudo tee -a $PROG
echo "python3 $LIB_DIR/src/main.py \$@" | sudo tee -a $PROG

echo "#!/bin/bash" | sudo tee -a $PROG_UPDATE_IP
echo "python3 $LIB_DIR/src/update-ip.py \$@" | sudo tee -a $PROG_UPDATE_IP

sudo chmod 0755 $PROG_UPDATE_IP
sudo chmod 0755 $PROG
