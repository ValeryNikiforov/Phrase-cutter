echo "decoder-test $1" > decoder-test.scp 
./decode.sh | python3 make_segments.py $1 $2 $3 > segmentation.log
./decode.sh > result.txt