# To set up the development environment

```shell
git clone <repo url> && cd capstone
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## There are two modes to run this in

```shell
python scraper.py sites.txt
```
will run the scraper in a single thread sequentially. This is good for debugging. 

```shell
python scraper.py sites.txt --threaded
```
adds multithreading support to drastically speed things up. This is non-sequential. 