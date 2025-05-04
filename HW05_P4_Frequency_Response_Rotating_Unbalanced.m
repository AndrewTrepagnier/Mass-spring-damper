clc; clear; close all

figure(1); set(gcf,'units','normalized','outerposition',[0.5 0.5 0.3 0.5],'color','w','Name','Frequency Response');
hold on; box on; grid on

r = 0:0.01:3;

z1 = 0;
xp_1 = r.^2./sqrt((1-r.^2).^2+(2*z1*r).^2);

z2 = 0.06;
xp_2 = r.^2./sqrt((1-r.^2).^2+(2*z2*r).^2);

z3 = 0.1;
xp_3 = r.^2./sqrt((1-r.^2).^2+(2*z3*r).^2);

z4 = 0.2;
xp_4 = r.^2./sqrt((1-r.^2).^2+(2*z4*r).^2);

z5 = 0.4;
xp_5 = r.^2./sqrt((1-r.^2).^2+(2*z5*r).^2);

z6 = 1;
xp_6 = r.^2./sqrt((1-r.^2).^2+(2*z6*r).^2);

plot(r,xp_1,'LineWidth',1,'Color','k')
plot(r,xp_2,'LineWidth',1,'Color','b')
plot(r,xp_3,'LineWidth',1,'Color','g')
plot(r,xp_4,'LineWidth',1,'Color','r')
plot(r,xp_5,'LineWidth',1,'Color','m')
plot(r,xp_6,'LineWidth',1,'Color','c')

title('Rotate Unbalanced'); xlabel('r','FontSize',20); ylabel('$\frac{MX}{me}$      ','Interpreter','latex','rotation',0,'FontSize',25)
legend('z = 0','z = 0.06','z = 0.1','z = 0.2','z = 0.4','z = 1')

axis([0 max(r) 0 10]);