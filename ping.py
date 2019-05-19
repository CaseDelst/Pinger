from    matplotlib.widgets    import     Slider, Button, RadioButtons
import  matplotlib.pyplot     as         plt 
import  matplotlib.animation  as         animation 
import  matplotlib.patches    as         mpatches
from    matplotlib            import     style 
from    pythonping            import     ping
from    datetime              import     datetime 
import  pandas                as         pd  
import  numpy                 as         np
import  os


plt.rcParams.update({'font.size': 12})
style.use('dark_background')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
df = pd.DataFrame(columns=['Time', 'Min', 'Avg', 'Max', 'Label?'])

#Number of pings available on graph at any given time
targetXTicks = 60
labelSeparator = 15
lineWeight = 2
yMax = 80
yMin = 0

#Initialize DF
for i in range(targetXTicks):
    LabelVal = True if ((targetXTicks - i) % labelSeparator == 0) else False
    df = df.append({'Time'   : "-00:00:" + (str(targetXTicks - i) if (targetXTicks - i) >= labelSeparator else ('0' + str(targetXTicks - i))), 
                    'Min'    : 0, 
                    'Avg'    : 0, 
                    'Max'    : 0, 
                    'Label?' : LabelVal},
                    ignore_index=True)

def animate(i):
    global df
    
    #Format is min/avg/max, first breaks lines picks 6th, then breaks words picks 6th, then splits format into 3 nums
    pingStats = str(ping('8.8.8.8')).split('\n')[5].split(' ')[5].split('/')

    #Format to floats
    for i in range(len(pingStats)):
        pingStats[i] = float(pingStats[i])

    #Add to already existing data frame
    currentTime = str(datetime.now()).split(' ')[1][0 : -7]
    secondsVal = int(currentTime[-2:])
    LabelVal = True if (secondsVal % labelSeparator == 0) else False

    dfAppend = df.append({'Time' : str(datetime.now()).split(' ')[1][0 : -7], 
                        'Min'    : pingStats[0], 
                        'Avg'    : pingStats[1], 
                        'Max'    : pingStats[2],
                        'Label?' : LabelVal},
                    ignore_index=True)

    
    while dfAppend.shape[0] > targetXTicks:
        dfAppend = dfAppend.drop([0])
   
    print(dfAppend)
    df = dfAppend
    print()

    

    xs = []
    ys = []

    ax1.clear()
    ax1.plot(df['Time'], df['Min'], label='Min', linewidth=lineWeight, color='green')
    ax1.plot(df['Time'], df['Avg'], label='Avg', linewidth=lineWeight, color='orange')
    ax1.plot(df['Time'], df['Max'], label='Max', linewidth=lineWeight, color='red')
    #Find average average ping
    averageSum = df.sum(axis=0, skipna=True)['Avg']
    averageAverage = averageSum / targetXTicks
    ax1.axhline(y=averageAverage, 
                color='orange', 
                lw=1, 
                ls='--', 
                zorder=0)

    #set ranges for values
    ax1.set_ylim([yMin, yMax])
    ax1.set_xlim(xmin=0.0, xmax=targetXTicks-1)
    
    #set lables
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Ping (in ms)')
    plt.title('Ping')

    minPatch = mpatches.Patch(color='green', label='Min')
    avgPatch = mpatches.Patch(color='orange', label='Avg')
    maxPatch = mpatches.Patch(color='red', label='Max')
    avgAvgPatch = mpatches.Patch(color='orange', label='Average Avg', linestyle='--', fill=False)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.035),
               ncol=3, fancybox=True, shadow=True, handles=[minPatch, avgPatch, maxPatch, avgAvgPatch])

    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
        if df.iloc[n]['Label?'] == False:
            label.set_visible(False)


ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.gcf().subplots_adjust(bottom=0.15, left=0.15, top=.9)
plt.xticks(rotation=45)
plt.show()


