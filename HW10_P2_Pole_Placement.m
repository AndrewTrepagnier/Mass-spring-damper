clc; clear; close all

GS1 = tf(1,[1 7 2 5 2 3])
GS2 = tf(1,[1 7 2 5 2 -3])
GS3 = tf(1,[1 0 7 2 5 2 3])


figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Apple');

subplot(2,3,1); hold on
pzmap(GS1)
grid on; title('Pole Placement for G_1(S)')
axis([-10 1 -4 4]); axis equal

subplot(2,3,2); hold on
pzmap(GS2)
grid on; title('Pole Placement for G_2(S)')
axis([-10 1 -4 4]); axis equal

subplot(2,3,3); hold on
pzmap(GS3)
grid on; title('Pole Placement for G_3(S)')
axis([-10 1 -4 4]); axis equal

