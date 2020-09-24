# Atlas Dataset Manager
The inspiration for this project was to help manage the unwieldy process of creating and maintaining my foreign policy notes and citations dataset that I'm using to train a Natural Language Understanding & Generation model. 

While the input is relatively simple (a single article from a source I've deemed useful), its outputs are complex: first, every article needs to be classified into a taxonomy. To speed up the To assist with the creation of the taxonomy and ensure some degree of normalization, I've built a mapping visualization (with D3) to assist with the process that relies on vector similarity analysis. Second, I want to begin work on a summarization model that can identify a particular group within the taxonomy and summarize trends. Finally, I want to create a more advanced web scraper that is able to identify new sources of data beyond what I've manually added. 

## Current Capabilities (Version 0.0)
To start out, I've created a web scraper with BeautifulSoup and a simple Flask CMS that takes in a link and auto-fills the data I need for the first two data sections 1) citation data, 2) geographic data. For now, the addition and manipulation of the taxonomy data will be handled manually.

## Planned Releases
### 0.1 
Visualization of trends in the database. I'm simply taking some of the pivot tables I've made in my notebook and implementing them in my app through D3. 

### 0.2
Simple user interface that allows me to navigate and edit the relational database handling the article data, the geographic data, and the taxonomy data.

### 0.3
More complex user interface that leverages vector space embeddings and unsupervised clustering to create an interactive scatterplot with D3. 

### 1.0
Precision Control mechanism

### 2.0 
Automatic Summarization model 

### 3.0 
NLU-based Web Scraper 
