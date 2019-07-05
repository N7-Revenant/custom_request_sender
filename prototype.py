import http.client


class Request:
    def __init__(self, req_title, req_type, req_path):
        self.title = req_title
        self.type = req_type
        self.path = req_path


requests = {
    '1': Request('send del', 'DELETE', '/test'),
    '2': Request('send post', 'POST', '/test')
}

input_help = ["0: exit application"] + ['%s: %s' % (key, requests[key].title) for key in requests]


command_id = ''
while command_id != '0':
    print(*input_help, sep='\n')
    command_id = input('Select command: ')
    if command_id in requests:
        connection = http.client.HTTPConnection(host='localhost', port=8888)
        req_settings = requests[command_id]
        connection.request(req_settings.type, req_settings.path)
        response = connection.getresponse()
        print("Status: {} and reason: {}".format(response.status, response.reason))
        print("Response body:", response.read().decode(), sep='\n')
        connection.close()
    else:
        if command_id != '0':
            print("Unknown command code!")
else:
    print("'0' selected, exiting application...")
