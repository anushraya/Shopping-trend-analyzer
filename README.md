# Social Media Trend Analysis

A project which aims to analyse past as well as realtime trends from social media comprehensively, to give an overall idea of the product and sales patterns. It is intended to assist in prediction of future sales and potential products.

It is a cross platform solution with ability to visualise and handle large amounts of data at ease, without failing.

## Setup

### Installing and Configuring Elasticsearch

The Elasticsearch components are not available in Ubuntu’s default package repositories. They can, however, be installed with APT after adding Elastic’s package source list.

    curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch |sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg

Next, add the Elastic source list to the `sources.list.d` directory, where APT will search for new sources:

    echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

Next, update your package lists so APT will read the new Elastic source

    sudo apt update

Then install Elasticsearch with this command:

    sudo apt install elasticsearch

Start the Elasticsearch service with `systemctl`. Give Elasticsearch a few moments to start up. Otherwise, you may get errors about not being able to connect.

    sudo systemctl start elasticsearch

### Installing and Configuring the Kibana Dashboard

    sudo apt install kibana

Then start the Kibana service:

    sudo systemctl start kibana

### Installing Python dependencies and API Keys

Install the required dependencies using the following command after cloning the repo locally.

```python
pip install -r ./requirements.txt
```

Create a `.env` file and copy paste the following code into it - 

    consumer_key='<your twitter developer account API key>'
    
    consumer_secret='<your twitter developer account consumer key>'
    
    access_token='<your twitter developer account access token>'
    
    access_token_secret='<your twitter developer account token scret>'
    
    bearer_token='<your twitter developer account bearer token>'
    
    username='<your instagram account username>'
    
    password='<your instagram account password>'

## Execution

For fetching and analysing data from twitter, run:

    python3 ./twitter_data.py


And for fetching and analysing instagram data, run:   

    python3 ./instagram_data.py


To analyse and visualize, open `http://localhost:5601/` on your browser for the Kibana dashboard.
