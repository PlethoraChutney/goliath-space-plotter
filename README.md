# Goliath space monitor
I suppose this is generally useful, but it was written for Goliath at OHSU.

This script converts the output of du to a
[sunburst plot](https://plotly.com/python/sunburst-charts/).

Run
```
du --max-depth 2 /goliath/processing/lab1 /goliath/rawdata/lab1 > /path/to/script/du-out.txt
python goliath_monitor.py du-out.txt
cp du-out.txt /somewhere/public/for/other/uses/du-out.txt
cp goliath-du.csv /somewhere/public/for/other/uses/goliath-du.csv
```

as a cron job, with the necessary environment modifications (or full paths to everything). Then point some url to the html file generated by the script.