import os
import sys
from bs4 import BeautifulSoup
from scraper import gethtml
import re
import pandas as pd
import numpy as np
import requests

class tag(object):
    def __init__(self,tag,adict):
        self.tag = tag
        self.method = adict.get('method')
        self.pattern = adict.get('pattern')
        self.ajoin = adict.get('join')
        self.omit = adict.get('omit')
        if adict.get('method') != None:
            adict.pop('method')
        if adict.get('pattern') != None:
            adict.pop('pattern')
        if adict.get('join') != None:
            adict.pop('join')
        if adict.get('omit') != None:
            adict.pop('omit')
        self.kargs = adict
        
    def get_text(self,soup):
        areturn = None
        if self.method == None:
            text = soup.find_all(self.tag,self.kargs)
            areturn = [x.text.strip() for x in text]
        elif self.method == 'unpack':
            search = soup.find(self.tag,self.kargs)
            while True:
                try:
                    search = search.findNext()
                except:
                    return None
                else:
                    try:
                        if self.pattern == search.text.strip():
                            break
                    except:
                        None       
            areturn = search.findNext().text.strip()
        elif self.method == 'search':
            search = soup.find(self.tag,self.kargs)
            if search != None:
                areturn = re.findall(self.pattern,search.text)
                areturn = [x.strip() for x in areturn]
                if areturn == []:
                    areturn = re.findall(self.pattern,str(search))
                    areturn = [x.strip() for x in areturn]
        elif self.method == 'children':
            search = soup.find(self.tag,self.kargs)
            if search:
                search = search.find_all(self.pattern)
                areturn = [x.text.strip() for x in search]
        
        elif self.method == 'None':
            return None
        elif self.method == 'static':
            return self.pattern
        
        else:
            text = soup.find_all(self.tag,self.kargs)
            areturn = [x.get(self.method).strip() for x in text]
            
        if self.omit != None and areturn:
            areturn = areturn[self.omit:]
        if self.ajoin != None and areturn:
            if len(areturn) > 1:
                areturn = [(self.ajoin).join(x) for x in zip(areturn[0::2],areturn[1::2])]
        if areturn == []:
            areturn = None
        if type(areturn) == list and len(areturn) == 1:
            areturn = areturn[0]
        return areturn
    
class recipe(object):
    def __init__(self,name,url):
        self.name = name
        self.soup = BeautifulSoup(gethtml(name,url.replace(urldict[name],'')),'lxml',from_encoding='UTF-8')
        self.url = url
        for k,v in tag_dict[self.name].items():
            setattr(self,k,v)
        if all(x == [] for x in self.get_texts().values()):
            self.name = name+'2'
            for k,v in tag_dict.get(self.name).items():
                setattr(self,k,v)
        self.features = self.get_texts()
    
    def get_texts(self):
        textt = {}
        for feature,atag in tag_dict[self.name].items():
            textt[feature] = atag.get_text(self.soup)
        return(textt)

#### IMPORTANT TAGS FOR EACH HTML STRUCTURE ###

