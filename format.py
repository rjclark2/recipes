import pandas as pd
import os
import numpy as np

df = []

#### FN ####
names = {'title':'Recipe Name','description':'Description','ingredients':'Ingredients'
        ,'url':'Original Recipe Website','author':'Author','instructions':'Instructions'
        ,'ttime':'Total Time','ptime':'Preperation Time'
        ,'ctime':'Cooking Time','servings':'Number of Servings'
        ,'calories':'Calories per Serving','fat':'Fat per Serving'
        ,'carbs':'Carbohydrates per Serving'
        ,'protein':'Protein per Serving','cholesterol':'Cholesterol per Serving'
        ,'sodium':'Sodium per Serving','nreviews':'Number of Ratings','reviews':'Average Rating',
        'published':'Publish Date'}
del df
epi = os.listdir('json')
epi = [x for x in epi if 'fn' in x and 'all' not in x]
for i,filn in enumerate(epi):
    if i ==0:
        df = pd.read_json('json/'+filn)
    else:
        df = df.append(pd.read_json('json/'+filn),ignore_index = True)

df=df.rename(names,axis=1)
df.to_json('json/fnall.json',orient='records')

df = pd.read_json('json/fnall.json')
df = df[['Recipe Name','Description','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']]
nulls = ['Recipe Name','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']
for i in nulls:
    df = df[df[i].isnull() == False]
df['Recipe Name'] = df['Recipe Name'].apply(lambda x: x[0])
def to_datetime(x):
    try:
        x  = np.datetime64(x)
        x = (np.datetime64('today')-x)/(np.timedelta64(1,'D'))
        x = int(x)
        return x
    except:
        return None
def to_timedelta(x):
    try:
        x = x.split()
        x[-1] = int(x[-1])
        x = [str(i) for i in x]
        x = pd.Timedelta(' '.join(x) + ' minutes')
        return x/pd.Timedelta('1 minute')
    except:
        try:
            x = pd.Timedelta(' '.join(x))
            return x/pd.Timedelta('1 minute')
        except:
            return None
df['Publish Date'] = df['Publish Date'].apply(lambda x: min(x))
df['Publish Date'] = df['Publish Date'].apply(to_datetime)
#df['Original Recipe Website'] = df['Original Recipe Website'].apply(lambda x: 'The Food Network')
df = df[df['Publish Date'].isnull() == False]
df['Publish Date'] = df['Publish Date'].astype('int')
#df['Total Time'] = df['Total Time'].str.replace('hrs','hours').str.replace('hr','hour').str.replace('mins','minutes').str.replace('min','minutes')
#df['Total Time'] = df[~df['Total Time'].str.contains('week')]['Total Time']
#df['Total Time'] = df['Total Time'].apply(pd.to_timedelta)
#df = df[df['Total Time'].isnull() == False]
df['Description'] = df['Description'].fillna('')
df.to_json('static/fnall.json',orient='records')


##### AR ######

names = {'title':'Recipe Name','description':'Description','ingredients':'Ingredients'
        ,'url':'Original Recipe Website','author':'Author','instructions':'Instructions'
        ,'ttime':'Total Time','ptime':'Preperation Time'
        ,'ctime':'Cooking Time','servings':'Number of Servings'
        ,'calories':'Calories per Serving','fat':'Fat per Serving'
        ,'carbs':'Carbohydrates per Serving'
        ,'protein':'Protein per Serving','cholesterol':'Cholesterol per Serving'
        ,'sodium':'Sodium per Serving','nreviews':'Number of Ratings','reviews':'Average Rating',
        'pubished':'Publish Date'}
del df
epi = os.listdir('json')
epi = [x for x in epi if 'ar' in x and 'all' not in x]
for i,filn in enumerate(epi):
    if i ==0:
        df = pd.read_json('json/'+filn)
    else:
        df = df.append(pd.read_json('json/'+filn),ignore_index = True)

df=df.rename(names,axis=1)
df.to_json('json/arall.json',orient='records')
df = pd.read_json('json/arall.json')
df = df[['Recipe Name','Description','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']]
nulls = ['Recipe Name','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']
for i in nulls:
    df = df[df[i].isnull() == False]

