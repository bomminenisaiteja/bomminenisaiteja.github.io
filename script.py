import requests
import lxml.html as lh
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
from plotly.subplots import make_subplots



url="https://www.mohfw.gov.in/"
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
col=[]
i=0
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print('%d:"%s"'%(i,name))
    col.append((name,[]))
for j in range(1,len(tr_elements)):
    T=tr_elements[j]
    if len(T)!=5:
        break
    i=0
    for t in T.iterchildren():
        data=t.text_content()
        if i>0:
            try:
                data=int(data)
            except:
                pass
        col[i][1].append(data)
        i+=1
Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
df=df.rename(index=str,columns={df.columns[2]:"CONFIRMED"})
df=df.rename(index=str,columns={df.columns[3]:"RECOVERED"})
df=df.rename(index=str,columns={df.columns[4]:"DECEASED"})
df=df.rename(index=str,columns={df.columns[1]:"STATE/UT"})


fig8 = go.Figure(
    data=[
        go.Bar(
            name="CONFIRMED",
            x=df["STATE/UT"],
            y=df["CONFIRMED"],
            offsetgroup=1,
        ),
        go.Bar(
            name="RECOVERED",
            x=df["STATE/UT"],
            y=df["RECOVERED"],
            offsetgroup=1,
        ),
        go.Bar(
            name="DECEASED",
            x=df["STATE/UT"],
            y=df["DECEASED"],
            offsetgroup=1,
        )
    ],
    layout=go.Layout(
        title="COVID19",
        yaxis_title="CASES"
    )
)
html = df.to_html()
fig=fig8.to_html()
with open("file.html", "w") as file:
    file.write(html)
with open("file2.html","w") as file2:
    file2.write(fig)
data = data2 = ""

# Reading data from file1
with open('file.html') as fp:
    data = fp.read()

# Reading data from file2
with open('file2.html') as fp:
    data2 = fp.read()

# Merging 2 files
# To add the data of file2
# from next line
data += "\n"
data += data2

with open('index.html', 'w') as fp:
    fp.write(data)