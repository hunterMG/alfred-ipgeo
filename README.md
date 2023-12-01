# 🌍 Alfred-ipgeo

Another Alfred workflow to query an online GeoIP database for a specific IP address  or domain via HTML parsing instead of an API.

![img](./ipgeo-demo.jpg)

## 🚀 Features

- ISP info.
- List Multiple IP addresses of a domain if there were. 

## Requirements

- python3
- beautifulsoup4

## 👋 Usage

Download IPGeo.alfredworkflow from [Release](https://github.com/hunterMG/alfred-ipgeo/releases/) or the latest link below👇 then open it using Alfred to import.

[Latest download.](https://github.com/hunterMG/alfred-ipgeo/releases/latest/download/IPGeo.alfredworkflow)

It relies on `beautifulsoup4` now, which should be installed first:

```bash
/usr/bin/python3 -m pip install beautifulsoup4
```

Simply type your keyword into Alfred (default: `ipg`) and provide a query (IP/Domain) to see its infomation from an online GeoIP database.

If nothing is typed, your external IPv4 address will be displayed.

## ✅ Todos

- [x] Workflow configuration
- [ ] Default python3 package only(remove bs4 dependency for better disturbution)
- [ ] Alfred workflow gallery publish

## Ref

<https://github.com/wrjlewis/notion-search-alfred-workflow>
