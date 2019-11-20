#!/usr/bin/env bash

out=`date`
echo "Loading wifi sampler.."
nc $1 23 <telnet.in >"log/$out $1.log" 

