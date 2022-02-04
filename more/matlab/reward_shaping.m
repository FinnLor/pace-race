g = @(x,n) 200*x.^3 .* (exp(-0.001*n+4)+2.5);

subplot(3,2,[1 3])
fsurf(g,[0,1,0,2000])
title('Reward function surface: $200\cdot x^3\cdot (e^{-0.001\cdot n+4}+2.5)$', Interpreter='latex')
xlabel('Path length');
ylabel('Steps');
zlabel('Reward');


gradients1 = [];
n_max = 2000;
init = g(0,0);
for n = 1:n_max
    diff = g(n/n_max,n) - init;
    init = g(n/n_max,n);
    gradients1(n) = diff;
end
sum(gradients1)
subplot(3,2,2)
plot(gradients1)
title("test")
title(strcat('Rewards per step if n=2000, Cumulative reward: ',string(sum(gradients1))))
xlabel('Steps');
ylabel('Reward');

gradients2 = [];
init = g(0,0);
n_max = 800;
for n = 1:n_max
    diff = g(n/n_max,n) - init;
    init = g(n/n_max,n);
    gradients2(n) = diff;
end
sum(gradients2)
subplot(3,2,4)
plot(gradients2)
title(strcat('Rewards per step if n=800, Cumulative reward: ',string(sum(gradients2))))
xlabel('Steps');
ylabel('Reward');

subplot(3,2,[5,6])
p = fcontour(g,[0,1,0,2000]);
p.Fill = 'on';
p.LevelList = 50:50:11000;