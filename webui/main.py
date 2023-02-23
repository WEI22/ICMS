import os

html_path = r"C:\Users\User\Documents\UM\Year 3\Sem 1\KIX3004\Assignment\ICMS\blog\templates\xxhungry\index.html"

ls = []
with open(html_path, "r") as f:
    ls = f.readlines()

ls1 = []
for i in ls:
    if "img" in i:
        # {% static '' %}
        # j = i.replace("css/", "{% static '")
        # j = j.replace("\">", "' %}\">")
        # ls1.append(j)
        j = i.replace("src=\"", "src=\"{% static '")
        j = j.replace(".png\"", ".png' %}\"")
        j = j.replace(".jpg\"", ".jpg' %}\"")
        ls1.append(j)

    else:
        ls1.append(i)

print(ls1)

with open(html_path, "w") as f:
    f.writelines(ls1)