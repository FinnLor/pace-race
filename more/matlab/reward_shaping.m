g = @(n,x) 200*x.^3 .* (exp(-0.001*n+4)+2.5);
customGreen = [0.4660 0.6740 0.1880];

subplot(3,2,[1 3 5])
p = fsurf(g,[0,2000,0,1]);
% get(p); set(p,'linestyle','none'); % remove edges
get(p); set(p,'edgecolor',[0.5 0.5 0.5]);
map = repmat((0.3:0.001:1)',1,3); % custom colormap
colormap('white');
ax1 = gca; hold on;
% title('Reward function surface: $200\cdot x^3\cdot (e^{-0.001\cdot n+4}+2.5)$', Interpreter='latex');
xlabel('Step','Interpreter','latex');
ylabel('Relative path length','Interpreter','latex');
zlabel('Reward','Interpreter','latex');

% Calculate short parabolic trajectory
t1 = @(x) 1./600^2*x.^2;
x1 = 1:600;
y1 = t1(x1);
z1 = g(x1,y1) + 1;
plot3(ax1,x1,y1,z1,'r', 'LineWidth',4);
text(300,0.85,5600,'A','FontSize',18,'FontWeight','bold');

% Calculate long linear trajectory
x2 = 1:2000;
y2 = linspace(0,1,2000);
z2 = g(x2,y2) +1;
plot3(ax1,x2,y2,z2,'Color',customGreen, 'LineWidth',4);
text(1500,0.9,2300,'B','FontSize',18,'FontWeight','bold')

% Calculate negative parabolic trajectory
t3 = @(x) 2000/(0.3^2)*x.^2;
y3 = linspace(0,0.3,600);
x3 = t3(y3);
z3 = g(x3,y3) + 1;
plot3(ax1,x3,y3,z3,'b', 'LineWidth',4);
text(1700,0.35,300,'C','FontSize',18,'FontWeight','bold')

gradients1 = myGrad(g,600,x1,y1);
subplot(3,2,2)
plot(gradients1,'r','LineWidth',2);
grid on;
ax3 = gca; hold on;
title(strcat('Rewards per step for trajectory A, Cumulative reward: ',string(round(sum(gradients1),1))));
xlabel('Step','Interpreter','latex');
ylabel('Reward','Interpreter','latex');

gradients2 = myGrad(g,2000,x2,y2);
subplot(3,2,4)
plot(gradients2,'Color',customGreen,'LineWidth',2,'DisplayName','B');
grid on;
ax2 = gca; hold on;
title("test")
title(strcat('Rewards per step for trajectory B, Cumulative reward: ',string(round(sum(gradients2),1))))
xlabel('Step','Interpreter','latex');
ylabel('Reward','Interpreter','latex');

gradients3 = myGrad(g,600,x3,y3);
subplot(3,2,6)
plot(gradients3,'b','LineWidth',2);
grid on;
ax3 = gca; hold on;
title(strcat('Rewards per step for trajectory C, Cumulative reward: ',string(round(sum(gradients3),1))));
xlabel('Step','Interpreter','latex');
ylabel('Reward','Interpreter','latex');

function gradients = myGrad(fun,nMax,x,y)
    gradients = zeros(1,nMax);
    init = fun(x(1),y(1));
    for i = 1:length(x)
        diff = fun(x(i),y(i)) - init;
        init = fun(x(i),y(i));
        gradients(i) = diff;
    end
end
