
#신문 기사 제목에서, 우리가 원치 않는 내용들을 replace하기 위한 함수
def titleReplacer(file,titleList):
    xs = file.readlines()
    for x in xs:
        _list = x.split('^')[0]
        #크롤링 시 구분자를 ^로 했기 때문.
        titleList.append(_list.replace("&"," ").replace("?","").replace("→","").replace(",","").replace("'","").replace("[","").replace("]","").replace(".","").replace("·"," ").replace("\"","").replace("…","").replace("“","").replace("‘","").replace("”","").split())

#titleReplacer에서 구한 data들을 서로서로 비교해 같은 것이 있을 때 resultList에 추가하는 함수
def matcher(list1, list2,resultList):
    l1len = len(list1)
    l2len = len(list2)
    #각 data들 간에 길이가 같은 가능성이 매우 낮기 때문에 for문을 두번 돌림.
    for i in range(l1len):
        if i< l2len:
            for j in range(len(list1[i])):
                for k in range(len(list1[i])):
                    if k <= len(list2[i])-1:
                        if list1[i][j] == list2[i][k]:
                            resultList.append(list1[i][j])
                        else:
                            break
        else:
            break

    for i in range(l2len):
        if i < l1len:
            for j in range(len(list2[i])):
                for k in range(len(list2[i])):
                    if k <= len(list1[i])-1:
                        if list2[i][j] == list1[i][k]:
                            resultList.append(list2[i][j])
                        else:
                            break
        else:
            break

#함수 실 사용 예시
chungS = open('./중앙일보/중앙일보정치.txt','rt',encoding='UTF8')
hanS = open('./한겨례/한겨례정치.txt','rt',encoding='ansi')
ytnS = open('./YTN/YTN정치.txt','rt',encoding='UTF8')
saegaeS = open('./세계일보/세계일보정치.txt','rt',encoding='UTF8')
gyungS = open('./경향신문/GHpoli.txt','rt',encoding='UTF8')

cTitle = []
hTitle = []
yTitle = []
sTitle = []
gTitle = []
result = []

titleReplacer(chungS,cTitle)
titleReplacer(hanS,hTitle)
titleReplacer(ytnS,yTitle)
titleReplacer(saegaeS,sTitle)
titleReplacer(gyungS,gTitle)

matcher(cTitle,hTitle,result)
matcher(cTitle,yTitle,result)
matcher(cTitle,sTitle,result)
matcher(cTitle,gTitle,result)
matcher(hTitle,yTitle,result)
matcher(hTitle,sTitle,result)
matcher(hTitle,gTitle,result)
matcher(yTitle,sTitle,result)
matcher(yTitle,gTitle,result)
matcher(sTitle,gTitle,result)


#같은 단어가 몇 번 나왔는지 체크하는 알고리즘
count={}
for i in result:
    try: count[i] +=1
    except: count[i]=1

#내림차순으로 재 정렬
sorted_dict = dict(sorted(count.items(), key=lambda x : x[1], reverse=True))
sorted_list = list(sorted_dict.keys())

#TOP 20개의 단어를 선택
semi_result = []
for i in range(20):
    semi_result.append(sorted_list[i])


#혹여나 같은 키워드가 있을 경우 제거를 위해 인덱스 체크
popindex=[]
for i in range(len(semi_result)):
    for j in range(len(semi_result)-1):
        if i == j : 
            continue
        else :
            if (semi_result[i] in semi_result[j]): 
                popindex.append(i)
                
            if (semi_result[j] in semi_result[i]):
                popindex.append(j)
    if len(semi_result[i])==1:
        popindex.append(i)
#중복된 인덱스를 제거하기 위해 자료형을 set으로 변경
pind = set(popindex)
removedList = []
for i in pind:
    removedList.append(semi_result[i])

for i in removedList:
    semi_result.remove(i)


final_result =[]
#상위 10개의 키워드를 리스트에 저장
for i in range(10):
    final_result.append(semi_result[i])

#출력
outputFileName = 'policyKeywords'
textFile = open(f'{outputFileName}.txt', 'w', encoding='utf-8')
for key_ in final_result:
    textFile.write(key_+"\n")
textFile.close()
print(final_result)

