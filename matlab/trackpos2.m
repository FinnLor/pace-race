% trackpos2
%
% USE:
% find the orthogonalized track-position of C

% preferences
clc;
clear all;
disp(['start trackpos2']);
show = false;


figure(1)
for n = 1:5
    % Definitionen
    N = 500;
    s = linspace(0.5, 2*pi, N);
    y = 1./s + rand*3.*cos(s).*sin(s).^2;
    x = (-1)^(randi([1,2])) * (s + 3*rand*tan(0.2*s));
    br = 1;
    %br = 0.5 + 1./s + rand*2.*cos(0.5*s).*sin(s).^2;
    %br = br(1:N-1)';
    %br = rand([N-1,1]);

    %N = 5000;
    %s = linspace(0, 5*pi, N);
    %x = s + 0.1*randn*cos(1*randn*s) - 0.1*randn*sin(1*randn*s) + 0.15*randn*cos(1*randn*s) - 0.15*randn*sin(1*randn*s) + 0.2*randn*cos(1*randn*s) - 0.2*randn*sin(1*randn*s) + 0.27*randn*cos(1*randn*s) - 0.27*randn*sin(1*randn*s);
    %y = s + sin(0.1*rand*s) - cos(0.1*rand*s) + sin(0.5*rand*s) - cos(0.5*rand*s) + sin(1*rand*s) - cos(1*rand*s) + 0.2*sin(2*rand*s) - 0.2*cos(2*rand*s);
     
 



    % Drehung
    for k = 1:length(x)-1
        bxa(k) = ((x(k+1)-x(k))*cos(pi/2)) - ((y(k+1)-y(k))*sin(pi/2));
        bya(k) = ((x(k+1)-x(k))*sin(pi/2)) + ((y(k+1)-y(k))*cos(pi/2));
    end
    x(1) = [];
    y(1) = [];
    mt = [x; y]';       % mean track
    b = [bxa; bya]';    % border
    fb = 10;            % halbe Straßenbreite (aktuell konstant)
    % Normierung der border-Vektoren
    for k = 1:length(b)
        bn(k,:) =import b(k,:)/(fb*vecnorm(b(k,:)));
    end

    % Vektoraddition als linken u rechten Rand
    bl = mt + (bn.*br);
    br = mt - (bn.*br);

    %subplot(5,1,n)
    plot(mt(:,1),mt(:,2),bl(:,1),bl(:,2),br(:,1),br(:,2));
end

% Darstellung
%figure(1);
%subplot(1,2,1)
%plot(mt(:,1),mt(:,2),bl(:,1),bl(:,2),br(:,1),br(:,2));
%subplot(1,2,2)
%plot(mt(:,1),mt(:,2),bl(:,1),bl(:,2),'.',br(:,1),br(:,2),'.');



disp(['end trackpos2']);


