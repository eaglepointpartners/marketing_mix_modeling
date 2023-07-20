#!/bin/bash

> response.txt

for f in $(echo $files)
    do
        if [[ -f "$f" ]]; then
            printf "%0.s#" {1..132} && echo
            realpath $f
            trivy --exit-code 1 --severity HIGH,CRITICAL fs --scanners $check $f
            echo $? >> response.txt
            printf "%0.s#" {1..132} && echo
        fi
done

if [[ $(grep 1 ./response.txt | sort -u) -ne 0 ]]; then
    exit 1
fi
