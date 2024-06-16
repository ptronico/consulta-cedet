import json
import rich
import fire
import asyncio
import aiohttp


bookstores_domains = [
  'livrariaib.com',
  'livrariadobernardo.com',
  'livrariabrunatorlay.com.br',
  'livrariaalexandrecosta.com.br',
  'livrariaguilhermefreire.com.br',
  'livraria.seminariodefilosofia.org',
  'livraria.deiaetiba.com.br',
  'livraria.daniellopez.com.br',
  'livrariacampagnolo.com.br',
  'livrariadobene.com.br',
  'livrariadorobertomotta.com.br',
  'livrariabsm.com.br',
  'livrariadonikolas.com',
  'livrariadamarcela.com.br',
  'livrariadopadrewander.com.br',
  'livrariadothomas.com.br',
  'livrariadaaraceli.com.br',
  'livrariavistapatria.com.br',
  'livraria.rodrigogurgel.com.br',
  'livrariacazarre.com.br',
  'livrariadosaulo.com.br',
  'livrariavictorsales.com.br',
  'mariebrunobookshop.com.br',
  'livrariabrodbeck.com.br',
  'afilivraria.com.br',
  'livrariaamandabuttchevits.com.br',
  'livrariadoconsta.com.br',
  'livrariateatualizei.com.br',
  'livrariadoalam.com.br',
  'bibliotecadoluiz.com.br',
  'livraria.sensoincomum.org',
  'livrariasantacarona.com.br',
  'livrariadamarize.com.br',
  'livrariadolacombe.com.br',
  'livrariapriantunes.com.br',
  'livrariacontraosacademicos.com.br',
  'livrariasabedoriacatolica.com.br',
  'livraria.paulamarisa.com.br',
  'livrariadanuzioneto.com.br',
  'livrariaanaderosa.com.br',
  'livrariachestertonbrasil.com.br',
  'livrariadapietra.com.br',
  'livrariapedroaugusto.com.br',
  'livrariadoutorpacheco.com.br',
  'livrariaeduardobolsonaro.com.br',
  'livrariacazarre.com.br',
  'livrariacep.com.br',
  'livrariapaulokogos.com.br',
  'livrariazapparoli.com.br',
  'livrariaborasersanto.com.br',
  'livrariadacassia.com.br',
  'livrariadafran.com.br',
  'livrariadorasta.com.br',
  'livrariadaprof.com.br',
  'livrariaheroisemais.com.br',
  'livrariaedmilsoncruz.com.br',
  'livrariarebelo.com.br',
  'livrariadjessi.com.br',
  'livraria.cooperadoresdaverdade.com',
  'livrariadaamanda.com.br',
  'livrariapadrediogo.com.br',
  'livrariacatolikids.com.br',
  'livrariadopadrelucas.com.br',
  'livrariazanette.com.br',
  'livrariadajulia.com.br',
]


async def fetch(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url, timeout=10) as response:
            return json.loads(await response.text())
    except asyncio.exceptions.TimeoutError as exc:
        # print(exc)
        return ''
    except aiohttp.client_exceptions.ClientConnectionError as exc:
        # print(f'ClientConnectionError: {exc}')
        return ''
    except json.decoder.JSONDecodeError as exc:
        # print(f'JSONDecodeError: {exc}')
        return ''


async def fetch_all(urls_domains, book_name='bitcoin'):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        tasks = []
        for url_domain in urls_domains:
            url = f'https://{url_domain}/index.php?route=product/search/autocompleteprod&prod={book_name}'
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


async def main(book_name):
    data = {}
    responses = await fetch_all(bookstores_domains, book_name=book_name)
    for response in responses:
        if type(response) is not dict:
            continue
        for produto in response['produtos']:
            if produto['name'] not in data:
                data[produto['name']] = []
            cleaned_produt = {}
            price_str = produto['price'] if type(produto['special']) is bool else produto['special']
            data[produto['name']].append({
                'special': price_str,
                'name': produto['name'],
                'href': produto['href'],
                'amount': float(price_str.replace('R$ ', '').replace(',', '.')),
            })
    keys = []
    for name, options in data.items():
        rich.print(f'[bold yellow]{name.upper()}[/bold yellow]')
        sorted_options = sorted(options, key=lambda d: d['amount'])
        for option in sorted_options:
            key = f"{option['special']}:{option['name']}"
            if key not in keys:
                keys.append(key)
                rich.print(f"    [green]{option['special']}[/green][gray] - {option['href']}[/gray]")
    # print(keys)

def get_prices(book_name):
    asyncio.run(main(book_name=book_name))


if __name__ == '__main__':
    fire.Fire({
        'get_prices': get_prices,
    })
