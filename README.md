
##  簡介
* 此repository實現Craig Gentry等人提出的非對稱式加密演算法，此演算法的安全性為基於lattice base的困難問題，可以抵抗量子電腦破密攻擊。演算法詳細過程請見[此篇論文](https://eprint.iacr.org/2007/432)的7-1小節。  
* 由於基於lattice base的演算法有運算成本非常高的通病（因為有相當多的矩陣乘法），實務上請務必搭配其他高效演算法(例如AES128、AES256)使用。
* 此package會拿你電腦一半的CPU進行multiprocessing。
* library中所有矩陣乘法通通沒有用numpy，所以效率很差哦@@。

## 注意事項
* 開發版本：python 3.9.1
* 外部引用：\_\_future\_\_、random、multiprocessing、base64

## 如何使用

### 1. 生成公鑰、私鑰對
&emsp;&emsp;需要載入兩個module，其中Crypto包含加解密所需要的類別、並且config加解密中所需要的參數必須透過config進行設定。
```python
from  DualRegev.Cipher  import  Crypto
from  DualRegev.Config  import  config
```

<br>

&emsp;&emsp;安全參數設定中的n、m代表公鑰的大小，q代表模數。公鑰本身為n x m矩陣，因此設定時須特別注意，演算法的時間複雜度為O(n x m)，推薦100左右即可。q為一大質數，可取其值q = poly(n)。

```python
# 設定安全參數
config.set_parameter(n=128, m=256, q=16349)

# 生成公鑰、私鑰
key_obj  =  Crypto.LBDRKey().generate_key()
private_key  =  key_obj.extract_private_key()
public_key  =  key_obj.extract_key()

# 將公鑰、私鑰寫入檔案
with  open('sk.pem', 'wb') as  f:
	f.write(private_key)
with  open('pk.pem', 'wb') as  f:
	f.write(public_key)
```

<br>

### 2. 資料加密
 
&emsp;&emsp;加密方法中可接受的資料型態為bytes，由於加密密文的空間複雜度較大，package中提供converter針對不同的資料來源進行最佳的資料型態轉換。
 
```python
from  DualRegev.IO  import  Converter
```
<br>

&emsp;&emsp;加密過程如下，其中data訊息的資料型態不是bytes的話，必須使用Converter中相對應的方法將資料型態轉為bytes後才可進行加密，詳細請見 DualRegev/IO 的README.txt。。

```python
# 創建加密工具物件
crypto_obj  =  Crypto.LBDRCrypt() 

# 載入公鑰
with  open('pk.pem', 'rb') as  f:
	pk  =  f.read()
crypto_obj.import_key(pk)

# 加密訊息
data  =  '0x7c091f4c34ef21bac81f4d406f4e9cd1'
byte_data  =  Converter.hex_to_bytes(data)

enc_data  =  crypto_obj.encrypt(byte_data)

# 紀錄加密訊息
with  open('cipher_text.bin', 'wb') as  f:
	f.write(enc_data)
```
<br>

### 3. 資料解密
 
&emsp;&emsp;解密方法回傳的資料型態為bytes，使用Converter中相反的轉換方法即可把原文還原。
 
```python
# 創建加密工具物件
crypto_obj  =  Crypto.LBDRCrypt()

# 載入私鑰
with  open('sk.pem', 'rb') as  f:
	sk  =  f.read()
crypto_obj.import_key(sk)

# 讀取加密訊息
with  open('cipher_text.bin', 'rb') as  f:
	enc_data  =  f.read()

# 解密訊息
byte_data  =  crypto_obj.decrypt(enc_data)
data  =  Converter.bytes_to_hex(byte_data)
print(data)
```

<br>

&emsp;&emsp;print的結果：

```
>>> 0x7c091f4c34ef21bac81f4d406f4e9cd1
```
