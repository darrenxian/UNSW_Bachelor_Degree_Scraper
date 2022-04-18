# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Import Libraries

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

# %% [markdown]
# ### Scrape Bachelor Degrees Website 

# %%
# Given bachelors degree website url
website="https://www.unsw.edu.au/business/study/undergraduate/bachelor-degrees"

# Pull HTML from website using requests package to web_page
web_page=requests.get(website).content.decode('UTF-8')

# Parse HTML and load it to a bs4 structure assigned to webpage_content
webpage_content = BeautifulSoup(web_page,'html.parser') 


# %%
# Use CSS selector to select all elements in <a> within h3 which is within parent div[class=node-title]
links_raw=webpage_content.select("div[class=node-title] > h3 > a")


# %%
# UNSW website
School_website='https://www.unsw.edu.au'

# Test for bachelor of actuarial studies url
links_raw[0]['href']

# For loop that creates a list with our final 5 degree websites
Links=[]
for i in range(0,len(links_raw)):
    Links.append(School_website+links_raw[i]['href']) # save the links of the 5 pages


# %%
Links

# %% [markdown]
# ### Create DataFrame

# %%
# Create the column names
column_names = ["Degree","Faculty","Delivery Mode","Award","Commencing Terms","Duration Full Time","Key Features","Program Code"," CRICOS Code","UAC Code" , "UOC Code" , "Campus","Indicative Enrolments","link", "2021 lowest Selection Rank_2","2021 A levels", "2021 IB Diploma"," 2021 Lowest ATAR", "Review"]

# Create the dataframe
Degrees_database= pd.DataFrame(columns = column_names)

# %% [markdown]
# ### Find necessary features

# %%
# for loop that scrapes the 5 webpages and inserts the data in the dataframe
for link in Links:
    
    # Pull HTML from each degree website
    degree_page=requests.get(link).content.decode('UTF-8')
    
    # Parse HTML and load to bs4 object 
    degree_page = BeautifulSoup(degree_page,'html.parser') 
    
    # Scrape the degree_name
    degree_name=degree_page.select("div.page-header.background-shape-2 > div.content > h1 " )[0].get_text().strip()
    
    # Scrape the tile which includes Faculty, Delivery Mode, Award, Commencing Terms, Duration
    tile=degree_page.select("div.propertytiles.property-tiles-bg-colour--light-grey.section > div.property-tiles > div.property-tile > div.text" )

    faculty=tile[0].get_text().strip()

    delivery_mode=tile[1].get_text().strip()

    Award=tile[2].get_text().strip()

    commencing_terms=tile[3].get_text().strip()

    Duration_Full_Time=tile[4].get_text().strip()
    
    # Select 'Key features' text
    key_features_raw=degree_page.select("div.text.uds-component.section" )[2].select("span > div >p >b " )

    key_features=key_features_raw[0].get_text().strip()
    
    # Concatenate the key features with comma
    for i in key_features_raw:
        key_features=key_features+','+i.get_text().strip()

    # Find Program Code
    Program_Code=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[5].get_text().strip()
    
    # Find CRICOS Code
    CRICOS_Code=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[6].get_text().strip()

    # Find UAC Code
    UAC_Code=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[8].get_text().strip()

    # Find UOC
    UOC=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[9].get_text().strip()

    # Find Campus
    Campus=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[7].get_text().strip()

    # Find Indicative Enrolments
    Indicative_Enrolments=degree_page.select("div.propertytiles.section > div.property-tiles > div.property-tile > div.text" )[10].get_text().strip()
    
    v=degree_page.find("span", class_="analytics-container" )
    
    # Scrape the video  or the picture by using a condition
    if v:
        link_src=degree_page.select('.youtube-player' )[0]['data-src']
        link='https://www.youtube.com/watch?v='+link_src
    else:
        link=degree_page.select("div.media > picture > img" )[0]['src']
        link=School_website+link

    raw_21_tiles=degree_page.select(" div.responsivegrid.aem-GridColumn--default--none.aem-GridColumn.aem-GridColumn--default--12.aem-GridColumn--medium--12.aem-GridColumn--small--12.aem-GridColumn--offset--default--0 > div.propertytiles.property-tiles-bg-colour--light-grey.section > div[class=property-tiles] > div[class=property-tile] > div[class=text] ")
    
    # 2021 lowest selection rank
    lowest_selection_rank_21=raw_21_tiles[0].get_text().strip()

    # 2021 A levels
    A_levels_21=raw_21_tiles[1].get_text().strip()

    # 2021 IB Diploma
    IB_diploma_21=raw_21_tiles[2].get_text().strip()

    # 2021 Lowest ATAR
    Lowest_atar_21=raw_21_tiles[3].get_text().strip()

    # Get quote 
    quote=degree_page.find(class_="quote" ).get_text().strip()
    author=degree_page.find(class_="author-name h5" ).get_text().strip()

    role=degree_page.find(class_="author-role lead-text" ).get_text().strip()
    
    # Create the review by concatenating quote, author and role
    review=quote+' '+author+','+role

    # Insert the data into the dataframe
    series_obj = pd.Series( [degree_name,faculty,delivery_mode,Award,commencing_terms,Duration_Full_Time,key_features,Program_Code,CRICOS_Code,UAC_Code,UOC,Campus,Indicative_Enrolments,link,lowest_selection_rank_21,A_levels_21,IB_diploma_21,Lowest_atar_21,review], 
                        index=Degrees_database.columns )
    Degrees_database = Degrees_database.append( series_obj,
                        ignore_index=True)

# %% [markdown]
# ### Save to CSV

# %%
#save the dataframe to a CSV file
Degrees_database.to_csv('Bachelors_Degrees.csv',index=False)


# %%



