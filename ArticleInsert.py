class Reader:

    def main(self):
        file = open('article.docx', 'r+', encoding='UTF8')
        article = file.read()
        paragraphs = article.split('\n')
        title = paragraphs[0].strip()
        author = paragraphs[2].strip()

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

                    if "<p id='para1'>" in line:
                        th.write("            <p>"+str(paragraphs[4])+"</p>\n")
                    if "<p id='para2'>" in line:
                        th.writelines("            <p>" + str(paragraphs[6]) + "</p>\n")
                    if "<p id='para3'></p>" in line:
                        th.writelines("            <p>" + str(paragraphs[8]) + "</p>\n")
                    if "<p id='para4'></p>" in line:
                        th.writelines("            <p>" + str(paragraphs[10]) + "</p>\n")
                    if "<p id='para5'></p>" in line:
                        th.writelines("            <p>" + str(paragraphs[12]) + "</p>\n")
                    if "<p id='para6'></p>" in line:
                        th.writelines("            <p>" + str(paragraphs[14]) + "</p>\n")
                    if "<p id='para7'></p>" in line:
                        th.writelines("            <p>" + str(paragraphs[16]) + "</p>\n")
                    else:
                        th.writelines(line)
                else:
                    th.writelines(line)

        file.close()
        th.close()


obj = Reader()
obj.main()
