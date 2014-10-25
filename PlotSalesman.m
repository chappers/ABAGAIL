clear variables; close all;
colors = gray(5);
path=load('jython/mimic_samplesVary.mat');
colordef white
set(0,'DefaultFigureWindowStyle','docked')

names = fieldnames(path);
ax=[];
%for i = 1:length(names)
%  n = names{i};
%routes = {'RHC', 'SA'};
routes = {'MIMIC'};
N = path.numPoints;
%%
for r = 1:numel(routes)
  curves = {[routes{r} '_fitness'] [routes{r} '_iterations']}
      %for c = 1:2
      fitstr = curves(1)
      iterstr = curves(2)
      figure('Name', fitstr{:}, 'NumberTitle', 'off');
      hold all;
      %set(gca,'position',[0.03 0.03 1 1])
      fitness = path.(fitstr{:});
      %idx = find(fitness > 0);
      %fitness = fitness(idx);
      
      iters = path.(iterstr{:});
      %idx = find(iters > 0);
      %iters = iters(idx);
      %colormap(jet);
      plot(fitness');
   %end
      
      figure('Name',routes{r},'NumberTitle','off');
      %set(gca,'position',[0.03 0.03 1 1])
      ax(end+1) = gca;
      %plot(path.RHC_fitness)
      p = path.(routes{r});
      %%
      hold all
      cols = N;%length(path.(n));
      rows = size(p,1)/2 %length(path.(curves{1}))%length(path.RHC_fitness);
      for j = 1:rows
          %p = path.(names{i});
          xInd= (j-1)*2 +1;
          yInd = xInd+1;
          X = p(xInd,1:cols);
          Y = p(yInd,1:cols);
          scatter(X, Y) ,   plot(X, Y, 'Color', colors(3,:));
          %drawnow;
      end
      plot(X,Y,'b','LineWidth',5);
  hold off

end
break;
  %%
  cooling = path.SA_cooling_iterations;%(:,1:end/2);
  v=(sort(unique(cooling)));
  v = v(find(v >0));
  tmp =path.SA_cooling_iterations;
  tmp = tmp(find(tmp >0));
  numIters = size(path.SA_cooling_iterations,1);%numel(unique(tmp));
  numRuns = length(tmp) / numIters;
  iters = reshape(tmp, [numIters numRuns]);
  fitness = reshape(path.SA_cooling_fitness(1:numIters,1:numRuns), [numRuns, numIters]);
  figure;
 % set(gca,'position',[0 0 1 1])
  num = numel(v)
  colormap(jet(num));
 plot(v, fitness);
  colormap(pink)
 figure; hist(fitness,20)
 %set(gca,'position',[0 0 1 1])