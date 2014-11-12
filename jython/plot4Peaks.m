clear variables; close all;

path=load('4P/MIMIC_80.mat');
colordef black
set(0,'DefaultFigureWindowStyle','docked')

names = fieldnames(path);
ax=[];
%for i = 1:length(names)
%  n = names{i};
%routes = {'RHC', 'SA', 'GA', 'MIMIC'};
%routes = {'GA'};
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
      numIters = size(iters,2);
 
      [A,I]=sort(max(fitness,[],2),'ascend')
      F = fitness(I,:);
      [~,ind] = sort(fitness(:),'descend');
%      f= reshape(F, size(fitness'));
      %f( :, ~any(f,1)) = [];

      plot(iters(1,:),F);
   
      %end
      
      figure('Name',routes{r},'NumberTitle','off');
      
      %set(gca,'position',[0.03 0.03 1 1])
      ax(end+1) = gca;
      %plot(path.RHC_fitness)
      foo = fitness';
      [x,bar] = sort(foo(:));
      p = path.(routes{r});
      q = p(bar,:);
      y =  q .*  repmat(foo(bar), 1,size(q,2));
      pcolor(y(:,1:22))
      %p( ~any(p,2),:) = [];     

      
      %%
      hold all
      
      cols = N;%length(path.(n));
      rows = size(p,1)/2; %length(path.(curves{1}))%length(path.RHC_fitness);
      colors = parula(rows);
  
      %scatter3(X, Y, Z ,'filled','r')
      %plot3(X,Y,Z,'b','LineWidth',5);
  hold off

end