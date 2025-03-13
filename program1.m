%% Plot the response of the system with Wn = 5rad/s, Z = 0.05, 0.1, 0.2

%Subjected to initial conditions: x0=0, x0_dot = 60 cm/s

wn = 5;
zeta = [0.05; 0.1; 0.2];
x0 = 0;
v0=60;
t0=0;
deltat = 0.01; % time steps
tf = 6;
t = t0:deltat:tf;
for i=1:length(zeta),
    wd = sqrt(1-zeta(i).^2)*wn; % damped freq
    x = exp(-zeta(i)*wn*t).*(((zeta(i)*x0 + v0)/wd)*sin(wd*t)+x0*cos(wd*t));
    plot(t,x);
        hold on
end
title('Response to initial excitiation')
xlabel('t[s]')
ylabel('x(t)')
grid
