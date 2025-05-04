clc; clear; close all

GS1 = zpk([],[-1 -1-5i -1+5i],26)
GS2 = zpk([],[-4 -1-5i -1+5i],104)
GS3 = zpk([],[-1 -4-5i -4+5i],41)


figure(1); set(gcf,'units','normalized','outerposition',[0 0 1 1],'color','w','Name','Apple');

subplot(2,3,[ 1 2]); hold on
step(GS1)
step(GS2)
step(GS3)
grid on; title('Time Response')
axis equal; axis([0 6 0 1.5])
legend('G_1(S)','G_2(S)','G_3(S)')


subplot(2,3,4); hold on
pzmap(GS1)
grid on; title('Pole Placement for G_1(S)')
axis([-5 0 -10 10]); axis equal

subplot(2,3,5); hold on
pzmap(GS2)
grid on; title('Pole Placement for G_2(S)')
axis([-5 0 -10 10]); axis equal

subplot(2,3,6); hold on
pzmap(GS3)
grid on; title('Pole Placement for G_3(S)')
axis([-5 0 -10 10]); axis equal



