clear variables; close all
colors = gray(5);
path = load('jython/ts.mat');
colordef black

names = fieldnames(path);
ax=[];
for i = 1:length(names)
  n = names{i};
  figure('Name',n,'NumberTitle','off');
  %set(gca,'position',[0.03 0.03 1 1])
  ax(end+1) = gca;
  %plot(path.RHC_fitness)
  p = path.RHC;
 hold off
  %%
  hold on
  for j = 1:size(p,1) /2
   %p = path.(names{i});


   xInd= (j-1)*2 +1;
   yInd = xInd+1;
   X = p(xInd,:);
   Y = p(yInd,:);
   scatter(X, Y) ,   plot(X, Y, '-y', 'Color', colors(2,:));
  end
  plot(X,Y,'r');
  hold off
end
