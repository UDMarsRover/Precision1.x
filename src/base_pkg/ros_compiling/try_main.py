#!/usr/bin/env python3

# Task: create a publisher to publish an array of random floating point values.
# create a subscriber to get the array and print it.
# Run using this file. may have to make it executable.
# Make publisher in try_publishing.py and subscriber in try_subscriber.py
# Use the dummy files for reference.

from try_publishing import FloatArrayPublisher as fap
from try_subscribing import FloatArraySubscriber as fas

if __name__ == '__main__':
    fap.publish() # haha, fap
    fas.subscribe()    