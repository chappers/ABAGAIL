function plotFixed(x)
[M N] = size(x);
for i=1:M
    I = find(x(i,:) ~= 0);
    last = N;
    if(~isempty(I))
        last = I(end);
    end
    plot(x(i,1:last));
end

end
