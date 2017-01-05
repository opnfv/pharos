##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import jsonpickle
import pika


class Message(object):
    def __init__(self, type, topic, content):
        self.type = type
        self.topic = topic
        self.content = content


class Notification(object):
    """
    This class can be used by the dashboard and the labs to exchange notifications about booking
    events and pod status. It utilizes rabbitmq to communicate.

    Notifications are associated to an event and to a topic.
    Events are:
    [ 'booking_start', 'booking_end']
    The topic is usually a POD name, ie:
    'Intel POD 2'
    """

    def __init__(self, dashboard_url, user=None, password=None, verbose=False):
        self.rabbitmq_broker = dashboard_url
        self.verbose = verbose
        if user is None and password is None:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.rabbitmq_broker))
        else:
            self.credentials = pika.PlainCredentials(user, password)
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(
                credentials=self.credentials,
                host=self.rabbitmq_broker))
        self._registry = {}
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange='notifications', type='topic')
        self._result = self._channel.queue_declare(exclusive=True, durable=True)
        self._queue_name = self._result.method.queue

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def register(self, function, topic, type='all'):
        """
        Registers a function to be called for the specified event.
        :param function: the function to register
        :param event: the event type
        :param regex: a regex to specify for wich topics the function will be called. Some
        possible Expressions can be:
        'Intel POD 2' : Intel POD 2
        """

        if topic not in self._registry:
            self._registry[topic] = [(function, type)]
        else:
            self._registry[topic].append((function, type))

    def receive(self):
        """
        Start receiving notifications. This is a blocking operation, if a notification is received,
        the registered functions will be called.
        """
        if self.verbose:
            print('Start receiving Notifications. Keys: ', self._registry.keys())
        self._receive_message(self._registry.keys())

    def send(self, message):
        """
        Send an event notification.
        :param event: the event type
        :param topic: the pod name
        :param content: a JSON-serializable dictionary
        """
        self._send_message(message)

    def _send_message(self, message):
        routing_key = message.topic
        message_json = jsonpickle.encode(message)
        self._channel.basic_publish(exchange='notifications',
                                    routing_key=routing_key,
                                    body=message_json,
                                    properties=pika.BasicProperties(
                                        content_type='application/json',
                                        delivery_mode=2,  # make message persistent
                                    ))
        if self.verbose:
            print(" [x] Sent %r:%r" % (routing_key, message_json))

    def _receive_message(self, binding_keys):
        for key in binding_keys:
            self._channel.queue_bind(exchange='notifications',
                                     queue=self._queue_name,
                                     routing_key=key)
        self._channel.basic_consume(self._message_callback,
                                    queue=self._queue_name)
        self._channel.start_consuming()

    def _message_callback(self, ch, method, properties, body):
        if self.verbose:
            print(" [x] Got %r:%r" % (method.routing_key, body))
        if method.routing_key not in self._registry:
            return
        for func, type in self._registry[method.routing_key]:
            message = jsonpickle.decode(body.decode())
            if message.type == type:
                func(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
