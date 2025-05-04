clc; clear; close all

wn = 10; z= 0.3;
GS1 = tf(wn^2,[1 2*z*wn wn^2])

wn = 20; z= 0.3;
GS2 = tf(wn^2,[1 2*z*wn wn^2])

wn = 30; z= 0.3;
GS3 = tf(wn^2,[1 2*z*wn wn^2])

figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Apple');

subplot(1,2,1); hold on
step(GS1)
step(GS2)
step(GS3)
grid on; title('Time Response')
axis equal; axis([0 2 0 1.5])
legend('\omega_n = 10','\omega_n = 20','\omega_n = 30')

subplot(1,2,2); hold on
pzmap(GS1)
pzmap(GS2)
pzmap(GS3)
grid on; title('Pole Placement')
axis([-10 0 -40 40]); axis equal
legend('\omega_n = 10','\omega_n = 20','\omega_n = 30')

