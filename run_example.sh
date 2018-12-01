# Wait for DNS to come up
sleep 30s

# Run the Christmas Tree
python3 /full/path/to/main.py --clientid=my-client-id --endpoint=myendpoint-ats.iot.ap-southeast-2.amazonaws.com --cacert=/path/to/AmazonRootCA1.pem --privatekey=/path/to/deviceid-private.pem.key --cert=/path/to/deviceid-certificate.pem.crt --topic=mytopicname
