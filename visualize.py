import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from datetime import datetime
from scipy.signal import savgol_filter

with open('metadata.p','rb') as file: galleries = pickle.load(file)

ids = np.array([ int(metadata['gid']) for metadata in galleries.values() ])
times = np.array([ int(metadata['posted']) for metadata in galleries.values() ])
ratings = np.array([ float(metadata['rating']) for metadata in galleries.values() ])
dates = [ datetime.fromtimestamp(time).date() for time in times ]

if False:
    sources = {'patreon':[],'pixiv':[],'fanbox':[],'other':[]}
    
    dates = set()
    
    for metadata in galleries.values():
        dates.add( (datetime.fromtimestamp(int(metadata['posted'])).date()) )
    
    daterates = {}
    for source in sources:
        daterates[source] = {}
        for date in dates: daterates[source][date] = 0
    

    for metadata in galleries.values():
        title = metadata['title'].lower()
        date = datetime.fromtimestamp(int(metadata['posted'])).date()
        for site in ('patreon','pixiv','fanbox'):
            if site in title:
                daterates[site][date] += 1
                break
        else:
            daterates['other'][date] += 1
    
    fig, ax = plt.subplots()
    
    dates = list(dates)
    
    ax.bar(dates,np.array(list(daterates['patreon'].values())),color='g')
    ax.bar(dates, np.array(list(daterates['fanbox'].values())), bottom=np.array(list(daterates['patreon'].values())) ,color='r')
    ax.bar(dates, np.array(list(daterates['pixiv'].values())), bottom=np.array(list(daterates['fanbox'].values()))+np.array(list(daterates['patreon'].values())) ,color='b')
    ax.bar(dates, np.array(list(daterates['other'].values())), bottom=np.array(list(daterates['pixiv'].values()))+np.array(list(daterates['fanbox'].values()))+np.array(list(daterates['patreon'].values())) ,color='k')
    
    patches = []
    patches.append(patch.Patch(color='blue',label = f'Pixiv ({ np.array(list(daterates["pixiv"].values())).sum()})'))
    patches.append(patch.Patch(color='red',label = f'Fanbox ({np.array(list(daterates["fanbox"].values())).sum()})'))
    patches.append(patch.Patch(color='green',label = f'Patreon ({np.array(list(daterates["patreon"].values())).sum()})'))
    patches.append(patch.Patch(color='black',label = f'Other ({np.array(list(daterates["other"].values())).sum()})'))
    
    plt.legend(handles=patches,fontsize="9")
    ax.set_ylabel('Posts per Day', color='k')
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    plt.title("Source of Posts Tagged [AI Generated] per Day (as of 2023-04-16)")
    plt.show()

if False:
    tagratings = {'global':[]}
    taguploaders = {'global':set()}
    for metadata in galleries.values():
        tags = metadata['tags']
        rating = float(metadata['rating'])
        uploader = metadata['uploader']
        for tag in tags:
            if tag in tagratings:   
                tagratings[tag].append(rating)
                taguploaders[tag].add( (uploader) )
            else:
                tagratings[tag] = [rating]
                taguploaders[tag] = {uploader}
        tagratings['global'].append(rating)
        taguploaders['global'].add( (uploader) )
    
    avg = np.mean(tagratings['global'])
    for tag in tagratings: tagratings[tag].extend([avg,avg,avg,avg,avg,avg,avg,avg,avg,avg])
    
    #for tag in tagratings: print(len(tagratings[tag])-1,tag,np.mean(tagratings[tag]))
    
    sortedtags = [ [round(np.mean(tagratings[tag])-avg,2),len(tagratings[tag])-10,len(taguploaders[tag]),tag] for tag in tagratings ]
    sortedtags.sort()
    for tag in sortedtags:
        if tag[2]>3 and tag[1]>5: print(f'{tag[0]},{tag[1]},{tag[2]},{tag[3]}')
    
    print('Global Average',avg)

if False:
    daterate = {}

    for date in dates:
        if date in daterate: daterate[date] += 1
        else: daterate[date] = 1
    
    fig, ax = plt.subplots()
    ax.bar(daterate.keys(),daterate.values(),color='k')
    ax.set_ylabel('Posts per Day', color='k')
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    plt.title("Number of Posts Tagged [AI Generated] per Day (as of 2023-04-16)")
    plt.show()

