## Installation
Now it's supported only on linux distro. Windows may be supported next

### Prerequisites
You need install following packages :
- ca-certificates
- python3
- curl

Commands : 
```bash
sudo apt update
sudo apt install curl ca-certificates python3
```

### Run installation
Clone this repository or download the zip file. Navigate to cloned directory or extracted directory. After that run the following command : 
```bash
./install.sh
```
Then program will take a rest to do installation.


## Usage
After the program has been installed, you can reload the terminal or system to take an effects. After that, just run the program : 
```shell
check-public-ip

```

If you found the error related to the certificate : 
```
Traceback (most recent call last):
  File "/usr/local/lib/check-ip-public/src/main.py", line 49, in <module>
    print(checkpublicip(args.ifaces, args.timeout).strip(), end="")
  File "/usr/local/lib/check-ip-public/src/main.py", line 30, in checkpublicip
    return geturlfromiface("https://checkip.amazonaws.com", iface, timeout)
  File "/usr/local/lib/check-ip-public/src/main.py", line 20, in geturlfromiface
    curl.perform()
pycurl.error: (77, 'error setting certificate verify locations:\n  CAfile: /etc/pki/tls/certs/ca-bundle.crt\n  CApath: none')
```

It's because the `pycurl` cannot find your certificates for sending requests. To fix this, you can simply run : 
```
sudo cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt
```
Reference: https://stackoverflow.com/questions/3160909/how-do-i-deal-with-certificates-using-curl-while-trying-to-access-an-https-url
