# CS（顧客満足度）と、サービス項目（30項目）のCSポートフォリオ分析　
# 手順
# 1.  準備　環境設定
#     ワーキングディレクトリ指定、ライブラリのインポート
# 2.  CSスコア(Q9)、サービス項目(Q17_1～Q17_30まで30列）、FLAG（＝GATE、企業名）のデータ読み込み、データフレームを作る
# 3.  サービス項目　Q17_1～Q17_30について、それぞれ、平均点を算出する　全体＋FLAG（GATE）4社ごとに出力
# 4.  CS×サービス項目相関　
#　　 Q9（CS）列×Q17_1～Q17_30（サービス項目＝30列）の相関係数を順次算出、FLAG（GATE）ごとに計算
# 5.  全体＋FLAGごとに、相関係数、検定結果、サービス項目平均点のスコアをまとめ、一覧表を出力　サービス項目30個については、表示名を指定　
# 6.  作図
#　 　 x軸は相関係数、y軸はサービス項目平均点として、CSポートフォリオの図表（4象限）を作図　FLAG（GATE）ごとに4つの図出力
# 7.  統計検定（p値、判定基準）、一覧表にする


# 花店 顧客満足CSポートフォリオ分析 スクリプト 【全体】
# 1. 下準備　　
# CS は1＝1点～10＝10点
# CS総合満足度＝Q9の列（2023年）1～10点、10点が最高点、FLAG＝全４業態、回答者計500名


# ライブラリをインポート
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

from scipy.stats import pearsonr  
# Spearman順位相関係数を使う場合
from scipy.stats import spearmanr

from itertools import combinations

# グループ別集計用ライブラリ　インポート
from pandas.core.groupby.grouper import get_grouper


# CSポートフォリオ 
# 2. ローデータ読み込み
# ローデータのファイルを指定、日本語のエンコーディングはutf-8とする　YOUR_DATA.csv　の部分は自分のデータに
df23 = pd.read_csv("YOUR_DATA.csv", encoding='utf-8')  


# 3. 平均スコア = 図のy軸データ【全体】
q17_cols = [f"Q17_{i}" for i in range(1, 31)]

# Q17_1～Q17_30（列名・変数名）に、それぞれ表示名をつける
col_names = ["店頭情報提示", "明確な価格設定", "SNSでシェアしたくなる", "バラエティ","べーシックな商品が揃う","季節感","独自な商品","外れがなく安心","日持ち","鮮度","品質管理","少量でも買いやすい",
"色やサイズの選びやすさ","アクセスが便利","ついでに買える","買物がスムーズ","お買い得セール","新しい楽しみ方","イベント充実","清潔感","驚きや楽しさ","雰囲気がよい","スタッフのニーズ対応力","スタッフの応対", "スタッフのスキル", "選び方やケアの相談ができる", "特殊な要望やクレーム対応力",
"エコな花植物", "無駄やロス防止","スタッフが生き生きと働く"]

mean_scores = df23[q17_cols].mean()
mean_scores.index = col_names

# display(mean_scores)

q17_col_display_names = {
       
}


# 4. CS×サービス項目　相関係数＝図のx軸データ【全体】
correlations = {}
for col in q17_cols:
    coef, p_value = pearsonr(df23[col], df23["Q9"]) # Spearman順位相関係数の場合は、pearsonrをspearmanrに
    correlations[col] = coef
correlations = pd.Series(correlations)
correlations.index = col_names
# display(correlations)


# 5. 平均スコアと相関係数（各30項目）を、まとめて、Q17_1~Q17_30の項目別に、一覧表にする
summary_df = pd.DataFrame({"平均スコア": mean_scores, "相関係数": correlations})

# 表の出力
display(summary_df.round(3))

# print(summary_df.round(3).to_string())


# 6. 図の出力
# 図のタイトル＝ CSポートフォリオ　全体
# x軸タイトル ＝ CSとの相関
# y軸タイトル =  平均スコア

