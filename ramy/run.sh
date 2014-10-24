#!/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=./lib/ABAGAIL.jar:../../output/production/ABAGAIL/:../../../Common/JMatIO/lib/jmatio.jar:$CLASSPATH

#export RUNS = 3;
#export SAMPLES = 20;
#export ITERS = 100000;

# NN
#echo "NN 10 runs 10 samples 10 iters"
#{ time java VoteTest 3 20 100000 Vote_3a_20_100000.mat ;}  > NN_Vote3runsa_20samples_10000iters.log 2>&1 &

#echo "NN 100 runs 10 samples 10 iters"
#{ time java VoteTest 3 20 100000 Vote_3b_20_100000.mat ;} > NN_Vote3runsb_20samples_10000iters.log 2>&1 &

#echo "NN 100 runs 10 samples 100 iters"
#{ time java VoteTest 3 20 100000 Vote_3c_20_100000.mat ;} > NN_Vote3runsc_20samples_100000iters.log 2>&1 &
#echo "NN 100 runs 10 samples 1000 iters"
#{ time java VoteTest 3 20 100000 Vote_3d_20_100000.mat ;}  > NN_Vote3runsd_20samples_100000iters.log 2>&1

echo "GA 3 runs 200 samples 100000 iters pop 500 mate 300 mut 100"
{ time java VoteTest GA 3 200 1000000 GA_test_3runs_200samples_100000iters_500pop_300mate_100mut.mat 500 300 100 ;}  > GA_test_3runs_200samples_100000iters_500pop_300mate_100mut.log 2>&1 &

echo "GA 3 runs 200 samples 100000 iters pop 1000 mate 500 mut 200"
{ time java VoteTest GA 3 200 1000000 GA_test_3runs_200samples_100000iters_1000pop_500mate_200mut.mat 1000 500 200 ;}  > GA_test_3runs_200samples_100000iters_1000pop_500mate_200mut.log 2>&1 &

echo "GA 3 runs 200 samples 100000 iters pop 1000 mate 500 mut 200"
{ time java VoteTest GA 3 200 1000000 GA_test_3runs_200samples_100000iters_1000pop_500mate_200mut.mat 1000 500 200 ;}  > GA_test_3runs_200samples_100000iters_1000pop_500mate_200mut.log 2>&1 &

echo "GA 3 runs 200 samples 100000 iters pop 1000 mate 900 mut 700"
{ time java VoteTest GA 3 200 1000000 GA_test_3runs_200samples_100000iters_1000pop_900mate_700mut.mat 1000 900 700 ;}  > GA_test_3runs_200samples_100000iters_1000pop_900mate_700mut.log 2>&1



echo "done"


