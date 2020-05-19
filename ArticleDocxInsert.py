import docx


class Reader:

    def main(self):
        file = docx.Document('article.docx')
        fulltext = []
        for para in file.paragraphs:
            fulltext.append(para.text)
        title = fulltext[0].strip()
        author = fulltext[2].strip()

        with open('Example.html', 'r+', encoding='UTF8') as t:
            th = open('ArticlePage.html', 'w')
            for i, line in enumerate(t, start=0):
                if 60 <= i <= 100:
                    if '<h1 class="titlehere mb-3"><font color = "white"><b>' in line:
                        th.writelines('            <h1 class="mb-3"><font color = "white"><b>'
                                      + str(title) + '</b></font></h1>')
                    if '<h3 class="authorhere mb-3"></h3>' in line:
                        th.writelines('            <h3 style="text-align: right">'
                                      + str(author) + '</h3><br>')

                    try:
                        for index in range(1, 20):
                            if "p id='para"+str(index)+"'" in line:
                                th.write("            <p>" + str(fulltext[2+(2*index)]) + "</p>\n")
                                break

                        if "p id='para" + str(index) + "'" not in line:
                            th.write(line)

                    except:
                        pass
                else:
                    th.writelines(line)


obj = Reader()
obj.main()
