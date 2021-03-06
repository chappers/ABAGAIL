clear variables; close all;

path=load('jython/mimic_samplesVary.mat');
colordef black
set(0,'DefaultFigureWindowStyle','docked')

names = fieldnames(path);
ax=[];
%for i = 1:length(names)
%  n = names{i};
%routes = {'RHC', 'SA', 'GA', 'MIMIC'};
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
      fitness = path.(fitstr{:})';
      %idx = find(fitness > 0);
      %fitness = fitness(idx);
      
      iters = path.(iterstr{:});
      numIters = size(iters,2);
      
      [F, sortInd] = sort(fitness(:));
      f= reshape(F, size(fitness'));
      %f( :, ~any(f,1)) = [];

      plot(f');
   
      %end
      
      figure('Name',routes{r},'NumberTitle','off');
      %set(gca,'position',[0.03 0.03 1 1])
      ax(end+1) = gca;
      %plot(path.RHC_fitness)
      ifix = zeros( 2*size(sortInd,1),1);
      ifix(2:2:end) = 2*sortInd ;
      ifix(1:2:end) = ifix(2:2:end)-1
      p = path.(routes{r});
      p = p(ifix,:);
    
      p( ~any(p,2),:) = [];     

      
      %%
      hold all
      
      cols = N;%length(path.(n));
      rows = size(p,1)/2; %length(path.(curves{1}))%length(path.RHC_fitness);
      colors = parula(rows);
      for j = 1:rows
          %p = path.(names{i});
          xInd= (j-1)*2 +1;
          yInd = xInd+1;
          X = p(xInd,1:cols);
          Y = p(yInd,1:cols);
          Z = (j/2)*ones(cols,1);
          %scatter3(X, Y, Z,'filled','r') ,   
          plot3(X, Y,Z,'Color', colors(j,:),'LineWidth',5);
          %drawnow;
      end     %%
      X = path.MIMIC_best(1,:);
      Y = path.MIMIC_best(2,:);
      Z = (j/10)*ones(cols,1)
      %scatter3(X, Y, Z ,'filled','r')
      %plot3(X,Y,Z,'b','LineWidth',5);
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