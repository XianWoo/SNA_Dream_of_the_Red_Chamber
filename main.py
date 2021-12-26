import pandas as pd
from pyecharts.charts import Graph
from pyecharts import options as opts
import jieba
import jieba.posseg as pseg
import matplotlib.pyplot as plt

def deal_data():
    with open("红楼梦.txt", encoding='gb18030') as f:
        honglou = f.readlines()

    renwu_data = pd.read_csv("renwu_total")
    mylist = [k[0].split(" ")[0] for k in renwu_data.values.tolist()]
   
    tmpNames = []
    names = {}
    relationships = {}
    for h in honglou:
        poss = pseg.cut(h)
        tmpNames.append([])
        for w in poss:
            if w.word =='林黛玉' or w.word == '林妹妹' or w.word == '林姑娘':
                w.word = '黛玉'
            if w.word =='贾宝玉' or w.word == '宝二爷':
                w.word = '宝玉'
            if w.word =='薛宝钗' or w.word == '宝姐姐' or w.word == '宝丫头' or w.word == '宝姑娘':
                w.word = '宝钗'    
            if w.word =='王熙凤' or w.word =='凤辣子' or w.word == '琏二奶奶' or w.word == '凤姐':
                w.word = '凤姐'
            if w.word =='珍大奶奶':
                w.word = '尤氏'
            if w.word == '惜春' or w.word == '四姑娘':
                w.word = '贾惜春'
            if w.word == '秦氏' or w.word == '蓉大奶奶':
                w.word = '秦可卿'
            if w.word == '史太君' or w.word == '老祖宗' or w.word =='老太太':
                w.word = '贾母'
            if w.word == '娘娘' or w.word == '贾妃':
                w.word = '贾云春'
            if w.word == '二姑娘' or w.word == '迎春':
                w.word = '贾迎春'
            if w.word == '三姑娘' or w.word == '探春':
                w.word = '贾探春'
            if w.word == '宫裁' or w.word == '李宫裁':
                w.word = '李纨'
            if w.word == '史大姑娘':
                w.word = '史湘云'
            if w.word == '姨太太':
                w.word = '薛姨妈'




            if w.flag != 'nr' or len(w.word) < 2 or w.word not in mylist:
                continue
            tmpNames[-1].append(w.word)
            if names.get(w.word) is None:
                names[w.word] = 0
            relationships[w.word] = {}
            names[w.word] += 1
    #print(relationships)
    #print(tmpNames)
    for name, times in names.items():
        print(name, times)


    for name in tmpNames:
        for name1 in name:
            for name2 in name:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] += 1
    print(len(relationships))
    with open("relationship.csv", "w", encoding='utf-8') as f:
        f.write("Source,Target,Weight\n")
        for name, edges in relationships.items():
            for v, w in edges.items():
                f.write(name + "," + v + "," + str(w) + "\n")

    with open("NameNode.csv", "w", encoding='utf-8') as f:
        f.write("ID,Label,Weight\n")
        for name, times in names.items():
            f.write(name + "," + name + "," + str(times) + "\n")


def deal_graph():
    relationship_data = pd.read_csv('relationship.csv')
    namenode_data = pd.read_csv('NameNode.csv')
    relationship_data_list = relationship_data.values.tolist()
    namenode_data_list = namenode_data.values.tolist()

    nodes = []
    for node in namenode_data_list:
        if node[0] == "宝玉":
            node[2] = node[2]/3
        nodes.append({"name": node[0], "symbolSize": node[2]/30})
    links = []
    for link in relationship_data_list:
        links.append({"source": link[0], "target": link[1], "value": link[2]})

    g = (
        Graph()
        .add("", nodes, links, repulsion=7000)
        .set_global_opts(title_opts=opts.TitleOpts(title="红楼人物关系"))
    )
    return g


if __name__ == '__main__':
    deal_data()
    g = deal_graph()
    g.render()
