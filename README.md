# ProCon2018-Solver

これは第29回高専プロコンのソルバです。

## 依存
- wxPython
- NumPy
- (QRコード読み取り用↓)
- pyzbar
- pillow
- ZBarを以下よりダウンロード、インストール
- http://zbar.sourceforge.net/download.html-
- (機械学習用↓)
- tensorflow-gpu 1.4
- keras
- CUDA 8.0
- cudnn 6.0

### 導入
 ``` $ pip install wxpython numpy ```

### anaconda学習用仮想環境作成
 ``` 
 $ conda create -n procon2018 python=3.6
 $ activate procon2018
 $ pip install wxPython numpy
 $ pip install "tensorflow-gpu==1.4"
 $ pip install keras ```
