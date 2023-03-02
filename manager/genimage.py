
import httpx
import asyncio
from graia.ariadne.message.element import Image as GraiaImage
from typing import Union
from graia.ariadne.message import Source
from graia.ariadne.model import Friend, Group


async def get_generated_image(prompt: str, prefix: str):
    num_image = 1
    url = 'http://kwdl.xyz'
    port = 6003
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{url}:{port}/', json={'prompt': prompt[len(prefix):], 'width': 512, 'height': 512, 'num_images_per_prompt': 1})
        job_id = r.json()['job_id']
        while True:
            await asyncio.sleep(10)
            nr = await client.get(f'{url}:{port}/status/{job_id}')
            if nr.json()['status'] == 'Done':
                break
        # for image_id in range(num_image):
        #     print(image_id)
        #     mr = await client.get(f'{url}:{port}/{job_id}/{image_id}')
        #     with open(f'img-{job_id:05}-{image_id:03}.jpg', 'wb+') as f:
        #         f.write(mr.content)
        image_id = 0
        image_response = await client.get(f'{url}:{port}/{job_id}/{image_id}')
        return image_response

async def respond_generated_image(app, target: Union[Friend, Group], source: Source, config, response):
    return await app.send_message(target, GraiaImage(data_bytes=response.content),
                                  quote=source if config.response.quote else False)
    

def check_prefix(content, prefix_list):
    for prefix in prefix_list:
        if content.startswith(prefix):
            return prefix
    return None



if __name__ == '__main__':
    asyncio.run(get_generated_image())