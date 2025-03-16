% There are many different ways to calculate the transient response of a
% spring-mass-damper system. In linear systems, the frequency of a system's
% response is exaclty equal to the frequency of the excitation. 

% in this problem, the given system response is y(t) = 0.002cos(40t).
% Therefore, w = 40 rad/s

%In other words: The system's response equation is given y(t) = 0.002*cos(40*t) which describe the system's motion due to the external force.
% But the external force equation is unknown f(t) = F_0*cos(w*t).

%Since system response general form is y(t) = Y*cos(w*t) so Y = 0.002 and w = 40 are known
%and since f(t) = F_0*cos(w*t), then F_o and w are unknown.

%Define knowns of the system
M = 150; %kg
K = 60000; %N/m
C = 1200; %N.s/m

%Parameters of the system's response
Y = 0.002;
w = 40;

%Calculations
wn = sqrt(K/M);
r = w/wn;
Z = C/(2*sqrt(K*M));

F_o = Y*K*(sqrt((1-r^2)^2 + (2*Z*r)^2));
disp(F_o);
disp(w);

% Plotting
for i=1:101,
    t(i) = 6* i/100;
    y(i) = Y*cos(40*t(i));
    f_(i) = F_o*cos(40*t(i));
end

subplot(2,1,1);
plot(t,y);
subplot(2,1,2);
plot(t,f_);

