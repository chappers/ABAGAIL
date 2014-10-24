clf;
close all;
clear;
c1 = 'g';
c2 ='b';
colordef white
%whitebg([0 0 0])

set(0,'DefaultFigureWindowStyle','docked')
%%
rhcFig = figure('Name', 'RHC %Error','NumberTitle','off');
saFig = figure('Name', 'SA %Error','NumberTitle','off');
gaFig = figure('Name', 'GA %Error','NumberTitle','off');

load('Vote_3a_20_100000.mat')
r = RHC_testError;
s = SA_testError;
g = GA_testError;


figure(rhcFig) ; hold all ;colormap(jet)
plotFixed(r)
figure(saFig); hold all;colormap(cool)
plotFixed(s)
figure(gaFig); hold all
plotFixed(g)

load('Vote_3b_20_100000.mat')
r = RHC_testError;
s = SA_testError;
g = GA_testError;

figure(rhcFig) ; hold all
plotFixed(r)
figure(saFig); hold all
plotFixed(s)
figure(gaFig); hold all
plotFixed(g)

load('Vote_3c_20_100000.mat')
r = RHC_testError;
s = SA_testError;
g = GA_testError;

figure(rhcFig) ; hold all
plotFixed(r)
figure(saFig); hold all
plotFixed(s)
figure(gaFig); hold all
plotFixed(g)

load('Vote_3d_20_100000.mat')
r = RHC_testError;
s = SA_testError;
g = GA_testError;

figure(rhcFig) ; hold all
plotFixed(r)
figure(saFig); hold all
plotFixed(s)
figure(gaFig); hold all
plotFixed(g)



break;
