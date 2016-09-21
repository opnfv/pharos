import json
import re

import pika


class Notification(object):
    """
    This class can be used by the dashboard and the labs to exchange notifications about booking
    events and pod status. It utilizes rabbitmq to communicate.

    Notifications are associated to an event and to a topic.
    Events are:
    [ 'booking_start', 'booking_stop', 'pod_status' ]
    The topic is usually a POD name, ie:
    'Intel POD 2'
    """

    def __init__(self, dashboard_url, verbose=False):
        self.rabbitmq_broker = dashboard_url
        self.verbose = verbose
        self._registry = {}

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.rabbitmq_broker))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='notifications', type='topic')

        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

    def register(self, function, event, regex):
        """
        Registers a function to be called for the specified event.
        :param function: the function to register
        :param event: the event type
        :param regex: a regex to specify for wich topics the function will be called. Some
        possible Expressions can be:
        'Intel POD 2' : Intel POD 2
        'Intel POD .*' : All Intel Pods
        '.*' : All Topics
        """

        if event not in self._registry:
            self._registry[event] = [(function, regex)]
        else:
            self._registry[event].append((function, regex))

    def receive(self):
        """
        Start receiving notifications. This is a blocking operation, if a notification is received,
        the registered functions will be called.
        """
        if self.verbose:
            print('Start receiving Notifications. Keys: ', self._registry.keys())
        self._receive_message(self._registry.keys())

    def send(self, event, topic, content):
        """
        Send an event notification.
        :param event: the event type
        :param topic: the pod name
        :param content: a JSON-serializable dictionary
        """
        message = {
            'event': event,
            'topic': topic,
            'content': content
        }
        self._send_message(message)

    def _send_message(self, event):
        routing_key = event['type']
        message = json.dumps(event)
        self.channel.basic_publish(exchange='notifications',
                                   routing_key=routing_key,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       content_type='application/json'
                                   ))
        if self.verbose:
            print(" [x] Sent %r:%r" % (routing_key, message))

    def _receive_message(self, binding_keys):
        for key in binding_keys:
            self.channel.queue_bind(exchange='notifications',
                                    queue=self.queue_name,
                                    routing_key=key)
        self.channel.basic_consume(self._message_callback,
                                   queue=self.queue_name,
                                   no_ack=True)
        self.channel.start_consuming()

    def _message_callback(self, ch, method, properties, body):
        if self.verbose:
            print(" [x] Got %r:%r" % (method.routing_key, body))
        if method.routing_key not in self._registry:
            return
        for func, regex in self._registry[method.routing_key]:
            message = json.loads(body.decode())
            match = re.match(regex, message['topic'])
            if match:
                func(body)
