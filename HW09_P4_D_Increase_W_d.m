clc; clear; close all

wd = 20; zwn= 10;
wn = sqrt(wd^2+zwn^2); z = zwn/wn;
GS1 = tf(wn^2,[1 2*z*wn wn^2])

wd = 30; zwn= 10;
wn = sqrt(wd^2+zwn^2); z = zwn/wn;
GS2 = tf(wn^2,[1 2*z*wn wn^2])

wd = 40; zwn= 10;
wn = sqrt(wd^2+zwn^2); z = zwn/wn;
GS3 = tf(wn^2,[1 2*z*wn wn^2])

figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Apple');

subplot(1,2,1); hold on
step(GS1)
step(GS2)
step(GS3)
grid on; title('Time Response')
axis equal; axis([0 0.6 0 1.5])
legend('\omega_d = 20','\omega_d = 30','\omega_d = 40')

subplot(1,2,2); hold on
pzmap(GS1)
pzmap(GS2)
pzmap(GS3)
grid on; title('Pole Placement')
axis([-10 0 -50 50]); axis equal
legend('\omega_d = 20','\omega_d = 30','\omega_d = 40')
