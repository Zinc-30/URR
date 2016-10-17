% this figures draws the adjusted taxonomy, collecting answer from crowd.
% Changing Parameter: Budget, six lines- 0~1

lineWidth = 3;
markerSize=20;
labelTestSize = 40;
legendTextSize = 40;
boxRatioTextSize = 35;

greedy = [26,61,81,131,183];
dp = [30,78,115,158,216];
rand = [25,51,72,75,96];
% entity_one = [26,48,66,82,99];
% entity_total = [];
hFig = figure(1);
enlargeScale = 1.4;
set(hFig, 'Position', [0 0 560*enlargeScale 420*enlargeScale]);
hold on;
xSequenceC = {'0.2';'0.4';'0.6';'0.8';'1'};

xSequence = 1:length(xSequenceC);

a1 = plot(xSequence, greedy, 'o--r','LineWidth',lineWidth); M1 = 'Greedy';
a2 = plot(xSequence, dp, '^-.k','LineWidth',lineWidth); M2 = 'DP';
a3 = plot(xSequence,rand,'*--','LineWidth',lineWidth); M3 = 'Rand';
% a3 = plot(xSequence, theta_7, 'd--c','LineWidth',lineWidth); M3 = '\theta = 0.7';
% a4 = plot(xSequence, theta_8, '+--b','LineWidth',lineWidth); M4 = '\theta = 0.8';
% a5 = plot(xSequence, theta_9, 'v-.m','LineWidth',lineWidth); M5 = '\theta = 0.9';
% a10 = plot(xSequence,weight_10, 'square:g','LineWidth',lineWidth); M6 = '\lambda = 1';
%h_legend = legend(M1, M2, M3, M4,  2);
h_legend = legend(M1,M2,M3,2);
xhand = xlabel(['Budget (', char(8240),')']);
yhand = ylabel('Utility');
% set(a1, 'MarkerSize', markerSize);
% set(a2, 'MarkerSize', markerSize);
% set(a3, 'MarkerSize', markerSize);
% set(a4, 'MarkerSize', markerSize);
set([a1,a2,a3],'MarkerSize',markerSize);
set(h_legend,'FontSize',legendTextSize);
%set(h_legend, 'FontWeight', 'bold'); 
set(gca,'fontsize',boxRatioTextSize);
set(xhand, 'FontSize', labelTestSize);
set(yhand, 'FontSize', labelTestSize);
set(gca,'XTick',xSequence); % Change x-axis ticks
set(gca,'XTickLabel',xSequenceC); % Change x-axis ticks labels to desired values.
hold off;