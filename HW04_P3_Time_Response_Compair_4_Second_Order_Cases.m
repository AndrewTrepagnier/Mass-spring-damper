clc; clear; close all

M = 1; K = 1; 
Wn = sqrt(K/M);

x_o = 1; x_dot_o = 1;

t = 0:0.01:20;

x_not_damped = x_o*cos(Wn*t) + x_dot_o/Wn*sin(Wn*t);
x_dot_not_damped = Wn*( - x_o*sin(Wn*t) + x_dot_o/Wn*cos(Wn*t) );

x_critical_damped = exp(-Wn*t).*( ( Wn*x_o + x_dot_o )*t + x_o );
x_dot_critical_damped = -Wn*exp(-Wn*t).*( ( Wn*x_o + x_dot_o )*t + x_o ) + exp(-Wn*t).*( Wn*x_o + x_dot_o );

C = 5;
z_o = C/(2*sqrt(K*M));
x_over_damped = exp(-z_o*Wn*t).*( x_o*cosh(Wn*sqrt(z_o^2-1)*t) + 1/sqrt(z_o^2-1)*( z_o*x_o + x_dot_o/Wn )*sinh(Wn*sqrt(z_o^2-1)*t) );
x_dot_over_damped = -z_o*Wn*exp(-z_o*Wn*t).*( x_o*cosh(Wn*sqrt(z_o^2-1)*t) + 1/sqrt(z_o^2-1)*( z_o*x_o + x_dot_o/Wn )*sinh(Wn*sqrt(z_o^2-1)*t) ) + ... 
           Wn*sqrt(z_o^2-1)*exp(-z_o*Wn*t).*( x_o*sinh(Wn*sqrt(z_o^2-1)*t) + 1/sqrt(z_o^2-1)*( z_o*x_o + x_dot_o/Wn )*cosh(Wn*sqrt(z_o^2-1)*t) );


C = 0.4;
z_u = C/(2*sqrt(K*M));
Wd = Wn*sqrt(1-z_u^2);

x_under_damped = exp(-z_u*Wn*t).*( x_o*cos(Wd*t) + 1/sqrt(1-z_u^2)*(z_u*x_o + x_dot_o/Wn)*sin(Wd*t));
x_dot_under_damped = -z_u*Wn*exp(-z_u*Wn*t).*( x_o*cos(Wd*t) + 1/sqrt(1-z_u^2)*(z_u*x_o + x_dot_o/Wn)*sin(Wd*t)) + ...
                     Wd*exp(-z_u*Wn*t).*( - x_o*sin(Wd*t) + 1/sqrt(1-z_u^2)*(z_u*x_o + x_dot_o/Wn)*cos(Wd*t));



figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Time Response');

subplot(2,1,1)
hold on; box on; grid on

plot(t,x_not_damped,'LineWidth',1,'Color','b')
plot(t,x_critical_damped,'LineWidth',1,'Color','r')
plot(t,x_over_damped,'LineWidth',1,'Color','m')
plot(t,x_under_damped,'LineWidth',1,'Color','g')

axis([0 max(t) -1.6 1.6]);
title('Displacement'); xlabel('Time (sec)'); ylabel('Displacement')
legend('Not Damped','Critical Damped','Over Damped','Under Damped')

subplot(2,1,2)
hold on; box on; grid on

plot(t,x_dot_not_damped,'LineWidth',1,'Color','b')
plot(t,x_dot_critical_damped,'LineWidth',1,'Color','r')
plot(t,x_dot_over_damped,'LineWidth',1,'Color','m')
plot(t,x_dot_under_damped,'LineWidth',1,'Color','g')

axis([0 max(t) -1.6 1.6]);
title('Velocity'); xlabel('Time (sec)'); ylabel('Velocity')
legend('Not Damped','Critical Damped','Over Damped','Under Damped')


figure(2); set(gcf,'units','normalized','outerposition',[0.2 0.2 0.3 0.5],'color','w','Name','Phase Plane');
hold on; box on; grid on

axis equal

plot(x_not_damped,x_dot_not_damped,'LineWidth',1,'Color','b')
plot(x_critical_damped,x_dot_critical_damped,'LineWidth',1,'Color','r')
plot(x_over_damped,x_dot_over_damped,'LineWidth',1,'Color','m')
plot(x_under_damped,x_dot_under_damped,'LineWidth',1,'Color','g')

title('Phase Plane'); xlabel('Displacement'); ylabel('Velocity')
legend('Not Damped','Critical Damped','Over Damped','Under Damped')

