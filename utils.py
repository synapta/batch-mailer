import asyncio
import httpx

"""
Utils functions to manage attachments
"""

async def request_header(client, url):
    print('    Get attachment header: %s' % url)
    res = None
    try:
        response = await client.head(url)
        res = response.headers
    except Exception as err:
        res = 'Errore'
        print('    %s' % str(err))
    
    return {'url': url, 'response': res}


async def request(client, url):
    print('    Get attachment: %s' % url)
    res = None
    file_name = None
    try:
        res = await client.get(url)
        headers = res.headers
        file_name = get_name_from_url(url)
        open(file_name, 'wb').write(res.content)
    except Exception as err:
        headers = 'Errore'
        print('    %s' % str(err))
    
    return {'url': url, 'file_name': file_name, 'response': res.status_code}


async def multi_requests(urls, req_func):
    async with httpx.AsyncClient() as client:
        tasks = [req_func(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        return results


def get_name_from_url(url):
    return url.split('/')[-1]
    