def to_datetime(x):
    try:
        x  = np.datetime64(x)
        x = (np.datetime64('today')-x)/(np.timedelta64(1,'D'))
        x = int(x)
        return x
    except:
        return None
def to_timedelta(x):
    try:
        x = x.split()
        x[-1] = int(x[-1])
        x = [str(i) for i in x]
        x = pd.Timedelta(' '.join(x) + ' minutes')
        return x/pd.Timedelta('1 minute')
    except:
        try:
            x = pd.Timedelta(' '.join(x))
            return x/pd.Timedelta('1 minute')
        except:
            return None
df['Publish Date'] = df['Publish Date'].apply(lambda x: min(x))
df['Publish Date'] = df['Publish Date'].apply(to_datetime)
#df['Original Recipe Website'] = df['Original Recipe Website'].apply(lambda x: 'allrecipes')
df = df[df['Publish Date'].isnull() == False]
df['Publish Date'] = df['Publish Date'].astype('int')
#df['Total Time'] = df['Total Time'].str.replace('hrs','hours').str.replace('hr','hour').str.replace('mins','minutes').str.replace('min','minutes').str.replace('minutesutes','')
#df['Total Time'] = df[~df['Total Time'].str.contains('week')]['Total Time']
#df['Total Time'] = df['Total Time'].apply(to_timedelta)
#df = df[df['Total Time'].isnull() == False]
df['Description'] = df['Description'].fillna('')
df.to_json('static/arall.json',orient='records')


### EPI ###3

names = {'title':'Recipe Name','description':'Description','ingredients':'Ingredients'
        ,'url':'Original Recipe Website','author':'Author','instructions':'Instructions'
        ,'ttime':'Total Time','ptime':'Preperation Time'
        ,'ctime':'Cooking Time','servings':'Number of Servings'
        ,'calories':'Calories per Serving','fat':'Fat per Serving'
        ,'carbs':'Carbohydrates per Serving'
        ,'protein':'Protein per Serving','cholesterol':'Cholesterol per Serving'
        ,'sodium':'Sodium per Serving','nreviews':'Number of Ratings','reviews':'Average Rating',
        'published':'Publish Date'}

del df
epi = os.listdir('json')
epi = [x for x in epi if 'epi' in x and 'all' not in x]
for i,filn in enumerate(epi):
    if i ==0:
        df = pd.read_json('json/'+filn)
    else:
        df = df.append(pd.read_json('json/'+filn),ignore_index = True)

df=df.rename(names,axis=1)
df.to_json('json/epiall.json',orient='records')
df = pd.read_json('json/epiall.json')
df = df[['Recipe Name','Description','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']]
nulls = ['Recipe Name','Ingredients','Original Recipe Website','Instructions','Number of Ratings','Publish Date']
for i in nulls:
    df = df[df[i].isnull() == False]

def to_datetime(x):
    try:
        x  = np.datetime64(x)
        x = (np.datetime64('today')-x)/(np.timedelta64(1,'D'))
        x = int(x)
        return x
    except:
        return None
def to_timedelta(x):
    try:
        x = x.split()
        x[-1] = int(x[-1])
        x = [str(i) for i in x]
        x = pd.Timedelta(' '.join(x) + ' minutes')
        return x/pd.Timedelta('1 minute')
    except:
        try:
            x = pd.Timedelta(' '.join(x))
            return x/pd.Timedelta('1 minute')
        except:
            return None
df['Publish Date'] = df['Publish Date'].apply(to_datetime)
df = df[df['Publish Date'].isnull() == False]
df['Publish Date'] = df['Publish Date'].astype('int')
#df['Total Time'] = df['Total Time'].str.replace('hrs','hours').str.replace('hr','hour').str.replace('mins','minutes').str.replace('min','minutes').str.replace('minutesutes','')
#df['Total Time'] = df[~df['Total Time'].str.contains('week')]['Total Time']
#df['Total Time'] = df['Total Time'].apply(to_timedelta)
#df['Total Time'] = df['Total Time'].apply(lambda x: 0)
#df = df[df['Total Time'].isnull() == False]
#df['Original Recipe Website'] = df['Original Recipe Website'].apply(lambda x: 'Epicurious')
df['Description'] = df['Description'].fillna('')
df.to_json('static/epiall.json',orient='records')

