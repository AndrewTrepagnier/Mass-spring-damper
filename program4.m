% 
% % Problem 4
% zeta1 = 0;
% zeta2 = 0.06;
% zeta3 = 0.1;
% zeta4 = 0.2;
% zeta5 = 0.4;
% zeta6 = 1;
% 
% 
% % y2 = 1 / (sqrt( (1 - r^2)^2 + (2*zeta2*r)^2) );
% % plot(r, y2);
% for i=1:101,
%     r(i) = 3* i/101;
%     y1(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta1*r(i))^2) );
% end
% 
% hold on;
% plot(r,y1);
% for i=1:101,
%     r(i) = 3* i/101;
%     y2(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta2*r(i))^2) );
% end
% plot(r,y2);
% hold on;
% 
% for i=1:101,
%     r(i) = 3* i/101;
%     y3(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta3*r(i))^2) );
% end
% plot(r,y3);
% hold on;
% 
% for i=1:101,
%     r(i) = 3* i/101;
%     y4(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta4*r(i))^2) );
% end
% plot(r,y4);
% hold on;
% 
% for i=1:101,
%     r(i) = 3* i/101;
%     y5(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta5*r(i))^2) );
% end
% plot(r,y5);
% hold on;
% 
% for i=1:101,
%     r(i) = 3* i/101;
%     y6(i) = 1 / (sqrt( (1 - r(i)^2)^2 + (2*zeta6*r(i))^2) );
% end
% plot(r,y6);
% hold off;
% 
% 
% title('System Frequency Response');
% xlabel('r (w/wn)');
% xlim([0 3]);
% ylim([0 10]);
% ylabel('KX/F');
% legend('Zeta = 0', 'Zeta = 0.06', 'Zeta = 0.10', 'Zeta = 0.2', 'Zeta = 0.04', 'Zeta = 1');
% grid;

% Problem 4
zeta = [0, 0.06, 0.1, 0.2, 0.4, 1];  
r = linspace(0, 3, 101);  

figure;
hold on;

% for all zeta values
for j = 1:length(zeta)
    y = 1 ./ sqrt((1 - r.^2).^2 + (2*zeta(j)*r).^2);
    plot(r, y);
end

hold off;

% Plot formatting
title('System Frequency Response');
xlabel('r (w/wn)');
xlim([0 3]);
ylim([0 10]);
ylabel('KX/F');
legend('Zeta = 0', 'Zeta = 0.06', 'Zeta = 0.10', 'Zeta = 0.2', 'Zeta = 0.4', 'Zeta = 1');
grid;