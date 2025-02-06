# dns-migration-check

### install
```
pip install -r requirements.txt
```

### usage
```
./dns-migration-check.py --help

python3 ./dns-migration-check.py -f zonefile -z zonename -p primary_nameserver -s secondary_nameserver

python3 ./dns-migration-check.py -f test_com_bind.zone -z test.com -p 8.8.8.8 -s ada.ns.cloudflare.com
```

### zone file format
```
<<SOA field>>

<<NS filed>>

<< Record Set>>
```

comment $TTL, $ORIGIN filed.  

dnspython3 module has error during reading zone file, if this fields is existed.

example
```
;; SOA Record
@        3600           IN      SOA     ns1-100.azure-dns.com.   azuredns-hostmaster.microsoft.com       (
                        1        ;serial
                        3600     ;refresh
                        300      ;retry
                        2419200  ;expire
                        300      ;minimum ttl
)

;; NS Records
@       172800  IN      NS      ns1-105.azure-dns.com.
@       172800  IN      NS      ns2-105.azure-dns.net.
@       172800  IN      NS      ns3-105.azure-dns.org.
@       172800  IN      NS      ns4-105.azure-dns.info.

;;$TTL 300
;;$ORIGIN test.com

;; MX Records

;; A Records
test1        300     IN      A       10.1.1.1
test2        300     IN      A       10.1.1.2
test3        300     IN      A       10.1.1.3

;; CNAME Records
test3     300     IN      CNAME   test1.test.com
```