if False:
    
    uploaders = {}

    topuploaders = ['KEYLUN','Blue-Shark','Drizz46MaleWV','Willh','ppkkmoon','Unclebilly8051','Pokom','abzd623','siacofilla','RaDeRo','firecat666','boyis cg','oktaoshi','Doomstate','(Disowned)']
    '''[103, 'KEYLUN'], [78, '(Disowned)'], [71, 'Blue-Shark'], [66, 'Drizz46MaleWV'], [36, 'Willh'], [30, 'ppkkmoon'], [27, 'Unclebilly8051'], [22, 'Pokom'], [19, 'abzd623'], [18, 'siacofilla'], [15, 'RaDeRo'], [13, 'firecat666'], [12, 'boyis cg'], [11, 'oktaoshi'], [11, 'Doomstate'], [10, 'tmot'], [10, 'Sirius9940K@'], [10, '10Step'],'''

    for uploader in topuploaders: uploaders[uploader] = [ [], [] ]

    for metadata in galleries.values():
        uploader = metadata['uploader']
        if not uploader in topuploaders: uploader = '(Other)'
        if not uploader in uploaders: uploaders[uploader] = [ [], [] ]
        uploaders[uploader][0].append( datetime.fromtimestamp(int(metadata['posted'])).date() )
        uploaders[uploader][1].append( float(metadata['rating']) )

    #uploadercount = [ [len(uploaders[uploader][0]),uploader] for uploader in uploaders ]
    #uploadercount.sort(reverse=True)

    for uploader in uploaders: print(uploader, len(uploaders[uploader][0]))
    
    fig, ax = plt.subplots()
    
    colors = [ 'lightgray','darkgray','mediumpurple','mediumseagreen','deeppink','chocolate','firebrick','skyblue','orchid','yellowgreen','orange','aquamarine','red','green','indigo','steelblue']
    i=0
    for uploader in reversed(uploaders):
        dates = uploaders[uploader][0]
        scores = uploaders[uploader][1]
        ax.scatter(dates,scores,s=4,c=colors[i])
        i+=1
    
    plt.title("Posts and Ratings of the Most Prolific [AI Generated] Uploaders (as of 2023-04-16)")
    
    patches = []
    i=0
    colors.reverse()
    for uploader in uploaders:
        scores = uploaders[uploader][1]
        patches.append(patch.Patch(color=colors[i],label = f'({ len(scores) }) [{ round(np.mean(scores),2) }] {uploader}'))
        i += 1
    ax.set_ylabel('Rating of each Post (Points)', color='k')
    plt.legend(handles=patches,fontsize="9")
    plt.show()

if True:
    
    topuploaders = ['KEYLUN','Blue-Shark','Drizz46MaleWV','Willh','ppkkmoon','Unclebilly8051','Pokom','abzd623','siacofilla','RaDeRo','firecat666','boyis cg','oktaoshi','Doomstate']
    
    ids = np.array([ int(metadata['gid']) for metadata in galleries.values() if metadata['uploader'] not in topuploaders])
    ratings = np.array([ float(metadata['rating']) for metadata in galleries.values() if metadata['uploader'] not in topuploaders])
    times = np.array([ int(metadata['posted']) for metadata in galleries.values() if metadata['uploader'] not in topuploaders])
    dates = [ datetime.fromtimestamp(time).date() for time in times ]
    
    print(len(ids))
    print(len(times))
    
    postrate = [1000000]

    for i in range(1,len(ids)):
        if i < 65:
            window = i
            startid = np.mean(ids[0:i])
        else:
            window = 50
            startid = ids[i-50]
        
        endid = ids[i]
        postrate.append((endid-startid)*(50/window))

    postrate[60:] = savgol_filter(postrate[60:],71,2)
    
    print(len(postrate))
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax2.plot(dates,100*50/np.array(postrate),linewidth=1.5,c='k')

    colormap = plt.get_cmap('brg')

    colors = colormap((np.array(ratings)/8)+0.3)

    ax1.scatter(dates,ratings,s=0.5,c=colors)
    release_date = datetime(2022,9,28)
    #ax1.plot([release_date,release_date],[0,5],c=(0.85,0.85,0.85),linewidth=1)
    #plt.bar(times,ratings)

    ax1.set_xlabel('Date of Posting')
    ax1.set_ylabel('Rating of each Post (Points)', color='g')
    ax2.set_ylabel('Percent of New Posts (Plot)', color='k')
    plt.title("Ratings and Percent of New Posts Tagged [AI Generated] excluding Top 14 Uploaders (as of 2023-04-16)")
    plt.show()