# 4象限で表示 x軸およびy軸で、それぞれ、中央値を基準に、正負の値を持つデータを分類して、それぞれ別の色やマーカーでプロットする

import numpy as np

import matplotlib as mpl
import matplotlib.font_manager as fm

# 日本語フォント 手動でインストール Windows  ファイルパスのスラッシュは正斜線を使う
font_path = "C:/Windows/Fonts/YuGothL.ttc"
font_prop = fm.FontProperties(fname=font_path, size=18)

# seabornのスタイル設定
sns.set_style("whitegrid")
sns.set_palette("pastel")  # 透明感のあるカラーパレットを設定

# フォントの設定
sns.set(font=font_prop.get_name())
sns.set_context("notebook", font_scale=1.7)


# 図のプロットの際、文字が重ならないようにするパッケージ　
!pip install adjustText
from adjustText import adjust_text  # adjustTextライブラリをインポート

# 平均スコア、CS相関係数ともに、30項目の中央値を境に、4象限に分ける
median_score = np.median(mean_scores)
median_correlation = np.median(correlations)

plt.figure(figsize=(30, 30))
scatter = plt.scatter(correlations[mean_scores >= median_score], mean_scores[mean_scores >= median_score], color='blue', label='High Score', marker='o')
scatter.set_alpha(0.6)  # 高スコア　データポイントの透明度を下げる

scatter = plt.scatter(correlations[mean_scores < median_score], mean_scores[mean_scores < median_score], color='red', label='Low Score', marker='x')
scatter.set_alpha(0.6)  # 低スコア　データポイントの透明度を下げる

plt.axhline(median_score, linestyle='--', color='gray')
plt.axvline(median_correlation, linestyle='--', color='gray')
plt.title("CSポートフォリオ", fontproperties=font_prop, fontsize=30)
plt.xlabel("CSとの相関", fontproperties=font_prop, fontsize=20)
plt.ylabel("平均スコア", fontproperties=font_prop, fontsize=20)

# 背景色を薄い桜色に設定
plt.gca().set_facecolor("#FFF7F3")

# 軸ラベルの背景色を透明に見せるために、白色のテキストエフェクトを追加する
plt.gca().xaxis.label.set_color('white')
plt.gca().yaxis.label.set_color('white')

# データラベル　列名の表示（col_names)　alpha指定でデータラベルの透明度とフォントサイズを調整
for label, x, y in zip(col_names, correlations, mean_scores):
    if x >= 0 and y >= 0:
        plt.annotate(label, xy=(x, y), xytext=(5, -5), textcoords="offset points", ha='left', va='bottom', fontproperties=font_prop, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))  
    elif x < 0 and y < 0:
        plt.annotate(label, xy=(x, y), xytext=(-5, 5), textcoords="offset points", ha='right', va='top', fontproperties=font_prop, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    else:
        plt.annotate(label, xy=(x, y), xytext=(5, 5), textcoords="offset points", ha='left', va='top', fontproperties=font_prop, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
           
plt.show()

# plt.legend() ← 凡例をつける場合
# 描画の外観は調整中　


# 7. 相関係数の検定（p値）、有意性判定基準【全体】
# 相関係数の検定
p_values = {}
for col in q17_cols:
    coef, p_value = pearsonr(df23[col], df23["Q9"]) # Spearman順位相関係数の場合は、pearsonrをspearmanrに
    p_values[col] = p_value

# 判定結果の定義
def significance(p_value):
    if p_value < 0.01:
        return "*** 1%水準で有意"
    elif p_value < 0.05:
        return "** 5％水準で有意"
    elif p_value < 0.1:
        return "* 10%水準で有意"
    else:
        return "n.s.（not significant）"

# 一覧表の作成
table = []
for col in q17_cols:
    p_value = p_values[col]
    table.append([col, f"{p_value:.3e}", significance(p_value)])

# 一覧表の出力
print("{:<10}{:<15}{:<30}".format("項目", "p値", "有意水準判定"))
for row in table:
    print("{:<10}{:<15}{:<30}".format(*row))
