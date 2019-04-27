# crawl-mobilephone
install scrapy:
- run: pip install Scrapy 
crawl data:
- cd project_path
- run: scrapy crawl fpt -o fpt.json && scrapy crawl hoangha -o hoangha.json && scrapy crawl thegioididong -o thegioididong.json 
