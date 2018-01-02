# Coptic Project Web Scrapers

This project contains scripts that scapes content from the Coptic web sites to extract resources and prepare them to be displayed on the [Coptic Project Portal](http://www.copticproject.com).

## Folder Structure


### `/settings.json`

This file is a template for scraping settings. The actual file in production will have a reference to selenium server, and the target path to store CSV files. 

### `/lib`

Contains the common libraries used by all scrapers.

### `/scrapers/<<uploader>>/<<site>>/<<content type>>`

Every python script  will follow this path pattern. Where _uploader_ is the owner of the media being scraped, _site_ is which portal is being scraped in case the uploader have more than one, and the _content type_ is one of the values: (sermons, books, hymns or songs).

Inside the leaf folder, the python script can be named as desired. As an example if there is only ony file, the name _scraper_ would make sense. In case there are several scripts for each author for example, it would make sense to name each script after the author's name.