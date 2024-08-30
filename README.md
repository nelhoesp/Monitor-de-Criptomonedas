## CryptoMonitor (Monitor de criptomonedas)

La aplicación gráfica (GUI) está hecha en Python/tkinter y permite realizar un seguimiento en tiempo real de un conjunto de criptomonedas presentes en una cartera de inversión. La interface se muestra a continuación.

![imagen](https://github.com/nelhoesp/Monitor-Criptomonedas/assets/156467223/6dfd62bb-d367-44f0-bed9-8dc189150a4f)

La sección Price Realtime contiene un Combobox con una lista de criptomonedas donde se muestra el precio en tiempo real del activo (el programa se actualiza cada 5 segundos), así como su cambio respecto al precio del último cierre del mercado, tanto en valor como en porcentaje. Los valores se codifican en función de las fluctuaciones de precios. Si este disminuye, se mostrará en color rojo; de lo contrario, se mostrará en color verde.
La lista de criptomonedas disponibles a elegir son: Bitcoin, Ethereum, Chainlink, Binance Coin, Litecoin y Dogecoin.
La información del precio de los tokens se obtienen a través de la consulta de la API libre de Coinbase (Exchange de criptomonedas). Para consultar el precio de cada una se usaron las siguientes URLs:
- Bitcoin: https://api.coinbase.com/v2/prices/btc-usd/spot
- Ethereum: https://api.coinbase.com/v2/prices/eth-usd/spot
- Chainlink: https://api.coinbase.com/v2/prices/link-usd/spot
- Binance Coin: https://api.coinbase.com/v2/prices/bnb-usd/spot
- Litecoin: https://api.coinbase.com/v2/prices/ltc-usd/spot
- Dogecoin: https://api.coinbase.com/v2/prices/doge-usd/spot

![imagen](https://github.com/nelhoesp/Monitor-Criptomonedas/assets/156467223/4bc87659-d8e7-4ef6-8778-a513cc48de15)

La sección Historic Data muestra una tabla con información histórica del precio del token seleccionado en los últimos 30 días. Esta tabla tiene las columnas "Date" para la fecha del registro, "Open" que es el precio de apertura en el mercado y "Close" que es el precio de cierre del mercado.
Esta información se obtuvo por medio de la librería "yfinance", que permite obtener información histórica de un activo financiero a partir de la fuente "YahooFinance".

La sección Price Historic Chart muestra un gráfico de velas japonesas con la información de los últimos 30 días de los precios del token seleccionado (la misma que se obtuvo para la sección "Historic Data", además de los valores máximo y mínimo del precio de la criptomoneda en cada día). 
