clc; clear; close all

GS8 = tf(1,[1 -2 -5 8 -2 -12])
GS9 = tf(1,[1 4 3 2 1 4 4])

figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Apple');

subplot(2,3,2); hold on
pzmap(GS8)
grid on; title('Pole Placement for G(S)')
axis([-4 4 -1 1]); axis equal

subplot(2,3,3); hold on
pzmap(GS9)
grid on; title('Pole Placement for G(S)')
axis([-3.5 1 -1 1]); axis equal

