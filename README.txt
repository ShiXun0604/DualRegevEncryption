Abstract：
    * 此library採用Craig Gentry等人在2007年提出的非對稱式加密演算法，此演算法的安全性為基於lattice base的困難問題，可以抵抗量子電腦破密攻擊。演算法詳細過程請見此篇論文的7-1小節。
    https://eprint.iacr.org/2007/432
    * 由於基於lattice base的演算法的通病就是加解密運算成本非常高，實務上請務必搭配其他高效演算法(例如AES128、AES256)使用。
    * 作者為了練習程式技巧，library中所有矩陣乘法都沒有使用numpy，所以效率很差哦ㄎㄎ。

開發版本：
    python 3.9.1


外部引用：
    __future__、random、multiprocessing、base64


注意事項：
    1. 請把DualRegev放入site-package內或是path找的到的地方。
    2. 為了優化加密效率，對於待加密訊息的資料型態轉換請閱讀DualRegev/IO/README.txt的指引進行資料型態轉換。