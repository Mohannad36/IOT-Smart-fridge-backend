# IOT-Smart-fridge-backend

## Dev Boards we use 

* [Devboard MainBoard](https://www.raspberrypi.com/products/raspberry-pi-5/)
* [Cheaper Option](https://www.raspberrypi.com/)
  * [Sensor Units](https://www.espressif.com/en/products/socs/esp32)
   #### Components
   * [Door Sensor](https://www.kjell.com/se/produkter/smarta-hem/smarta-sensorer/smarta-magnetkontakter/tp-link-tapo-t110-magnetsensor-p65257)

![](FDiagram.png)

*** ***

## Features

* Real-time inventory tracking
* Weight-based food quantity estimation
* Temperature and sensor monitoring
* Expiration date tracking
* Recipe suggestions based on available ingredients

## Dependencies
* [poetry](https://python-poetry.org/)
* [flask](https://flask.palletsprojects.com/en/stable/)

### Hardware Setup

1. **Rasberry Pi with Front Display**: Mounted on the fridge door, Serves as the main controol unit and with user interface  
2. **ESP32 Inside the Fridge**: Will manage internal sensors and cameras that will be mounted on the back and pointed in directions that will not discriminate the customer


*** ***


### Components List


* Rasberry Pi (with touchscreen display)
* ESP32 development board
* Various sensors (temperature, Hall sensor, weight sensor etc)
* Camera module
* Power supply units
* Etc


*** ***


### The system uses a client-server model

* **ESP32(Client)**: Collects sensor data and camera feeds, sends to Raspberry Pi 
* **Raspberry Pi(Server)**: Processes data, manages display and hosts the API


*** *** 


### Installation
1. git clone https://github.com/ghosthookcc/IOT-Smart-fridge-backend.git
2. cd IOT-Smart-fridge-backend/fridge-api
3. pipx poetry
4. poetry install

### How to run
1. cd IOT-Smart-fridge-backend/fridge-api
2. poetry run api

### Communication Architecture
* **TCP** sockets for data transfer between ESP32 and Raspberry Pi
* **REST**less for external integrations
  
![Described Communication Architecture](IOT-Smart-fridge.drawio.png "Communication Architecture")
