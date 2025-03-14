%FREE VIBRATION RESPONSE -  A spring mass system with a mass of 20 lb-sec^2/in and a stiffness of 500
% lb/in is subject to initial displacement x0=3 and v0 = 4. plot the
% variations of the mass displacement, velocity, and acceleration

for i=1:101,
    t_(i) = 6 * i/100;
    x_(i) =  3.1048 * sin(5*t_(i) + 1.3102);
    x1_(i) = 15.524 * cos(5*t_(i) + 1.3102);
    x2_(i) = -77.62 * sin(5*t_(i) + 1.3102);
end
subplot(3,1,1);
plot(t_,x_);
title('Dispalcement Response');

subplot(3,1,2);
plot(t_,x1_);
title('Velocity Response');

subplot(3,1,3);
plot(t_,x2_);
title("Acceleration Response");

