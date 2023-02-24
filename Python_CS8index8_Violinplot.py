#Pythonで、顧客満足関連指標は８つある　それぞれの指標について、調査対象4社（4水準）のスコアの分布を可視化するため、バイオリンプロット（図表）を作る
#プロットは、８指標それぞれについて、4社をひとかたまりにまとめて、for文で連続的に出力する　
#使用環境　Python3、Jupyter Notebook　場合によってはDocker、Ubutu　

#1 準備
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 日本語フォントをインストールする
!pip install japanize-matplotlib

import matplotlib.pyplot as plt
import japanize_matplotlib  # 日本語フォントを使用するためにimportする

plt.rcParams['font.family'] = 'IPAexGothic' #フォント名を指定

# Dockerで作業する場合
# Dockerfile側に、下記のパッケージをインストールする
# RUN pip install pandas
# RUN pip install seaborn
# RUN pip install matplotlib


#2 ファイル読み込み
#CSVファイルのパス  .....の部分には、ローデータのcsvファイルへのパスを入力する

file_path = "C:\\Users\\....csv"

#そのパスで、そのファイルが存在しているかどうか、確認
import os  
print(os.path.exists(r"C:\Users\........csv"))

#Windowsの日本語フォントがShift-JISになっているなどの理由で、FileNotFoundエラーになる可能性
#その場合、エスケープシーケンスを無効化するために、上記のようにr（raw文字）を使うか、ディレクトリの区切りを、\\（￥￥半角）にするか、/（スラッシュ）にする　

#df＝データフレームとして、CSVファイルの読み込み 日本語フォントが入っているために文字コードを指定
df = pd.read_csv(file_path, encoding="utf-8")



#3　CS指標（8つ）と、企業名（FLAG）4社のデータを読み込み、オブジェクトにする
# CS指標として、Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16　以上8列を読み込み、questions というデータフレームにまとめる
questions = ["Q9", "Q10","Q11","Q12","Q13", "Q14","Q15","Q16"]

# FLAGの値　4水準あり　FLAGは、対象4社の企業名のデータ
flags = df["FLAG"].unique()


#4　バイオリンプロット描画
# 辞書で出力名を定義　列名（Q9～Q16）に、指標名を対応させ、図表には指標名を使って、順番に描画する準備
q_names = {"Q9": "総合満足度", "Q10": "ニーズ充足", "Q11": "品質評価", "Q12": "コスパ評価", "Q13": "情緒的充足", "Q14": "継続利用意向", "Q15": "共感愛着", "Q16": "推奨意向"}

# バイオリンプロット作成　for文で、順番に自動描画
colors = {'日比谷花壇': 'blue', '青フラ': 'red', 'イオン': 'magenta', 'ユニクロ': 'green'}
for question in questions:
    # 図を作成
    fig, ax = plt.subplots(figsize=(20, 5))
    fig.suptitle(q_names[question], fontsize=18)
    
    # 全てのFLAGのデータを結合してバイオリンプロットを作成する
    data = pd.concat([df[df["FLAG"] == flag][question] for flag in flags], axis=1)
    data.columns = flags
    sns.violinplot(data=data, inner="stick", palette=colors, ax=ax)
    
    # 軸ラベル等の設定
    ax.set_xlabel("", fontsize=14)
    ax.set_ylabel("スコア", fontsize=14)
    ax.set_ylim(0, 10)
    
    # X軸の設定
    ax.xaxis.labelpad = 20 # X軸ラベルのスペースを調整
    ax.tick_params(axis='x', which='major', labelsize=14) # X軸のラベルのフォントサイズを設定
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=18) # X軸のラベルのフォントサイズを設定
        
    plt.show


# 5　図の保存　図をファイルに保存　作業ディレクトリに保存される　軸名は付かないので注意
    plt.savefig(question + '.png')
    
    plt.show()
