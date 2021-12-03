
import json
import requests
import schedule
import datetime
import numpy as np
from pytz import timezone    
from util.config import config,timeZone
from util.util import symbol_list
from kafka import KafkaProducer
from newsapi.newsapi_client import NewsApiClient




def kafka_producer_fake(producer,symbol):
    """
    send fake data to test visualization
    :param producer: (KafkaProducer) an instance of KafkaProducer with configuration written in config.py
    :return: None
    """
    
    close=4000
    close=close+np.random.uniform(-200,200)
    value={"symbol":symbol,
           "time":str(datetime.datetime.now(timezone(timeZone))),
           "open":close+np.random.uniform(-1,1),
           "high":close+np.random.uniform(0,1),
           "low":close+np.random.uniform(-1,0),
           "close":close,
           "volume":np.random.uniform(-1,1)*6e9}
    producer.send(topic=config['topic_name1'], value=bytes(str(value), 'utf-8'))
    print("Sent {}'s fake data.".format(symbol))







if __name__=="__main__":

    # init an instance of KafkaProducer
    producer = KafkaProducer(bootstrap_servers=config['kafka_broker'])
    #kafka_producer(producer)

    # schedule to send data every minute
    schedule.every(1).seconds.do(kafka_producer_fake,producer,'^GSPC')
     
    while True:
        schedule.run_pending()
    
    
    pass