import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Bar3D


st.set_page_config(page_title="Package Analysis", layout='wide')

class streamlitContainer :
    def container(self,input):
        with st.container():
            match input:
                case 1:
                    pass

                case 2:
                    self.left, self.right = st.columns(2)

                case 3:
                    self.left, self.middle, self.right = st.columns(3)

                case _: return

top = streamlitContainer()
top.container(2)
top.left.title("Kelompok 3 KDJK")
top.left.write("Anggota kelompok : ")
top.left.write("2210511087 - Diaz Saputra")
top.left.write("2210511087 - Diaz Saputra")
top.left.write("2210511087 - Diaz Saputra")
top.left.write("2210511087 - Diaz Saputra")

with top.right.status("Apa itu DDOS?"):
    st.write("DDOS attack atau Distributed Denial of Service merupakan serangan cyber dengan cara mengirimkan fake traffic atau lalu lintas palsu ke suatu sistem atau server secara terus menerus. Dampaknya, server tersebut tidak dapat mengatur seluruh traffic sehingga menyebabkan down.")
    st.write("Dalam prakteknya agar dapat menyerang suatu server, DDOS akan mengerahkan host dalam jumlah besar. Namun host yang dikerahkan tersebut adalah palsu, selanjutnya para hacker akan membanjiri lalu lintas server dengan host palsu tersebut. Sehingga ketika server berhasil dibanjiri oleh traffic hacker, dampaknya server akan lebih sulit diakses oleh host atau pengguna nyata.")
st.markdown("---")
st.header("Analisis data")
fileCheck = [f for f in os.listdir("./datasets")]
file = st.selectbox('Pilih file csv disini. (hanya tes menggunakan CICDS_Wednesday.csv)', fileCheck)
datasets = pd.read_csv("./datasets/"+file)

st.write("Isi dari file csv :")
st.write(datasets.head())


################################
st.header("Tipe DDOS : ")

dataPlot = datasets[[' Timestamp', ' Source IP',' Label']]
dataPlot = dataPlot.reset_index(names='Count')
dataDDOS = dataPlot[dataPlot[' Label'] != 'BENIGN']

dataDDOScount = dataDDOS.groupby(' Label')['Count'].agg(['sum','count'])
df_plot_count = dataDDOScount['count'].to_dict()
df_plot_sum = dataDDOScount['sum'].to_dict()

c = (
    Bar()
    .add_xaxis(list(df_plot_count.keys()))
    .add_yaxis("Count", list(df_plot_count.values()), category_gap="30%")
    .add_yaxis("Sum", list(df_plot_sum.values()), category_gap="30%")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="DDOS TYPE"))
    .render("bar_base.html")
)

HtmlFile = open("bar_base.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height = 500)


################################
st.header("3D BAR DDOS [Timestamp, DDOS, Packets] :")

df_plot_DDoS = dataDDOS.groupby(by=[' Timestamp', ' Label']).agg({'Count':'sum'})
print(df_plot_DDoS)
df_plot_DDoS = df_plot_DDoS.groupby([' Label',' Timestamp', 'Count']).size()
df_plot_DDoS_list = list(df_plot_DDoS.to_dict())

cb = (
    Bar3D()
    .add(
        "",
        [[d[1], d[0], d[2]] for d in df_plot_DDoS_list],
        xaxis3d_opts=opts.Axis3DOpts("", type_="category"),
        yaxis3d_opts=opts.Axis3DOpts("", type_="category"),
        zaxis3d_opts=opts.Axis3DOpts("", type_="value"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=4000000000),
        title_opts=opts.TitleOpts(title="Bar3D-Timestamp"),
    )
    .render("bar3d.html")
)
HtmlFile = open("bar3d.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height = 550)
