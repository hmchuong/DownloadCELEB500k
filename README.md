# DownloadCELEB500k
Download Celeb500k with Scrapy

## Requirements
- Python >= 3.5

## Install dependencies
- Scrapy
- Pillow
```
pip install scrapy Pillow
```

## Download url files
Download url files to `data` folder following the [instruction inside](data/README.md).

## Start downloading
Run the following command
```
sh crawl.sh 5
```
where 5 is the number of retries, you should run 5-10 times to get all images

## Results
Run the following command to get the number of download folders
```
ls -1 data/images/<url part> | wc -l
```

Run the following command to get the number of downloaded images
```
wc -l data/images/<url part>.jl
```