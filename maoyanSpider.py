import requests
from bs4 import BeautifulSoup

params = {'showType': 3, 'offset': 0}
r = requests.get("https://maoyan.com/films", params=params)
filmNames = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', class_="channel-detail movie-item-title")
filmScore = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', class_="channel-detail channel-detail-orange")
listPaper = BeautifulSoup(r.content.decode(), 'lxml').find('ul', class_="list-pager")
print(len(list(listPaper.children)))

for index in range(len(filmNames)):
    print(filmNames[index]['title'] + ";", "评分: ", end='')
    if filmScore[index].string == '暂无评分':
        print(filmScore[index].string)
    else:
        print(filmScore[index].contents[0].string + filmScore[index].contents[1].string)

# .contents可以直接下标获取直接子节点; .children得到的是list对象，需要for循环获取直接子节点; .descendants可以获得所有子节点
# .string可以获取文本内容，不带标签和属性
# print(xx, end=''): 可以实现不换行输出; print()方法中每个逗号会自动加一个空格，想要连续输出可以直接 '+' 号
