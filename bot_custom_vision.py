#!/usr/bin/env python

# Twitter Bot: Responding Bot

# This bot listens to the account @JakiToPtak.

import os
import pathlib
import requests
import time
import tweepy
import tensorflow as tf
import PIL
import psycopg2
import numpy as np
from database import init_db, read_mention_id_value, write_mention_id_value
from read_bird_list import read_scientific_name
import urllib.parse as urlparse

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = port)
print("Opened database successfully")

init_db(conn)

mentions_since_id = read_mention_id_value(conn)

CONSUMER_KEY = os.environ['api_key']
CONSUMER_KEY_SECRET = os.environ['api_secret_key']

ACCESS_TOKEN = os.environ['access_token']
ACCESS_TOKEN_SECRET = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


class Model:
    def __init__(self, model_filepath):
        self.graph_def = tf.compat.v1.GraphDef()
        self.graph_def.ParseFromString(model_filepath.read_bytes())

        input_names, self.output_names = self._get_graph_inout(self.graph_def)
        assert len(input_names) == 1
        self.input_name = input_names[0]
        self.input_shape = self._get_input_shape(self.graph_def, self.input_name)

    def predict(self, image_filepath):
        image = PIL.Image.open(image_filepath).resize(self.input_shape)
        input_array = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]

        with tf.compat.v1.Session() as sess:
            tf.import_graph_def(self.graph_def, name='')
            out_tensors = [sess.graph.get_tensor_by_name(o + ':0') for o in self.output_names]
            outputs = sess.run(out_tensors, {self.input_name + ':0': input_array})

        return {name: outputs[i] for i, name in enumerate(self.output_names)}

    @staticmethod
    def _get_graph_inout(graph_def):
        input_names = []
        inputs_set = set()
        outputs_set = set()

        for node in graph_def.node:
            if node.op == 'Placeholder':
                input_names.append(node.name)

            for i in node.input:
                inputs_set.add(i.split(':')[0])
            outputs_set.add(node.name)

        output_names = list(outputs_set - inputs_set)
        return input_names, output_names

    @staticmethod
    def _get_input_shape(graph_def, input_name):
        for node in graph_def.node:
            if node.name == input_name:
                return [dim.size for dim in node.attr['shape'].shape.dim][1:3]


def print_outputs(outputs):
    outputs = list(outputs.values())[0]

    labels = []
    labels_file = open('model/labels.txt', 'r')
    for label in labels_file.readlines():
        labels.append(label.strip())

    highest_score = np.max(outputs[0])
    first_class = labels[np.argmax(outputs[0])]
    first_class_scientific_name = read_scientific_name(first_class)
    #print(f"Specie {first_class} ({first_class_scientific_name}) with score of {highest_score}")

    second_highest = 0
    second_position = -1
    for i, score in enumerate(outputs[0]):
        if score > second_highest and score < highest_score:
            second_highest = score
            second_position = i

    second_class = labels[second_position]
    second_class_scientific_name = read_scientific_name(second_class)
    #print(f"Specie {second_class} ({second_class_scientific_name}) with score of {second_highest}")

    third_highest = 0
    third_position = -1
    for i, score in enumerate(outputs[0]):
        if score > third_highest and score < second_highest:
            third_highest = score
            third_position = i

    third_class = labels[third_position]
    third_class_scientific_name = read_scientific_name(third_class)
    #print(f"Specie {third_class} ({third_class_scientific_name}) with score of {third_highest}")

    if highest_score > 0.5:
        return "{} ({}).".format(first_class, first_class_scientific_name)
    elif highest_score > 0.2:
        return "Podria ser {} ({}) ?".format(first_class, first_class_scientific_name)
    else:
        return "No el puc identificar bé."

def process_image(filename):
    print("Processing image " + filename)
    image_path = pathlib.Path(filename)

    outputs = model.predict(image_path)
    
    return print_outputs(outputs)

def download_image(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as file:
        file.write(response.content)

    return filename

def check_mentions(api, mentions_since_id):
    new_mentions_since_id = mentions_since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=mentions_since_id).items():
        new_mentions_since_id = max(tweet.id, new_mentions_since_id)

        #print(tweet)
        # get all the images for each tweet
        try:
            images = tweet.extended_entities['media']

            reply_message = "@" + tweet.user.screen_name
            
            for i, img in enumerate(images, start = 1):
                # Download image
                filename = download_image(img['media_url'])

                # Process image
                prediction_message = process_image(filename)
                reply_message = reply_message + "\n" + str(i) + ". " + prediction_message

                # Delete downloaded image
                os.remove(filename)

            # Reply
            print(reply_message)
            api.update_status(reply_message, tweet.id)
        except Exception as e:
            print(e)

    return new_mentions_since_id


model_filepath = pathlib.Path('model/model.pb')
model = Model(model_filepath)
print("model loaded, script up and running...")

while True:
    try:
        new_mentions_since_id = check_mentions(api, mentions_since_id)

        if new_mentions_since_id > mentions_since_id:
            write_mention_id_value(conn, new_mentions_since_id)
            mentions_since_id = new_mentions_since_id

        time.sleep(5)

    except Exception as e:
        print(e)
        conn.close()

