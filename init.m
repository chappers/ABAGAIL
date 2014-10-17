clf;
close all;
clear;
c1 = 'g';
c2 ='b';
colordef black


set(0,'DefaultFigureWindowStyle','docked')
%%
data = 'ramy'%'../../saved_data/Vote*';
%data = '*vote5pct';
%%
[status, cmdout] = system(['ls ' data '*.mat'])
%[status, cmdout] = system(['ls ' data '*Ada*.mat'])
%%
cmdout2 = [];
%[status, cmdout2] = system(['ls ' data '*PrunedJ48-C*.mat'])
%%
%cmdout = [cmdout cmdout2]
files = strsplit(cmdout)
files = sort_nat(files)
%cmdout = dir('*.mat'); files={};
%[files{1:length(cmdout),1}] = deal(cmdout.name);

%%
ax=[];
count = 1;
fixedFiles ={};
for file = files(1:end)
    if (isempty(char(file)))
        continue;
    end
    fixedFiles{end+1} = char(file);
end
fixedFiles
%%
All =[];
for file = fixedFiles(1:end)
  T = load(char(file));
  All= [All T];
end
    %weights = ( 1:N )*  100 / N;
C.RHC_trainingError = vertcat(All.RHC_trainingError)';
C.GA_trainingError = vertcat(All.GA_trainingError)';
C.SA_trainingError = vertcat(All.SA_trainingError)';

    figure('Name',[char(file) 'RHC %Error'],'NumberTitle','off');
    set(gca,'position',[0.03 0.03 1 1])
    ax(end+1) = gca;


    plot(C.RHC_trainingError )

    hold off;
    figure('Name',[char(file) 'SA %Error'],'NumberTitle','off');
    set(gca,'position',[0.03 0.03 1 1])
    ax(end+1) = gca;

    hold on;

    plot(C.SA_trainingError )
    hold off;

    figure('Name',[char(file) 'GA %Error'],'NumberTitle','off');
    set(gca,'position',[0.03 0.03 1 1])
    ax(end+1) = gca;
    hold on;

    plot(C.GA_trainingError)
    set(gca,'position',[0.03 0.03 1 1])
    hold off;

%linkaxes(ax);
ylim([0 1]);
%axis( [1 size(RHC_trainingError,2) 0 100]);
break
%%
newfig = ax(1)
newAx = get(newfig,'Children');
for i = 2 : numel(ax)
    tmpAx=get(ax(i), 'Children')
    for j = 1 : numel(tmpAx)
        axChildren = get(tmpAx(j),'Children');
        copyobj(axChildren, newAx(j));
    end
end
%%
linkaxes(ax);
axis( [1 size(trainErrorPercent,2) 0 .8]);
break
L = findobj(50,'type','line');
copyobj(L,findobj(60,'type','axes'));
%%
figure
plot(mean(trainErrorRMS)  );hold on;
plot(testErrorRMS'); hold off;

%%
colors = colormap;
rng('shuffle');
%c1 = colors(randi(size(colors,1),1,1),:);
%c2 = colors(randi(size(colors,1),1,1),:);
%%
vote_Momentum2 = load('saved_data/vote_MLP.momentum2.mat');
figure('Name','vote_Momentum2','NumberTitle','off');
plot(mean(vote_Momentum2.trainErrorRMS), 'Color', c1 );hold on;
plot(mean(vote_Momentum2.testErrorRMS), 'Color',c2); hold off;

%%
iris_Momentum2 = load('saved_data/iris_MLP.momentum2.mat')
figure('Name','iris_Momentum2','NumberTitle','off');
 plot(mean(iris_Momentum2.trainErrorRMS), 'Color', c1 );hold on;
 plot(mean(iris_Momentum2.testErrorRMS), 'Color',c2); hold off;
