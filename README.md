# TTA_C3
このリポジトリは、TTA-C3を操作するためのライブラリです。

従来は、以下の２つの課題がありました。
- xselパソコン対応ソフトというGUIを操作する必要があること
- 上記GUIの仕様で、事前に決められた動作しかさせられないこと

このライブラリでは、以下のことが可能です。
- pyautoguiを用いることにより、GUIを意識しなくてもpythonから直接TTA-C3を操作できる。

## 仮想環境のインストール
tta_c3ディレクトリで以下を実行
```shell
(Get-Content -Path "tta_c3.yml" -Encoding Default) -join "`n" `  | % { [Text.Encoding]::UTF8.GetBytes($_) } ` | Set-Content -Path "tta_c3.yml" -Encoding Byte
conda env create -f tta_c3.yml
```

## 仮想環境の更新(パッケージの追加/削除を反映)
```shell
conda env export -n house_price_kaggle > house_price_kaggle.yml
conda env update -f house_price_kaggle.yml
```