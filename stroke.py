import cv2
import svgwrite
import numpy

def image_to_stroke(もとの画像, 出力画像パス):

    # 画像をうけとり、りんかくのSVG画像にして返す関数です

    画像 = numpy.array(もとの画像)

    if 画像.shape[2] == 3:
        画像 = numpy.dstack([画像, numpy.ones((画像.shape[0], 画像.shape[1]), dtype=画像.dtype) * 255])

    画像の不透明度 = 画像[:,:,3]

    透明な部分がある = numpy.any(画像の不透明度 == 0)

    if not 透明な部分がある:
        白い部分 = numpy.all(画像[:,:,:3] == [255, 255, 255], axis= -1)
        画像[白い部分, 3] = 0

    # 画像の透明ではない部分（イラストの部分）はすべて白にする
    画像[画像の不透明度 != 0] = [255, 255, 255, 255]

    # 画像の透明な部分はすべて黒にする
    画像[画像の不透明度 == 0] = [0, 0, 0, 255]

    # 白い部分のりんかくを取得する
    画像グレースケール = cv2.cvtColor(画像, cv2.COLOR_BGRA2GRAY)
    りんかくたち, _ = cv2.findContours(画像グレースケール, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # りんかくの情報をSVG形式にして保存する
    りんかくのSVGデータ = svgwrite.Drawing(出力画像パス, profile = "full")

    for りんかく in りんかくたち:
        点たち = [(int(点[0][0]), int(点[0][1])) for 点 in りんかく]
        りんかくのSVGデータ.add(りんかくのSVGデータ.polygon(点たち, fill="none", stroke = "black"))

    りんかくのSVGデータ.save()