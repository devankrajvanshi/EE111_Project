clear all;

%initiallisation
n=425;                            %No of Turns per unit length
Area=3;

%% 
%Area is set such that field is in the bounds of the BH curve
%Due to BH curve given, we'll observe non-sinusodial behaviour of current
%drawn

Number_of_Entries=1000;             %No of entries of Input Voltage Matrix
type voltage_matrix.txt;            %Input Voltage Waveform
Voltage_vector=readmatrix('voltage_matrix.txt');
time=Voltage_vector(1:Number_of_Entries,1);      
voltage=Voltage_vector(1:Number_of_Entries,2); %230V :peak value

%% 
%Calculating Magnetic Flux
Mag_Flux(1)=0;                          %initial vaue of Flux
for i = 2:Number_of_Entries
    Mag_Flux(i)=Mag_Flux(i-1)-((1/n)*voltage(i)*(time(i)-time(i-1)));
end

%%
figure
plot(time,Mag_Flux);
xlabel('Time');
ylabel('Magnetic Flux (in Webers)');
%legend ('Flux','Voltage');

B_Field=Mag_Flux/Area;

type B-H_curve.dat.txt;
BH_data=readmatrix('B-H_curve.dat.txt');
H_given=BH_data(:,1);
B_given=BH_data(:,2);
H_obtained=interp1(B_given,H_given,B_Field);
Current=(H_obtained)/(n/Length);

%% 
figure
plot(time,Current);
xlabel('Time');
ylabel('Current in (A)');
legend ('Current');
