#!/bin/bash

cd $(dirname $0)/..
BASEDIR=`pwd`
IDL=$BASEDIR/thrift/pitaya.thrift
SERVER=$BASEDIR/server
CLIENT=$BASEDIR/client
echo -e "This script is going to delete thrift generated code as below\n\tServer: $SERVER/pitaya/*\n\tClient: $CLIENT/piyata/*"
echo -e "and regenerate them using the definition as below\n\tIDL: $IDL"
read -r -p "Are you sure? [y/N] " response
case $response in
    [yY][eE][sS]|[yY]) 
	rm -r $SERVER/pitaya/*
	thrift -r -out $SERVER --gen py $IDL
	echo "Server-side code has been generated."
	rm -r $CLIENT/pitaya/*
	thrift -r -out $CLIENT --gen php $IDL
	echo "Client-side code has been generated."
        ;;
    *)
        exit;;
esac


