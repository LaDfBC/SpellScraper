from bs4 import BeautifulSoup, NavigableString, Tag
import requests

important_texts = ['Casting Time', 'Duration', 'Range', 'DESCRIPTION', 'Components', 'Saving Throw', 'Spell Resistance']

def print_all_spells():
    outfile = open("/home/squeaky/druid_spells.txt", mode='w')
    page = requests.get("http://www.d20pfsrd.com/magic/spell-lists-and-domains/spell-lists-druid/")
    soup = BeautifulSoup(page.content)

    tables = soup.findAll(lambda tag: tag.name == 'table')

    level = 0
    for table in tables:
        print_spells_for_level(table.find(lambda tag: tag.name == 'tbody'), level, outfile)
        level += 1

    outfile.close()

def get_spell_information(spell_link):
    successful = False
    count = 0
    while not successful:
        try:
            spell_page = requests.get(spell_link)
            successful = True
            count = 0
        except:
            count = count + 1
            print(count)
            continue
    soup = BeautifulSoup(spell_page.content)
    spell_map = {}
    try:
        title = soup.find('h1').text
        spell_map['Title'] = title

        school = soup.find(lambda tag: tag.text == 'School')
        spell_map['School'] = school.parent.find('a').next

        tag = soup.find('p', class_='divider')

        output = ""
        current_tag = None
        tag = tag.next.next.next.next

        while True:
            if tag.next == None:
                break
            if tag == None:
                tag = tag.next
                continue
            elif tag in important_texts:
                if current_tag != None:
                    spell_map[current_tag] = output.lstrip(" ").rstrip(" ").strip("\n")
                    output = ""
                current_tag = tag
            elif type(tag) is NavigableString:
                if 'effect' in tag.strip("\n").lower():
                    tag = tag.next
                    continue
                if 'Section 15' in tag:
                    spell_map['Description'] = output.lstrip(" ").rstrip(" ").strip("\n")
                    break
                output = output + tag
            elif type(tag) is Tag:
                if 'id' in tag.attrs and tag['id'] == 'comments':
                    spell_map['Description'] = output.lstrip(" ").rstrip(" ").strip("\n")
                    break
            tag = tag.next

        return spell_map
    except:
        return spell_map



def print_spells_for_level(table_soup, level, outfile):

    spells = table_soup.findAll(lambda tag: tag.name == 'tr')
    for spell in spells:
        spell_link = spell.find(lambda tag: tag.name == 'td').find('a')['href']
        information_map = get_spell_information(spell_link)
        try:
            outfile.write(str(level) + ";")
            outfile.write(information_map['Title'] + ";")
            outfile.write(information_map['School'] + ";")
            outfile.write(information_map['Casting Time'] + ";")
            outfile.write(information_map['Range'] + ";")
            outfile.write(information_map['Components'] + ";")
            outfile.write(information_map['Duration'] + ";")
            outfile.write('\"' + information_map['Description'] + "\";")
            outfile.write("Druid\n")
            print(information_map['Title'])
        except:
            print(information_map)

print_all_spells()