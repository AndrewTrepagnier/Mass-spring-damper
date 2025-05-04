clc; clear; close all

t = 0:0.01:8;
u = exp(-2*t);
y = 1/10*( exp(-2*t) - exp(-t/2).*(-cos(sqrt(31)/2*t) - 23/sqrt(31)*sin(sqrt(31)/2*t)) );

figure(1); set(gcf,'color','w');
hold on; box on; grid on; 
axis([min(t) max(t) -0.3 1.2]); 
plot(t,u,'LineWidth',1,'Color','b')
plot(t,y,'LineWidth',1,'Color','m')
legend('u(t)','y(t)'); 