tag_dict = {'ar2':
            {'title':tag('h1',{'class':'recipe-summary__h1'})
             ,'description':tag('div',{'class':'submitter__description'})
             ,'ingredients':tag('span',{'class':'recipe-ingred_txt added'})
             ,'url':tag('link',{'id':'canonicalUrl','method':'href'})
             ,'author':tag('span',{'class':'submitter__name'})
             ,'instructions':tag('span',{'class':'recipe-directions__list--item'})
             ,'ttime':tag('time',{'itemprop':'totalTime'})
             ,'ptime':tag('time',{'itemprop':'prepTime'})
             ,'ctime':tag('time',{'itemprop':'cookTime'})
             ,'servings':tag('div',{'class':'subtext'})
             ,'calories':tag('span',{'itemprop':'calories'})
             ,'fat':tag('span',{'itemprop':'fatContent'})
             ,'carbs':tag('span',{'itemprop':'carbohydrateContent'})
             ,'protein':tag('span',{'itemprop':'proteinContent'})
             ,'cholesterol':tag('span',{'itemprop':'cholesterolContent'})
             ,'sodium':tag('span',{'itemprop':'sodiumContent'})
             ,'reviews':tag('div',{'class':'reviewsummary--bar','method':'aria-label'})
             ,'pubished':tag('script',{'type':'application/ld+json','method':'search','pattern':'"datePublished": "([^"]*)'})
            }
             ,'ar':
             {'title':tag('h1',{'class':'headline heading-content'})
             ,'description':tag('p',{'class':'margin-0-auto'})
             ,'ingredients':tag('span',{'class':'ingredients-item-name'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('a',{'class':'author-name link'})
             ,'instructions':tag('div',{'class':'paragraph'})
             ,'ttime':tag('div',{'class':'two-subcol-content-wrapper','method':'unpack','pattern':'total:'})
              ,'ptime':tag('div',{'class':'two-subcol-content-wrapper','method':'unpack','pattern':'prep:'})
              ,'ctime':tag('div',{'class':'two-subcol-content-wrapper','method':'unpack','pattern':'cook:'})
              ,'servings':tag('div',{'class':'two-subcol-content-wrapper','method':'unpack','pattern':'Servings:'})
             ,'calories':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'([0-9.]+) *calories'})
             ,'fat':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'fat *([^g]*g)'})
             ,'carbs':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'carbohydrates *([^g]*g)'})
             ,'protein':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'protein *([^g]*g)'})
             ,'cholesterol':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'cholesterol *([^m]*mg)'})
             ,'sodium':tag('div',{'class':'partial recipe-nutrition-section','method':'search','pattern':'sodium * ([^m]*mg)'})
             ,'nreviews':tag('span',{'class':'ratings-count','omit':1})
             ,'reviews':tag('span',{'class':'rating-count','omit':5})
             ,'pubished':tag('script',{'type':'application/ld+json','method':'search','pattern':'"datePublished": "([^"]*)'})
            }
            ,'ny':
            {'title':tag('h1',{'class':'recipe-title title name'})
             ,'description':tag('div',{'class':'topnote'})
             ,'ingredients':tag('span',{'class':'ingredient-name'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('div',{'class':'nytc---recipebyline---bylinePart'})
             ,'instructions':tag('ol',{'class':'recipe-steps','method':'children','pattern':'li'})
             ,'ttime':tag('ul',{'class':'recipe-time-yield','method':'unpack','pattern':'Time'})
             ,'ptime':tag('None',{'method':'None'})
             ,'ctime':tag('None',{'method':'None'})
             ,'servings':tag('ul',{'class':'recipe-time-yield','method':'unpack','pattern':'Yield'})
             ,'calories':tag('None',{'method':'None'})
             ,'fat':tag('None',{'method':'None'})
             ,'carbs':tag('None',{'method':'None'})
             ,'protein':tag('None',{'method':'None'})
             ,'cholesterol':tag('None',{'method':'None'})
             ,'sodium':tag('None',{'method':'None'})
             ,'nreviews':tag('script',{'type':'application/ld+json','method':'search','pattern':'"ratingCount":([0-9]*)'})
             ,'reviews':tag('script',{'type':'application/ld+json','method':'search','pattern':'"ratingValue":([0-9]*)'})
             ,'published':tag('meta',{'property':'og:image','method':'content'})
            }
            ,'bon':
            { 'title':tag('h1',{'class':'split-screen-content-header__hed'})
              ,'description':tag('div',{'class':'container--body-inner'})
             ,'ingredients':tag('div',{'data-testid':'IngredientList','method':'children','pattern':['p','div'],'omit':2,'join':' '})
             ,'url':tag('meta',{'property':"og:url",'method':'content'})
             ,'author':tag('span',{'itemprop':'name'})
             ,'instructions':tag('div',{'data-testid':'InstructionsWrapper','method':'children','pattern':['h3','p'],'join':': '})
              ,'ttime':tag('div',{'class':'content-background','method':'search','pattern':'Total Time([0-9 a-z]*)'})
             ,'ptime':tag('div',{'class':'content-background','method':'search','pattern':'Prep Time([0-9 a-z]*)'})
             ,'ctime':tag('div',{'class':'content-background','method':'search','pattern':'Cook Time([0-9 a-z]*)'})
             ,'servings':tag('div',{'data-testid':'IngredientList','method':'search','pattern':'Ingredients([0-9 –]*) [Ss]ervings'})
             ,'calories':tag('None',{'method':'None'})
             ,'fat':tag('None',{'method':'None'})
             ,'carbs':tag('None',{'method':'None'})
             ,'protein':tag('None',{'method':'None'})
             ,'cholesterol':tag('None',{'method':'None'})
             ,'sodium':tag('None',{'method':'None'})
             ,'reviews':tag('div',{'id':'reviews','method':'search','pattern':'Reviews .?([0-9]+).?'})
            }
            ,'fn':
            {'title':tag('span',{'class':'o-AssetTitle__a-HeadlineText'})
             ,'description':tag('div',{'class':'o-AssetDescription__a-Description'})
             ,'ingredients':tag('span',{'class':'o-Ingredients__a-Ingredient--CheckboxLabel','omit':1})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('div',{'class':'o-Attribution__m-Author'})
             ,'instructions':tag('li',{'class':'o-Method__m-Step'})
             ,'ttime':tag('span',{'method':'unpack','pattern':'Total:'})
             ,'ptime':tag('span',{'method':'unpack','pattern':'Active:'})
             ,'ctime':tag('time',{'itemprop':'cookTime'})
             ,'servings':tag('span',{'class':'o-RecipeInfo__a-Description','method':'unpack','pattern':'Yield:'})
             ,'calories':tag('span',{'itemprop':'calories','method':'unpack','pattern':'Yield:'})
             ,'fat':tag('span',{'itemprop':'fatContent'})
             ,'carbs':tag('span',{'itemprop':'carbohydrateContent'})
             ,'protein':tag('span',{'itemprop':'proteinContent'})
             ,'cholesterol':tag('span',{'itemprop':'cholesterolContent'})
             ,'sodium':tag('span',{'itemprop':'sodiumContent'})
             ,'nreviews':tag('script',{'type':'application/ld+json','method':'search','pattern':'"reviewCount":([0-9]*)'})
             ,'reviews':tag('script',{'type':'application/ld+json','method':'search','pattern':'AggregateRating","ratingValue":([0-9]*)'})
             ,'published':tag('script',{'type':'application/ld+json','method':'search','pattern':'"datePublished":"([^"]*)'})

            }
            ,'poy':
            {'title':tag('h2',{'class':'tasty-recipes-title'})
             ,'description':tag('div',{'class':'tasty-recipes-description-body'})
             ,'ingredients':tag('div',{'class':'tasty-recipes-ingredients','method':'children','pattern':'li'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('None',{'method':'static','pattern':'Lindsay Ostrom'})
             ,'instructions':tag('div',{'class':'tasty-recipes-instructions','method':'children','pattern':'li'})
             ,'ttime':tag('None',{'method':'None'})
             ,'ptime':tag('span',{'class':'tasty-recipes-prep-time'})
             ,'ctime':tag('span',{'class':'tasty-recipes-cook-time'})
             ,'servings':tag('span',{'class':'tasty-recipes-yield','method':'search','pattern':'^[0-9]*'})
             ,'calories':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'calories":"([^"]*)'})
             ,'fat':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'fatContent":"([^"]*)'})
             ,'carbs':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'carbohydrateContent":"([^"]*)'})
             ,'protein':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'proteinContent":"([^"]*)'})
             ,'cholesterol':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'cholesterolContent":"([^"]*)'})
             ,'sodium':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'sodiumContent":"([^"]*)'})
             ,'nreviews':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'reviewCount":"([^"]*)'}) #get these
             ,'reviews':tag('script',{'class':'yoast-schema-graph','method':'search','pattern':'[0-9]","ratingValue":"([^"]*)'})
            }
             ,'yum':
            {'title':tag('div',{'class':'primary-info-left-wrapper','method':'children','pattern':'h1'})
             ,'description':tag('div',{'class':'wrapper recipe-description'})
             ,'ingredients':tag('div',{'class':'shopping-list-ingredients','method':'children','pattern':'li'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('None',{'method':'None'})
             ,'instructions':tag('div',{'class':'wrapper directions-wrapper','method':'children','pattern':'a'})
             ,'ttime':tag('div',{'class':'recipe-summary-item unit h2-text','method':'children','pattern':'span','join':' '})
             ,'ptime':tag('None',{'method':'None'})
             ,'ctime':tag('None',{'method':'None'})
             ,'servings':tag('div',{'class':'unit-serving-wrapper','method':'search','pattern':'([0-9]*) *[Ss][Ee][Rr][Vv][Ii][Nn][Gg]'})
             ,'calories':tag('div',{'class':'recipe-nutrition','method':'search','pattern':'([0-9]*) *[Cc]alories'})
              ,'fat':tag('div',{'class':'recipe-nutrition','method':'search','pattern':'Fat *[0-9]*% *DV *([0-9]*g)'})
             ,'carbs':tag('div',{'class':'recipe-nutrition','method':'search','pattern':'Carbs *[0-9]*% *DV *([0-9]*g)'})
             ,'protein':tag('div',{'class':'recipe-nutrition','method':'search','pattern':'Protein *[0-9]*% *DV *([0-9]*g)'})
             ,'cholesterol':tag('div',{'class':'recipe-nutrition-full not-shown','method':'search','pattern':'Cholesterol *([0-9]*mg)'})
             ,'sodium':tag('div',{'class':'recipe-nutrition','method':'search','pattern':'Sodium *[0-9]*% *DV *([0-9]*mg)'})
             ,'nreviews':tag('span',{'class':'count font-bold micro-text'})
             ,'reviews':tag('None',{'method':'None'}) #get these
             ,'published':tag('script',{'type':'application/ld+json','method':'search','pattern':'"dateModified":"([^"]*)'})
            }
            ,'epi':
            {'title':tag('div',{'class':'title-source','method':'children','pattern':'h1'})
             ,'description':tag('div',{'itemprop':'description','method':'children','pattern':'p','join':' '})
             ,'ingredients':tag('li',{'class':'ingredient'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('span',{'class':'byline author'})
             ,'instructions':tag('li',{'class':'preparation-step'})
             ,'ttime':tag('None',{'method':'None'})
             ,'ptime':tag('None',{'method':'None'})
             ,'ctime':tag('None',{'method':'None'})
             ,'servings':tag('None',{'method':'None'})
             ,'calories':tag('None',{'method':'None'})
              ,'fat':tag('None',{'method':'None'})
             ,'carbs':tag('None',{'method':'None'})
             ,'protein':tag('None',{'method':'None'})
             ,'cholesterol':tag('None',{'method':'None'})
             ,'sodium':tag('None',{'method':'None'})
             ,'nreviews':tag('span',{'class':'reviews-count'})
             ,'reviews':tag('meta',{'itemprop':'ratingValue','method':'content'}) #get these   
             ,'published':tag('meta',{'itemprop':'datePublished','method':'content'})
             }
            ,'2epi':
             {'title':tag('div',{'class':'title-source','method':'children','pattern':'h1'})
             ,'description':tag('div',{'itemprop':'description','method':'children','pattern':'p','join':' '})
             ,'ingredients':tag('li',{'class':'ingredient'})
             ,'url':tag('link',{'rel':'canonical','method':'href'})
             ,'author':tag('a',{'class':'contributor'})
             ,'instructions':tag('li',{'class':'preparation-step'})
             ,'ttime':tag('None',{'method':'None'})
             ,'ptime':tag('None',{'method':'None'})
             ,'ctime':tag('None',{'method':'None'})
             ,'servings':tag('None',{'method':'None'})
             ,'calories':tag('None',{'method':'None'})
              ,'fat':tag('None',{'method':'None'})
             ,'carbs':tag('None',{'method':'None'})
             ,'protein':tag('None',{'method':'None'})
             ,'cholesterol':tag('None',{'method':'None'})
             ,'sodium':tag('None',{'method':'None'})
             ,'nreviews':tag('span',{'class':'reviews-count'})
             ,'reviews':tag('meta',{'itemprop':'ratingValue','method':'content'})
             ,'published':tag('meta',{'itemprop':'datePublished','method':'content'})#get these   
            }
           }

urldict = {'epi':'https://www.epicurious.com/recipes/member/views/'
        ,'2epi' : 'https://www.epicurious.com/recipes/food/views/'
        ,'yum':'https://www.yummly.com/recipe/'
        ,'bon':''
        ,'ny':'https://cooking.nytimes.com/recipes/'
        ,'ar':'https://www.allrecipes.com/recipe/'
        ,'poy':'https://pinchofyum.com/'
        ,'fn':'https://www.foodnetwork.com/recipes/'}

from scraper import chunks

def gen_jsons_batch(name,num1,num2):
    if name == 'all':
        for i in urldict:
            download_htmls(i)
    else:
        with open('urls/'+name+'_urls','r') as r:
            numbers = r.readlines()
            numbers = [x.replace('\n','') for x in numbers]
        chunked = list(chunks(numbers,100))
        chunked = chunked[num1:num2]
        chunkn = num1*100 + 100
        print('starting')
        for chunk in chunked:
            df = pd.Series(recipe(name,chunk[0]).features)
            df = pd.DataFrame(df)
            df = df.T
            for link in chunk[1:]:
                try:
                    dft = pd.Series(recipe(name,link).features)
                    df = df.append(dft,ignore_index=True)
                except Exception:
                    pass
            df.to_json('json/'+name+str(chunkn))
            print(chunkn,' written')
            chunkn += 100


def gen_jsons(name):
    if name == 'all':
        for i in urldict:
            download_htmls(i)
    else:
        with open('urls/'+name+'_urls','r') as r:
            numbers = r.readlines()
            numbers = [x.replace('\n','') for x in numbers]
        chunked = list(chunks(numbers,100))
        chunkn = 100
        for chunk in chunked:
            df = pd.Series(recipe(name,chunk[0]).features)
            df = pd.DataFrame(df)
            df = df.T
            for link in chunk[1:]:
                try:
                    dft = pd.Series(recipe(name,link).features)
                    df = df.append(dft,ignore_index=True)
                except Exception:
                    pass
            df.to_json('json/'+name+str(chunkn))
            print(chunkn,' written')
            chunkn += 100

if __name__ == "__main__":
    ### Warning Running this will take a long time ###
    gen_jsons('all')
