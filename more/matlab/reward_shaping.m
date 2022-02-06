g = @(n,x) 200*x.^3 .* (exp(-0.001*n+4)+2.5);

subplot(3,2,[1 3 5])
fsurf(g,[0,2000,0,1])
ax1 = gca; hold on;
title('Reward function surface: $200\cdot x^3\cdot (e^{-0.001\cdot n+4}+2.5)$', Interpreter='latex')
xlabel('Path length');
ylabel('Steps');
zlabel('Reward');

% Calculate short parabolic trajectory
t1 = @(x) 1./600^2*x.^2;
x1 = 1:600;
y1 = t1(x1);
z1 = g(x1,y1) + 1;
plot3(ax1,x1,y1,z1,'r', 'LineWidth',4)

% Calculate long linear trajectory
x2 = 1:2000;
y2 = linspace(0,1,2000);
z2 = g(x2,y2) +1;
plot3(ax1,x2,y2,z2,'g', 'LineWidth',4)

% Calculate negative parabolic trajectory
t3 = @(x) 2000/(0.3^2)*x.^2;
y3 = linspace(0,0.3,600);
x3 = t3(y3);
z3 = g(x3,y3) + 1;
plot3(ax1,x3,y3,z3,'c', 'LineWidth',4)

gradients1 = myGrad(g,2000,x2,y2);
sum(gradients1);
subplot(3,2,2)
plot(gradients1,'g','LineWidth',2)
ax2 = gca; hold on;
title("test")
title(strcat('Rewards per step if n=2000, Cumulative reward: ',string(sum(gradients1))))
xlabel('Steps');
ylabel('Reward');

gradients2 = myGrad(g,600,x1,y1);
sum(gradients2);
subplot(3,2,4)
plot(gradients2,'r','LineWidth',2)
ax3 = gca; hold on;
title(strcat('Rewards per step if n=600, Cumulative reward: ',string(sum(gradients2))));
xlabel('Steps');
ylabel('Reward');

gradients3 = myGrad(g,600,x3,y3);
sum(gradients3);
subplot(3,2,6)
plot(gradients3,'c','LineWidth',2)
ax3 = gca; hold on;
title(strcat('Rewards per step if n=600, Cumulative reward: ',string(sum(gradients3))));
xlabel('Steps');
ylabel('Reward');

function gradients = myGrad(fun,nMax,x,y)
    gradients = zeros(1,nMax);
    init = fun(x(1),y(1));
    for i = 1:length(x)
        diff = fun(x(i),y(i)) - init;
        init = fun(x(i),y(i));
        gradients(i) = diff;
    end
end
