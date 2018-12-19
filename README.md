Narou_Analytics

scrayping.py 
なろうのランキングページのURLを引数として渡すと、その一覧から小説情報を取り出してJSONデータに吐き出します。
また、推奨作品を対象に入れることができ、そこからそこで推奨されている作品を対象に入れることで再帰的に作品を抽出できます。

引数: 第一引数、ランキングページのURL　第二引数、推奨作品からその推奨作品を対象にいれる際の深度を数値で与えられます。

e.g. python scraping.py https://yomou.syosetu.com/rank/genrelist/type/daily_201/ 0

python version 3.5.3

required library

#pip install requests

#pip install beautifulsoup4

#pip install lxml
