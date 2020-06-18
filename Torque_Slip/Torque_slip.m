% Creating a plot of the torque-speed curve of the induction motor 

%% 
% Initiallisation of values required
% Enter the physical parameters of induction motor
Sr1 = 0.640;                % Stator resistance
Sx1 = 1.100;                % Stator reactance
Rr2 = 0.333;                % Stator referred Rotor resistance
Rx2 = 0.464;                % Stator referred Rotor reactance
xm = 26.3;                  % Magnetization branch reactance
v_phase = 440 / sqrt(3);    % Applied Phase voltage
n_sync = 1800;              % Synchronous speed (r/min)
w_sync = 188.5;             % Synchronous speed (rad/s)

%% 
% Calculating the Thevenin voltage and impedance

z_th = ((j*xm) * (Sr1 + j*Sx1)) / (Sr1 + j*(Sx1 + xm));
r_th = real(z_th);
x_th = imag(z_th);
v_th = v_phase * ( xm / sqrt(Sr1^2 + (Sx1 + xm)^2) );

%% 
% Now calculate the torque-speed characteristic for many
% slips between 0 and 1.  Note that the first slip value 
% is set to 0.001 instead of exactly 0 to avoid divide-
% by-zero problems.
% For Slip between 1 to 2, machine works in braking region
%For slip between 0 to -2, machine works in generator region

s = (-2:.002:2);                  % Slip
s(1000) = 0.001;                  % to avoid zero by zero problem

%% 
% Calculate torque for original rotor resistance
for i = 1:2001
   t_induced(i) = (3 * v_th^2 * Rr2 / s(i)) / ...
            (w_sync * ((r_th + Rr2/s(i))^2 + (x_th + Rx2)^2) );
end

%% 
% Plot the torque-speed curve
plot(s,t_induced,'Color','k','LineWidth',2.0);
hold on;
xlabel('s','Fontweight','Bold');
ylabel('\tau_{ind}','Fontweight','Bold');
title ('Torque-Slip Characteristic','Fontweight','Bold');
xline(0);
xline(1);
grid on;
hold off;