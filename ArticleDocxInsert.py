import sys
import os.path
from pathlib import Path
import docx
import re
import random
import readtime
import csv


class VerityPlatform:

    def __init__(self):
        self.file_path = ''
        self.fulltext = []
        self.text_string = ''
        self.article_title_insert = ''
        self.title_word_count = []
        self.article_title_code = ''
        self.author_names_insert = ''
        self.author_names = []
        self.writerpage_codes = []
        self.department = ''
        self.department_code = ''
        self.articlepage_code = ''
        self.article_date = ''
        self.readtime = ''

    def path_handler(self, file_path):
        self.file_path = Path(file_path)
        self.file_path = self.file_path / "raw_data.txt"
        print(self.file_path)
        return

    def extract_article_contents(self, article_number_code):
        # call the article doc
        file = docx.Document('D:/CS/web/Verily/Verily/articles/article' + str(article_number_code) + '.docx')

        # extract the article into paragraphs and substitute special characters
        for para in file.paragraphs:
            parag = re.sub(r'“', '"', para.text)
            parag = re.sub(r'”', '"', parag)
            parag = re.sub(r"’", "'", parag)
            parag = re.sub(r"‘", "'", parag)
            parag = re.sub(r" ", " ", parag)
            parag = re.sub(r"–", "-", parag)
            parag = re.sub(r"—", "-", parag)
            parag = re.sub(r"ü", "u", parag)
            parag = re.sub(r"é", "&#233", parag)
            self.fulltext.append(parag)
            self.text_string = self.text_string + " " + parag

        # extract the title and the articlepage.html name from the article
        self.article_title_insert = self.fulltext[0].strip()
        self.article_title_insert = re.sub('"', "'", self.article_title_insert)
        self.title_word_count = self.article_title_insert.lower().split(' ')
        self.article_title_code = "article"
        if len(self.title_word_count) >= 3:
            self.article_title_code = self.article_title_code + str(article_number_code) + '-' + \
                                      self.title_word_count[0] + '-' + self.title_word_count[1] + '-' + \
                                      self.title_word_count[2]
        elif len(self.title_word_count) == 2:
            self.article_title_code = self.article_title_code + str(article_number_code) + '-' + \
                                      self.title_word_count[0] + '-' + self.title_word_count[1]
        elif len(self.title_word_count) == 1:
            self.article_title_code = self.article_title_code + str(article_number_code) + '-' + \
                                      self.title_word_count[0]
        self.article_title_code = self.article_title_code.strip()

        # extract the author name(s) from the articles
        self.author_names_insert = self.fulltext[2].strip()
        self.author_names = self.author_names_insert.split(',')
        self.writerpage_codes = self.author_names_insert.lower().split(',')
        self.writerpage_codes = [re.sub(r' ', '', author) for author in self.writerpage_codes]
        self.writerpage_codes = ['w-' + author for author in self.writerpage_codes]

        # initialize default article information
        self.department = "Verity Today"
        self.article_date = "2020"

        # manually infer department from article number
        self.department = 'Tech' if article_number_code in [1, 2, 3, 42, 43] else self.department
        self.department = 'Sports' if article_number_code in [4, 5, 6, 7, 45, 46] else self.department
        self.department = 'Social Change' if article_number_code in [8, 9, 10, 11, 12] else self.department
        self.department = 'Mental Health' if article_number_code in [13, 14, 15, 16] else self.department
        self.department = 'Global' if article_number_code in [17, 18, 19, 20, 44] else self.department
        self.department = 'Entertainment' if article_number_code in [21, 22, 23, 24, 25, 26, 27] else self.department
        self.department = 'Education' if article_number_code in [28, 29, 30, 31, 32] else self.department
        self.department = 'Creativity' if article_number_code in [33, 34, 35, 36, 37, 38] else self.department
        self.department = 'Biz & Eco' if article_number_code in [39, 40, 41] else self.department

        with open('article_info.csv', mode='r+', newline="\n") as article_info:
            reader = csv.reader(article_info, delimiter=',')
            for row in reader:
                if str(row[0]) == str(article_number_code):
                    self.department = 'Tech' if str(row[3][0]) == 'T' else self.department
                    self.department = 'Sports' if str(row[3][0]) == 'S' else self.department
                    self.department = 'Social Change' if str(row[3][1]) == 'o' else self.department
                    self.department = 'Mental Health' if str(row[3][0]) == 'M' else self.department
                    self.department = 'Global' if str(row[3][0]) == 'G' else self.department
                    self.department = 'Entertainment' if str(row[3][0]) == 'E' else self.department
                    self.department = 'Education' if str(row[3][1]) == 'd' else self.department
                    self.department = 'Creativity' if str(row[3][0]) == 'C' else self.department
                    self.department = 'Biz & Eco' if str(row[3][0]) == 'B' else self.department
                    self.article_date = str(row[4])
                    break

        self.department_code = (self.department.split(' '))[0].lower()

        self.articlepage_code = 'a-' + self.department_code + '-' + self.article_title_code

        # assign the date of the article
        if 1 <= article_number_code <= 46:
            self.article_date = "July 2020"
        elif 47 <= article_number_code <= 47:
            self.article_date = "August 2020"

        # calculate the time to read the article
        self.readtime = str(readtime.of_text(self.text_string))

        print("Article details and content extracted, 0")
        return "Article details and content extracted, 0"

    def replace_in_line(self, keyword, line, start, end, article_number_code):

        replacements = {"{{title}}": self.article_title_insert,
                        "{{department-code}}": self.department_code,
                        "{{department}}": self.department,
                        "{{authors}}": self.author_names_insert,
                        "{{date}}": self.article_date,
                        "{{read-time}}": str(self.readtime),
                        "{{number-code}}": str(article_number_code),
                        "{{author-0-link}}": self.writerpage_codes[0],
                        "{{author-0}}": self.author_names[0],
                        "{{author-0-description}}": descriptions.get(
                            self.writerpage_codes[0], (self.author_names[0] + " is a writer for Verity Today."))}

        new_line = line[:start-1]
        new_line += replacements.get(keyword, '{error}')
        new_line += line[end+3:]
        return new_line

    def create_article_page(self, article_number_code):

        with open('D:/CS/web/Verily/Verily/template-a.html', 'r+', encoding='UTF-8') as template:
            with open('D:/CS/web/Verily/Verily/a-' + str(self.department_code) + '-' +
                      str(self.article_title_code) + '.html', 'w') as article_page:

                # iterate the article-template page
                for i, line in enumerate(template, start=0):

                    # iterate over the other authors and insert details
                    for author_number in [1, 2]:
                        found = False
                        if len(self.writerpage_codes) == author_number+1:
                            if '<div class="about-author auth' + str(author_number) + ' d-flex p-4" ' \
                               'style="background-color: rgba(30, 30, 30, 1); display: none !important;">' in line:
                                article_page.write('<div class="about-author d-flex p-4" '
                                                   'style="background-color: rgba(30, 30, 30, 1);">\n')
                                found = True
                                break
                            if '<h3 class="hc"><a href="/{{author-' + str(author_number) + \
                                    '-link}}" class="hc">{{author-' + str(author_number) + '}}</a></h3>' in line:
                                article_page.write('<h3 class="hc"><a href="/' +
                                                   str(self.writerpage_codes[author_number]) + '" class="hc">' +
                                                   str(self.author_names[author_number] + '</a></h3>\n'))
                                found = True
                                break
                            if '<p class="tc">{{author-' + str(author_number) + '-description}}</p>' in line:
                                article_page.write('<p class="tc">' +
                                                   descriptions.get(self.writerpage_codes[author_number],
                                                                    (self.author_names[author_number] +
                                                                     " is a writer for Verity Today.")) + '</p>\n')
                                found = True
                                break
                    if found:
                        continue

                    # insert the paragraphs
                    try:
                        # check for paragraph slots and insert the equivalent paragraphs
                        if "<p id='para1'></p>" in line:
                            article_page.write('<p class="articleparagraph" style="color: white;">' +
                                               str(self.fulltext[2 + 2]) + "</p>\n")
                            continue
                        for index in range(2, 21):
                            if "<p class='para'></p>" in line:
                                article_page.write('<p class="articleparagraph" style="color: white;">' +
                                                   str(self.fulltext[2 + (2 * index)]) + "</p>\n\n")
                                continue
                    except Exception:
                        pass

                    while '{{' in line:
                        for index, character in enumerate(line):
                            if character == '{' and line[index - 1] == '{':
                                remaining_line = line[index + 1:]
                                for last_index, last_character in enumerate(remaining_line):
                                    if last_character == '}' and remaining_line[last_index - 1] == '}':
                                        keyword = line[(index - 1):(last_index + 2 + index)]
                                        index_end = last_index - 1 + index
                                        line = self.replace_in_line(keyword, line, index, index_end, article_number_code)
                                        break
                    article_page.write(line)

        print("Article page created successfully, 0")

    def insert_department_page(self, article_number_code):

        with open('D:/CS/web/Verily/Verily/d-' + str(self.department_code) + '.html', 'r+') as department_page:
            with open('D:/CS/web/Verily/Verily/temp-d.html', 'w') as temporary_page:
                for i, line in enumerate(department_page, start=0):
                    temporary_page.writelines(line)

        with open('D:/CS/web/Verily/Verily/temp-d.html', 'r+') as temporary_page:
            with open('D:/CS/web/Verily/Verily/d-' + str(self.department_code) + '.html', 'w') as department_page:
                finished = False
                search_finished = False
                for i, line in enumerate(temporary_page, start=0):

                    # write the article block in the department page
                    if '<div class="article"></div>' in line and not finished:
                        department_page.write('<div class="article"></div>\n\n')
                        department_page.write('<div class="col-md-6">\n')
                        department_page.write('<div class="blog-entry ftco-animate">\n')
                        department_page.write('<a href="/' + self.articlepage_code +
                                              '" class="img img-2" style="background-image: url(articles/article' +
                                              str(article_number_code) + '.jpg);"></a>\n')
                        department_page.write('<div class="text text-2 pt-2 mt-3">\n')
                        department_page.write('<a href="/' + self.articlepage_code +
                                              '"><h3 class="mb-2 hc">' + self.article_title_insert + '</h3></a>\n')
                        department_page.write('<div class="meta-wrap">\n')
                        department_page.write('<p class="meta">\n')
                        department_page.write('<span><i class="icon-calendar mr-2"></i>' +
                                              self.article_date + '</span>\n')
                        department_page.write('<span><i class="icon-folder-o mr-2"></i><a href="/' +
                                              self.writerpage_codes[0] + '" class="hc">' +
                                              self.author_names[0] + '</a></span>\n')
                        department_page.write('</p>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n\n')
                        finished = True

                    # write the article block in the search block
                    elif '<div class="article-searchable"></div>' in line and not search_finished:
                        department_page.write('<div class="col-md-6 searchable" style="display: none;">\n')
                        department_page.write('<div class="blog-entry ftco-animate">\n')
                        department_page.write('<a href="/' + self.articlepage_code +
                                              '" class="img img-2" style="background-image: url(articles/article' +
                                              str(article_number_code) + '.jpg);"></a>\n')
                        department_page.write('<div class="text text-2 pt-2 mt-3">\n')
                        department_page.write('<a href="/' + self.articlepage_code +
                                              '"><h3 class="mb-2 hc">' + self.article_title_insert + '</h3></a>\n')
                        department_page.write('<div class="meta-wrap">\n')
                        department_page.write('<p class="meta">\n')
                        department_page.write('<span><i class="icon-calendar mr-2"></i>' +
                                              self.article_date + '</span>\n')
                        department_page.write('<span><i class="icon-folder-o mr-2"></i><a href="/' +
                                              self.writerpage_codes[0] + '" class="hc">' +
                                              self.author_names[0] + '</a></span>\n')
                        department_page.write('</p>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n')
                        department_page.write('</div>\n\n')
                        department_page.write('<div class="article-searchable"></div>\n\n')
                        search_finished = True

                    # if the flag line isn't found, rewrite the original line
                    else:
                        department_page.writelines(line)

        print("Department page updated successfully, 0")

    def insert_writer_page(self, article_number_code):

        # iterate over the list of authors of the article
        for author_counter in range(0, len(self.author_names)):

            # check if a w-page needs to be created for the author
            if not os.path.isfile('D:/CS/web/Verily/Verily/' + self.writerpage_codes[author_counter] + '.html'):

                with open('D:/CS/web/Verily/Verily/template-w.html', 'r+') as writer_template:
                    with open('D:/CS/web/Verily/Verily/' + self.writerpage_codes[author_counter] +
                              '.html', 'w') as writer_page:

                        # iterate the w-template page
                        for i, line in enumerate(writer_template, start=0):

                            # insert the author name into the head title
                            if '<title>Author</title>' in line:
                                writer_page.write('<title>' + self.author_names[author_counter] + '</title>\n')
                                continue

                            # insert the writer information into the breadcrumbs
                            if '<p class="breadcrumbs"><span class="mr-2"><a href="index.html">Home</a></span>' \
                               ' <span class="mr-2"><a href="team.html">The Team</a> </span>' \
                               '<span class="mr-2">Author</span></p>' in line:
                                writer_page.write('<p class="breadcrumbs"><span class="mr-2"><a href="/index">Home</a>'
                                                  '</span> <span class="mr-2"><a href="/team">The Team</a></span>'
                                                  '<span class="mr-2 final-link">' +
                                                  self.author_names[author_counter].split(' ')[0] + '</span></p>\n')
                                continue
                            # insert the author name into the header section
                            if '<h1 class="mb-3 bread hc">Author Name</h1>' in line:
                                writer_page.write('<h1 class="mb-3 bread hc">' + self.author_names[author_counter] +
                                                  '</h1>\n')
                                continue
                            # insert the author profile picture into the header section
                            if '<div class="img" style="background-image: url(images/w-author.jpg);">' in line:
                                # check if a personal profile picture exists and insert it if it does
                                if os.path.isfile('D:/CS/web/Verily/Verily/images/' +
                                                  self.writerpage_codes[author_counter] + '.jpg'):
                                    writer_page.write('<div class="img" style="background-image: url(images/' +
                                                      self.writerpage_codes[author_counter] + '.jpg);">\n')
                                # if it doesn't, pick an avatar at random and insert it
                                else:
                                    writer_page.write('<div class="img" style="background-image: url(images/avatar' +
                                                      str(random.randint(1, 9)) + '.webp);">\n')
                                    continue
                            # insert the author description into the header section,
                            # or a default description if the author's doesn't exist
                            if '<p>Author desc here</p>' in line:
                                writer_page.write('<p>' +
                                                  descriptions.get(self.writerpage_codes[author_counter],
                                                                   (self.author_names[author_counter] +
                                                                    " is a writer for Verity Today.")) + '</p>\n')
                                continue

                            # insert the author name into the read-more-from line
                            if '''<h3 class="mb-3 bread font-weight-bold hc">Read Author's Work</h3>''' in line:
                                writer_page.write('<h3 class="mb-3 bread font-weight-bold hc">Read ' +
                                                  self.author_names[author_counter].split(' ')[0] +
                                                  ''''s Work</h3>\n''')
                                continue

                            # insert the article link and picture into the article slot
                            if '<a href="article1.html" class="img img-2" style="background-image: ' \
                               'url(articles/article1.jpg);"></a>' in line:
                                writer_page.write('<a href="/' + self.articlepage_code +
                                                  '" class="img img-2" style="background-image: '
                                                  'url(articles/article' + str(article_number_code) + '.jpg);"></a>\n')
                                continue
                            # insert the article link and name into the article slot
                            if '<a href="article1.html"><h3 class="mb-2 hc">More Rise Than Fall</h3></a>' in line:
                                writer_page.write('<a href="/' + self.articlepage_code +
                                                  '"><h3 class="mb-2 hc">' + self.article_title_insert + '</h3></a>\n')
                                continue

                            # insert the department link and name into the article slot
                            if '<span><i class="icon-folder-o mr-2"></i><a href="tech.html" ' \
                               'class="hc">Technology</a></span>' in line:
                                writer_page.write('<span><i class="icon-folder-o mr-2"></i><a href="/d-' +
                                                  self.department_code + '" class="hc">' +
                                                  self.department + '</a></span>\n')
                                continue

                            # if none of the flag lines are found, rewrite the original line
                            else:
                                writer_page.writelines(line)

                print("Writer page created successfully, 0")

            # check if a w-page already exists for the author
            elif os.path.isfile('D:/CS/web/Verily/Verily/' + self.writerpage_codes[author_counter] + '.html'):

                with open('D:/CS/web/Verily/Verily/' + self.writerpage_codes[author_counter] +
                          '.html', 'r+') as writer_page:
                    with open('D:/CS/web/Verily/Verily/temp-w.html', 'w') as temp_writer:
                        for i, line in enumerate(writer_page, start=0):
                            temp_writer.writelines(line)

                with open('D:/CS/web/Verily/Verily/temp-w.html', 'r+') as temp_writer:
                    with open('D:/CS/web/Verily/Verily/' + self.writerpage_codes[author_counter] +
                              '.html', 'r+') as writer_page:
                        finished = False

                        for i, line in enumerate(temp_writer, start=0):

                            if '<div class="article"></div>' in line and not finished:

                                writer_page.write('<div class="article"></div>\n')
                                writer_page.write('<div class="col-md-4 searchable">\n')
                                writer_page.write('<div class="blog-entry ftco-animate">\n')
                                writer_page.write('<a href="/' + self.articlepage_code +
                                                  '" class="img img-2" style="background-image: url(articles/article'
                                                  + str(article_number_code) + '.jpg);"></a>\n')
                                writer_page.write('<div class="text text-2 pt-2 mt-3">\n')
                                writer_page.write('<a href="/' + self.articlepage_code + '"><h3 class="mb-2 hc">' +
                                                  self.article_title_insert + '</h3></a>\n')
                                writer_page.write('<div class="meta-wrap">\n')
                                writer_page.write('<p class="meta">\n')
                                writer_page.write('<span><i class="icon-calendar mr-2"></i>June 2020</span>\n')
                                writer_page.write('<span><i class="icon-folder-o mr-2"></i><a href="/d-' +
                                                  self.department_code + '" class="hc">' +
                                                  self.department + '</a></span>\n')
                                writer_page.write('</p>\n')
                                writer_page.write('</div>\n')
                                writer_page.write('</div>\n')
                                writer_page.write('</div>\n')
                                writer_page.write('</div>\n\n')
                                finished = True

                            else:
                                writer_page.writelines(line)

                print("Writer page updated successfully, 0")


descriptions = {'w-karnavpopat': 'Karnav writes for Tech, Sports and Biz, and maintains this site.'}

if __name__ == '__main__':
    # select mode of insertion
    path = 'D:/CS/web/Verily/Verily/'
    dep_page = input('Do you want to insert the articles into the department pages?')
    w_page = input('Do you want to insert the articles into the author page(s)?')

    # insert the articles
    for code in range(41, 42):
        # exclude the articles which need image grid templates
        if code in range(-1, -1):
            pass

        try:
            obj = VerityPlatform()
            print(code)  # article number
            obj.extract_article_contents(code)
            obj.create_article_page(code)
            if dep_page[0].lower() == 'y':
                print("f")
                obj.insert_department_page(code)
            if w_page[0].lower() == 'y':
                obj.insert_writer_page(code)

        except Exception as e:
            print(e)
            continue

    sys.exit(0)
