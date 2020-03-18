import asyncio


class ClientServerProtocol(asyncio.Protocol):

    data_list = []

    def connection_made(self, transport):
        self.transport = transport

    @staticmethod
    def timestamp_check(timestamp, data):
        for i in ClientServerProtocol.data_list:
            if timestamp == int(i[2]) and data[0] == i[0]:
                i_index = ClientServerProtocol.data_list.index(i)
                ClientServerProtocol.data_list.remove(i)
                return ClientServerProtocol.data_list.insert(i_index, data)
            else:
                pass
        return ClientServerProtocol.data_list.append(data)

    @staticmethod
    def put(request):
        data = request[1:]
        try:
            data = [
                    data[0], str(float(data[1])), str(int(data[2]))
                    ]
            timestamp = int(data[2])
            ClientServerProtocol.timestamp_check(timestamp, data)
            return 'ok\n\n'
        except:
            return 'error\nwrong command\n\n'

    @staticmethod
    def get(request):
        necesarry_metrics = []

        for i in ClientServerProtocol.data_list:
            if request[1] == '*':
                necesarry_metrics.append(i)
            elif i[0] == request[1]:
                necesarry_metrics.append(i)

        if necesarry_metrics == []:
            return 'ok\n\n'

        final_str  = ''
        for i in necesarry_metrics:
            final_str += ' '.join(i) + '\n'

        answer = 'ok\n{}\n'.format(final_str)
        return answer

    @staticmethod
    def process_data(data):
        full_request = data.split('\n')

        if len(full_request) == 2 and full_request[0] != '':
            necesarry_method = full_request[0].split()[0]
            request = full_request[0].split()

            if necesarry_method == 'get' and len(request) == 2:
                return ClientServerProtocol.get(request)
            elif necesarry_method == 'put' and len(request) == 4:
                return ClientServerProtocol.put(request)
            else:
                return 'error\nwrong command\n\n'

        else:
            return 'error\nwrong command\n\n'

    def data_received(self, data):
        resp = ClientServerProtocol.process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
