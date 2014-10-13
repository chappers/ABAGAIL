#!/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=./lib/ABAGAIL.jar:../../output/production/ABAGAIL/:../../../Common/JMatIO/lib/jmatio.jar:$CLASSPATH
#mkdir -p data/plot logs image

# NN
echo "NN 10 runs 10 samples 10 iters"
time (java VoteTest 10 10 10 Vote_10_10_10.mat)   > NN_Vote10runs_10sames_10iters.log &

echo "NN 100 runs 10 samples 10 iters"
time(java VoteTest 100 10 10 Vote_100_10_10.mat )  > NN_Vote100runs_10sames_10iters.log &

echo "NN 100 runs 10 samples 100 iters"
time(java VoteTest 100 10 100 Vote_100_10_100.mat )  > NN_Vote100runs_10sames_100iters.log &
echo "NN 100 runs 10 samples 1000 iters"
time (java VoteTest 100 10 1000 Vote_100_10_1000.mat)   > NN_Vote100runs_10sames_1000iters.log &






# count ones
echo "count ones"
#jython countones.py

# continuous peaks
echo "continuous peaks"
#jython continuouspeaks.py

# knapsack
echo "Running knapsack"
#jython knapsack.py

