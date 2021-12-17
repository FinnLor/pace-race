% 1
N = 1000;
s = linspace(0.5, 2*pi,N); % is the length of the path

x = s + 2*cos(2*s);
y = s + 3*sin(3*s);
figure(1);
subplot(2,2,1)
plot(x,y)

x = s + cos(s).*sin(s);
y = tan(0.2*s);
subplot(2,2,2)
plot(x,y)
hold on
x = x - 0.2;
y = tan(0.2*s) + 0.2;
plot(x,y)

x = cos(s);
y = sin(s);
subplot(2,2,3)
plot(x,y)


x = 1./s + 3*cos(s).*sin(s).^2;
y = tan(0.2*s);
subplot(2,2,4)
plot(x,y)
