from dashboard_notification.notification import Notification
from dashboard_api.api import DashboardAPI

CONFIG = {
    'dashboard_ip': '127.0.0.1',
    'dashboard_url': 'http://127.0.0.1',
    'api_token': 'f33ff43c85ecb13f5d0632c05dbb0a7d85a5a8d1',
    'user': 'opnfv',
    'password': 'opnfvopnfv'
}

api = DashboardAPI(CONFIG['dashboard_url'], api_token=CONFIG['api_token'], verbose=True)


def booking_start(message):
    content = message.content
    booking = api.get_booking(id=content['booking_id'])

    # do something here...

    # notify dashboard
    api.post_resource_status(resource_id=booking['resource_id'], type='info', title='pod setup',
                             content='details')


def booking_end(message):
    # do something here...

    # notify dashboard
    api.post_resource_status(resource_id=message.content['resource_id'], type='info',
                             title='booking end', content='details')


def main():
    with Notification(CONFIG['dashboard_ip'], CONFIG['user'], CONFIG['password']) as notification:
        notification.register(booking_start, 'Arm POD 2', 'booking_start')
        notification.register(booking_end, 'Arm POD 2', 'booking_end')
        notification.receive()  # wait for notifications


if __name__ == "__main__":
    main()
