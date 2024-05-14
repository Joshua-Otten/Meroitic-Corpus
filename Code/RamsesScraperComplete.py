
# need to do other pages now
# pages to redo/correct for 2 brothers text:
# 10, 11, 28, 35, 40, 48, 55, 77, 84, 95
# vb+pfv - COMPLETE
# link to the images for each word - COMPLETE
# download it if you haven't downloaded it before - COMPLETE (just need to convert)

import requests
#from googletrans import Translator
from bs4 import BeautifulSoup
import json
import os

#translator = Translator()

url_number = 2

Not_Found = False

issues = open('issues.txt','a') # will store info about scraping problems to be corrected

while not Not_Found:

    url_origin = "http://ramses.ulg.ac.be/text/legacy/" + str(url_number)
    response = requests.get(url_origin)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        #worthwhile1 = soup.find('Chercher un texte',class_='subtitle')
        #worthwhile2 = soup.find('Find Text',class_='subtitle')
        worthwhile1 = soup.find('h2',text='Chercher un texte')
        worthwhile2 = soup.find('h2',text='Find Text')
        # check if we have the wrong website page currently
        if not worthwhile1 and not worthwhile2:
            # looks like our page is good, scraping is a go!
            title = str(soup.find('h2'))
            title = title[4:len(title)-5]
            print("\033[1m"+title+"\033[0m")
            
            issues.write("\n"+title+"\n"+url_origin+"\n")
            
            # replace '/' with '-' in the filename to prevent naming issues
            new_filename = ''
            if '/' in title.strip():
                for i in range(len(title.strip())):
                    if title.strip()[i] == '/':
                        new_filename += '-'
                    else:
                        new_filename += title.strip()[i]
            else:
                new_filename = title.strip()
            # create new JSON file
            file = open(new_filename+'.json','w',encoding='utf-8')
            
            page = 1
            
            # get starting page and response
            url = url_origin + "?page="+str(page)
            #print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # determining how many pages there are in a doc
            pages_string = soup.find_all(string=lambda text:text and text.startswith('page 1/'))
            # extract the page number from the text
            max_page = int(pages_string[0].split('/')[1].split('<')[0])
            
            # scrape all pages with content
            while page <= max_page:
                print('page',page,'/',max_page)
                # extract the entire sections first
                extract_transliterations = soup.find_all('div',class_='transliteration')
                extract_partsOfSpeech = soup.find_all('div',class_='partOfSpeech')
                extract_translations = soup.find_all('p',class_='translation')
                
                # turn them all into strings
                complete_transliteration = ''
                for word in extract_transliterations:
                    if word.text == '':
                        complete_transliteration += '[?] '
                    else:
                        complete_transliteration += word.text + ' '
                complete_partsOfSpeech = ''
                for word in extract_partsOfSpeech:
                    if word.text == '':
                        complete_transliteration += '[?] '
                    else:
                        complete_partsOfSpeech += word.text + ' '
                complete_translation = ''
                for word in extract_translations:
                    if word.text == '':
                        complete_transliteration += '[?] '
                    else:
                        complete_translation += word.text + ' '
                
                # strip them all
                complete_transliteration = complete_transliteration.strip()
                complete_partsOfSpeech = complete_partsOfSpeech.strip()
                complete_translation = complete_translation.strip()
                
                
                # now, need to extract each individual word from complete transliteration, parts of speech, and translation
                # transliterations will be the same
                # parts of speech are also the same, but may need to be grouped
                # translations are a different set of terms (and may also need to be grouped?)
                
                #tables = soup.find_all('table', class_='ramsesLine')
                
                #### get individual parts of speech ####
                analysis_text = []
                tables = soup.find_all('table', class_='ramsesLine')
                for table in tables:
                    analysis_rows = table.find_all('tr', class_='analysis')
                    for row in analysis_rows:
                        cells = row.find_all('td', class_='word')
                        for cell in cells:
                            parts = cell.find_all('div')
                            if len(parts) > 1:
                                formatted_text = ''
                                for i in range(len(parts)):
                                    formatted_text += parts[i].get_text().strip()
                                    if i<len(parts)-1:
                                        formatted_text += '+'
                                analysis_text.append(formatted_text)
                            #elif cell.get_text().strip() != '':
                            else:
                                analysis_text.append(cell.get_text().strip())
                #print(analysis_text)
                parts_of_speech = analysis_text
                ###### end new attempt with parts of speech ######
                


                
                transliterations = list()
                #parts_of_speech = list()
                translations = list()



                # getting the images and downloading them
                img_tags = soup.find_all('img')
                image_files = [img['src'] for img in img_tags]
                for i in range(len(image_files)):
                    image_files[i] = 'http://ramses.ulg.ac.be/'+image_files[i]
                
                # Image download/file-writing not completely working for some reason
                for link in image_files:
                    img_name = link.split('/')[-1]
                    if not os.path.exists('image_svg/'+img_name+'.svg'):
                        img_url = link
                        img_response = requests.get(img_url)
                        #print(img_url)
                        if img_response.status_code == 200:
                            filename = link.split('/')[-1]+ '.svg'
                            with open('image_svg/'+filename, 'wb') as f:
                                f.write(img_response.content)
                        else:
                            print('ERROR downloading image:',link)
                            issues.write('\tError downloading image: '+link+'\n')
                
                
                #### get individual transliterations ####
                translit_text = []
                tables = soup.find_all('table', class_='ramsesLine')
                for table in tables:
                    trans_rows = table.find_all('tr', class_='transliteration')
                    for row in trans_rows:
                        cells = row.find_all('td', class_='word')
                        for cell in cells:
                            translit_text.append(cell.get_text().strip())
                transliterations = translit_text
                #print(parts_of_speech)
                #print(transliterations)
                ###### end new attempt with transliterations ######
                
                
                #### get individual translations ####
                for table in tables:
                    translations.extend([trans.text.strip() for trans in table.select('.translation .word span')])
                #print(translations)
                ###### end new attempt with transliterations ######
                
                # check that everything is normal
                if len(transliterations) != len(parts_of_speech) != len(translations):
                    print('ERROR for page',page)
                    
                #### Now, replace any '' with 'NOT PROVIDED' ####
                for i in range(len(transliterations)):
                    if transliterations[i] == '':
                        transliterations[i] = 'NOT PROVIDED'
                    if parts_of_speech[i] == '':
                        parts_of_speech[i] = 'NOT PROVIDED'
                    if translations[i] == '':
                        translations[i] = 'NOT PROVIDED'
                

                
                '''
                ##### previous code:
                # Iterate through tables
                for table in tables:

                    # Extract transliterations
                    transliterations.extend([trans.text.strip() for trans in table.select('.transliteration .word div') if trans.text.strip() != ''])

                    # Extract parts of speech
                    parts_of_speech.extend([pos.text.strip() for pos in table.select('.analysis .word div') if pos.text.strip() != ''])
                    #pos_elements = table.select('.analysis .word div')
                    # removing inflection elements.  NOTE: may need to add additional analysis types!
                    inflection_elements = table.select('.analysis .inflection')
                    for inf in inflection_elements:
                        index = parts_of_speech.index(inf.text.strip())
                        # basically, if there is an inflection or something, merge it with the element from before so that all elements of a column occupy one spot in the list
                        parts_of_speech = parts_of_speech[:index-1] + ['+'.join(parts_of_speech[index-1:index+1])] + parts_of_speech[index+1:]

                    # Extract translations
                    translations.extend([trans.text.strip() for trans in table.select('.translation .word span') if trans.text.strip() != ''])

                #print("Transliterations:", transliterations)
                #print("Parts of Speech:", parts_of_speech)
                #print("Translations:", translations)
                #print("---")
                
                word_translations_rows = soup.find_all('tr',class_='translation')
                
                # we need to know if a give text has some issue which prevents these from being aligned
                if (len(transliterations) != len(parts_of_speech) != len(translations)):
                    print('text =',title.strip())
                    print('page =',page)
                    print("Transliterations:", transliterations)
                    print("Parts of Speech:", parts_of_speech)
                    print("Translations:", translations)
                    print("---")
                    print('NEED TO DO CORRECT PAGE',page,'MANUALLY. Initial attempt will be written in JSON file')
                    issues.write('\tCorrect page '+str(page)+' manually.\n')
                    #raise IndexError(" transliterations, parts of speech, and translations list lengths do not match")
                '''
                try:
                    # create list for individual word analysis
                    words = list()
                    for i in range(len(transliterations)):
                        word_data = {
                            'position': i,
                            'text': title.strip(),
                            'page': page,
                            'transliteration': transliterations[i],
                            'partOfSpeech': parts_of_speech[i],
                            'translation': translations[i],
                            'glyphs web link': image_files[i],
                            'glyphs path': 'images/'+image_files[i].split('/')[-1]+'.png'
                        }
                        words.append(word_data)
                    
                    
                    
                    data = {
                        'block type': 'page',
                        'text': title.strip(),
                        'page': page,
                        'transliteration': complete_transliteration,
                        'partsOfSpeech': complete_partsOfSpeech,
                        'translation': complete_translation,
                        'words': words,
                    }
                    
                    json_data = json.dumps(data, indent=2, ensure_ascii=False)
                    file.write(json_data)
                    file.write('\n')
                    
                except IndexError: # this shouldn't be an issue anymore
                    print('INDEX ERROR for page',page)
                    print('MUST DO THIS MANUALLY')
                    issues.write('\tpage '+str(page)+' not written\n')
                
                # get next page...
                page += 1
                url = url_origin + "?page="+str(page)
                #print(url)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
        else:
            print('url',url_number,'did not seem to have anything')
        url_number += 1
        print('next url, prev was:',url_origin)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
        Not_Found = True

issues.close()
