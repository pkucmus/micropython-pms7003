# PMS7003 MicroPython Driver

This is a MicroPython adaptation inspired by this Raspberry implementation: https://www.raspberrypi.org/forums/viewtopic.php?p=1244895&sid=5f9dab0e19a7086f9b900b51316ff349#p1244895

[Here](https://botland.com.pl/index.php?controller=attachment&id_attachment=2182) you can find the data sheet from [botland.com.pl](https://botland.com.pl/czujniki-czystosci-powietrza/10924-czujnik-pylu-czystosci-powietrza-pms7003-33v-uart.html)

## Caveats

### UART
I used it with an ESP32. Tried with ESP8266 but since it has only one (full)UART that is being used by the REPL (and WebREPL) it was unusable. ESP32 has an unused UART (UART 2) that can be used to communicate with other devices. So you need a chip that has a free UART (like ESP32).

### Voltage
The documentation claims that the device needs to run on 5V as it's internal fan is driven by 5V where the data pins output 3.3V for high.
**This was not the case for me** I could not read any data other than zeros from the UART when running on 5V. 
Powering the whole device with 3.3V works fine (even though the fan may spin with slower).
I tested running on 3.3V on six different PMS7003 devices.
[MicroPython forum link where I asked for help](https://forum.micropython.org/viewtopic.php?t=4566)

## Example usage

    from pms7003 import PMS7003

    pms = PMS7003()
    pms_data = pms.read()

`PMS7003.read()` will return a dictionary with *the oldest* read that is in the buffer. It means that your reads will always be a bit off in time, depending on the UART's buffer size and the frequency of your reads.
It's generaly a good idea not to read faster than the device writes.

The dictionary will contain the following data:

Key         | Description |                                               
:-----------|:------------------------------------------------------------
PM1_0       | PM 1.0 concentration μ g/m3 (factory environment)           
PM2_5       | PM 2.5 concentration μ g/m3 (factory environment)           
PM10_0      | PM 10 concentration μ g/m3 (factory environment)            
PM1_0_ATM   | PM 1.0 concentration μ g/m3 (atmospheric environment)       
PM2_5_ATM   | PM 2.5 concentration μ g/m3 (atmospheric environment)       
PM10_0_ATM  | PM 10 concentration μ g/m3 (atmospheric environment)        
PCNT_0_3    | Particle count of diameter beyond 0.3 um in 0.1 liter or air
PCNT_0_5    | Particle count of diameter beyond 0.5 um in 0.1 liter or air
PCNT_1_0    | Particle count of diameter beyond 1.0 um in 0.1 liter or air
PCNT_2_5    | Particle count of diameter beyond 2.5 um in 0.1 liter or air
PCNT_5_0    | Particle count of diameter beyond 5.0 um in 0.1 liter or air
PCNT_10_0   | Particle count of diameter beyond 10 um in 0.1 liter or air 

(and four more with `FRAME_LENGTH`, `VERSION`, `ERROR` and `CHECKSUM`)

# AQI

This repo also contains a simple class that can help calculate the Air Quality Index (as described [here](https://en.wikipedia.org/wiki/Air_quality_index#Computing_the_AQI))

```python
from pms7003 import PMS7003
from aqi import AQI

pms = PMS7003()
pms_data = pms.read()
aqi = AQI.aqi(pms_data['PM2_5_ATM'], pms_data['PM10_0_ATM'])
```

`AQI.aqi(pm2_5_atm, pm10_0_atm)` returns an integer representing the AQI.
