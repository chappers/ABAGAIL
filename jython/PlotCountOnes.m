clf(figure(1))
figure(1)



%%
X = removeZeros(GA_searchTimes);
Y = removeZeros(GA_fitness);
semilogx(cumsum(X,2)', Y');
title('GA Fitness vs clock time');

figure(2)
semilogy(ProblemSize,GA_times, '-O')
title('GA Time vs Problem Size');

figure(3)
semilogy(ProblemSize, GA_threshold,'-O');
title('GA Threshold vs Problem Size');
%%
figure(4)
Y = removeZeros(RHC_fitness);
X = RHC_searchTimes;
plot(Y')
