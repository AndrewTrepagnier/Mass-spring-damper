clc; clear; close all

t = 0:0.01:8;
u = 1*ones(size(t));
y = 2 + exp(-t).*(-cos(5*t) + 11/5*sin(5*t));

figure(1); set(gcf,'color','w');
hold on; box on; grid on; 
axis([min(t) max(t) 0 4]); 
plot(t,u,'LineWidth',1,'Color','b')
plot(t,y,'LineWidth',1,'Color','m')
legend('u(t)','y(t)'); 
