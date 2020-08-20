#!/bin/bash

i=1
while :
do
    hadoop fs -rm -r ./c1/output$i/
    mapred streaming -input ./data.txt -output ./c1/output$i -mapper ./mapper.py -reducer ./reducer.py -file ./c1/centroids.txt -file ./mapper.py
    rm ./c1/centroids.txt
    hadoop fs -copyToLocal ./c1/output$i/part-00000 ./c1/centroids.txt
    hadoop fs -copyToLocal ./c1/output$i/part-00000 ./c1/output/centroids$i.txt
    if [ $i = 20 ]
    then
        rm ./centroids.txt
        break
    fi
    i=$((i+1))
done
