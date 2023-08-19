import asyncio

class MentatRunner:
    _interrupted = False
    def __init__(self):
        pass
    
    async def get_response(self, data: str, stream_handler: callable):
        response = f'Responding to {data}'
        stream_handler('@@startstream')
        for char in response:
            stream_handler(char)
            if self._interrupted:
                self._interrupted = False
                return stream_handler('@@endstream')
            await asyncio.sleep(0.2)
        return stream_handler('@@endstream')
    
    def interrupt(self):
        self._interrupted = True
    
    def restart(self):
        return 'Restarting'