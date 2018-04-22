function s = kalmanf(s)
 
% VECTOR VARIABLES:
%
% s.x = state vector estimate. In the input struct, this is the
%       "a priori" state estimate (prior to the addition of the
%       information from the new observation). In the output struct,
%       this is the "a posteriori" state estimate (after the new
%       measurement information is included).
% s.z = observation vector
% s.u = input control vector, optional (defaults to zero).
%
% MATRIX VARIABLES:
%
% s.A = state transition matrix (defaults to identity).
% s.P = covariance of the state vector estimate. In the input struct,
%       this is "a priori," and in the output it is "a posteriori."
%       (required unless autoinitializing as described below).
% s.B = input matrix, optional (defaults to zero).
% s.Q = process noise covariance (defaults to zero).
% s.R = measurement noise covariance (required).
% s.H = observation matrix (defaults to identity).

% set defaults for absent fields:
if ~isfield(s,'x'); s.x=nan*z; end
if ~isfield(s,'P'); s.P=nan; end
if ~isfield(s,'z'); error('Observation vector missing'); end
if ~isfield(s,'u'); s.u=0; end
if ~isfield(s,'A'); s.A=eye(length(x)); end
if ~isfield(s,'B'); s.B=0; end
if ~isfield(s,'Q'); s.Q=zeros(length(x)); end
if ~isfield(s,'R'); error('Observation covariance missing'); end
if ~isfield(s,'H'); s.H=eye(length(x)); end
 
if isnan(s.x)
    % initialize state estimate from first observation
    if diff(size(s.H))
        error('Observation matrix must be square and invertible for state autointialization.');
    end
    s.x = inv(s.H)*s.z;
    s.P = inv(s.H)*s.R*inv(s.H'); 
else

    % Prediction for state vector and covariance:
    s.x = s.A*s.x + s.B*s.u;
	s.P = s.A * s.P * s.A' + s.Q;
 
	% Compute Kalman gain factor:
    %%% smaller K == more resistant to noise
	K = s.P*s.H'*inv(s.H*s.P*s.H'+s.R);
 
	% Correction based on observation:
	s.x = s.x + K*(s.z-s.H*s.x);
	s.P = s.P - K*s.H*s.P;

    % Note that the desired result, which is an improved estimate
	% of the sytem state vector x and its covariance P, was obtained
	% in only five lines of code, once the system was defined. (That's
	% how simple the discrete Kalman filter is to use.)
 
 
end
 
 
end