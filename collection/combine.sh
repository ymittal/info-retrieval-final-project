#!/bin/sh
cat *_en > combined/ted.en
sed -i '/^$/d' combined/ted.en
cat *_zh-CN > combined/ted.zh_cn
sed -i '/^$/d' combined/ted.zh-CN
cat *_ar > combined/ted.ar
sed -i '/^$/d' combined/ted.ar
