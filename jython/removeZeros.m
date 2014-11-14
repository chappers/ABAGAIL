function x = removeZeros(A)
x = A;
x(x<=0) = NaN;
end