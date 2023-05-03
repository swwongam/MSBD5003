git pull
databricks fs cp "dbfs:/dash_pie_top10.csv" "data"
databricks fs cp "dbfs:/dash_community.csv" "data"
git add .
git commit -m "File updates"
git push
