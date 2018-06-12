function g = sigmoidFunction(z)
%	Compute sigmoid function

  % You need to return the following variables correctly
  g = zeros(size(z));

  % Instructions: z can be a matrix, vector or scalar
  g = 1.0 ./ ( 1.0 + exp(-z)); % For Matlab
  % g = 1.0 ./ ( 1.0 + e.^(-z)); % For Octave, it can use 'exp(1)' or 'e'
    
end