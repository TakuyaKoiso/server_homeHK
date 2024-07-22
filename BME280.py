import spidev
import time
import datetime

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000
spi.mode = 0

spi.xfer2([0xF2 & 0b01111111, 0b00000101])
spi.xfer2([0xF5 & 0b01111111, 0b11100000])
spi.xfer2([0xF4 & 0b01111111, 0b10110111])

temp_msb_address = [0xFA, 0x00]
temp_lsb_address = [0xFB, 0x00]
temp_xlsb_address = [0xFC, 0x00]
dig_T1_lsb_address = [0x88, 0x00]
dig_T1_msb_address = [0x89, 0x00]
dig_T2_lsb_address = [0x8A, 0x00]
dig_T2_msb_address = [0x8B, 0x00]
dig_T3_lsb_address = [0x8C, 0x00]
dig_T3_msb_address = [0x8D, 0x00]
dt_now = datetime.datetime.now()
temp_msb = spi.xfer2(temp_msb_address)
temp_lsb = spi.xfer2(temp_lsb_address)
temp_xlsb = spi.xfer2(temp_xlsb_address)
dig_T1_lsb = spi.xfer2(dig_T1_lsb_address)
dig_T1_msb = spi.xfer2(dig_T1_msb_address)
dig_T2_lsb = spi.xfer2(dig_T2_lsb_address)
dig_T2_msb = spi.xfer2(dig_T2_msb_address)
dig_T3_lsb = spi.xfer2(dig_T3_lsb_address)
dig_T3_msb = spi.xfer2(dig_T3_msb_address)
adc_T = ((temp_msb[1] & 0b11111111) <<12) | ((temp_lsb[1] & 0b11111111) << 4) | ((temp_xlsb[1] & 0b11110000) >> 4)

dig_T1= ((dig_T1_msb[1] & 0b11111111) <<8) | (dig_T1_lsb[1] & 0b11111111) 

dig_T2= ((dig_T2_msb[1] & 0b11111111) <<8) | (dig_T2_lsb[1] & 0b11111111) 
if dig_T2 >> 15 == 1:
    dig_T2 = (dig_T2 & 0b0111111111111111) - 32768

dig_T3= ((dig_T3_msb[1] & 0b11111111) <<8) | (dig_T3_lsb[1] & 0b11111111) 	
if dig_T3 >> 15 == 1:
    dig_T3 = (dig_T3 & 0b0111111111111111) - 32768

var1 = (float(adc_T)/16384.0 - float(dig_T1)/1024.0) * float(dig_T2)
var2 = ((float(adc_T)/131072.0 - float(dig_T1)/8192.0) * (float(adc_T)/131072.0 - float(dig_T1)/8192.0)) * float(dig_T3)
t_fine = var1 + var2
T = t_fine / 5120.0

print(dt_now.strftime('%Y/%m/%d %H:%M:%S'))
print('{:3.1f}'.format(T) + ' degC')

press_msb_address = [0xF7, 0x00]
press_lsb_address = [0xF8, 0x00]
press_xlsb_address = [0xF9, 0x00]
dig_P1_lsb_address = [0x8E, 0x00]
dig_P1_msb_address = [0x8F, 0x00]
dig_P2_lsb_address = [0x90, 0x00]
dig_P2_msb_address = [0x91, 0x00]
dig_P3_lsb_address = [0x92, 0x00]
dig_P3_msb_address = [0x93, 0x00]
dig_P4_lsb_address = [0x94, 0x00]
dig_P4_msb_address = [0x95, 0x00]
dig_P5_lsb_address = [0x96, 0x00]
dig_P5_msb_address = [0x97, 0x00]
dig_P6_lsb_address = [0x98, 0x00]
dig_P6_msb_address = [0x99, 0x00]
dig_P7_lsb_address = [0x9A, 0x00]
dig_P7_msb_address = [0x9B, 0x00]
dig_P8_lsb_address = [0x9C, 0x00]
dig_P8_msb_address = [0x9D, 0x00]
dig_P9_lsb_address = [0x9E, 0x00]
dig_P9_msb_address = [0x9F, 0x00]

press_msb = spi.xfer2(press_msb_address)
press_lsb = spi.xfer2(press_lsb_address)
press_xlsb = spi.xfer2(press_xlsb_address)
dig_P1_lsb = spi.xfer2(dig_P1_lsb_address)
dig_P1_msb = spi.xfer2(dig_P1_msb_address)
dig_P2_lsb = spi.xfer2(dig_P2_lsb_address)
dig_P2_msb = spi.xfer2(dig_P2_msb_address)
dig_P3_lsb = spi.xfer2(dig_P3_lsb_address)
dig_P3_msb = spi.xfer2(dig_P3_msb_address)
dig_P4_lsb = spi.xfer2(dig_P4_lsb_address)
dig_P4_msb = spi.xfer2(dig_P4_msb_address)
dig_P5_lsb = spi.xfer2(dig_P5_lsb_address)
dig_P5_msb = spi.xfer2(dig_P5_msb_address)
dig_P6_lsb = spi.xfer2(dig_P6_lsb_address)
dig_P6_msb = spi.xfer2(dig_P6_msb_address)
dig_P7_lsb = spi.xfer2(dig_P7_lsb_address)
dig_P7_msb = spi.xfer2(dig_P7_msb_address)
dig_P8_lsb = spi.xfer2(dig_P8_lsb_address)
dig_P8_msb = spi.xfer2(dig_P8_msb_address)
dig_P9_lsb = spi.xfer2(dig_P9_lsb_address)
dig_P9_msb = spi.xfer2(dig_P9_msb_address)

adc_P = ((press_msb[1] & 0b11111111) << 12) | ((press_lsb[1] & 0b11111111) << 4) | ((press_xlsb[1] & 0b11110000) >> 4) 

dig_P1 = (dig_P1_msb[1] << 8) | (dig_P1_lsb[1])

dig_P2 = (dig_P2_msb[1] << 8) | (dig_P2_lsb[1])
if (dig_P2 >> 15) == 1:
    dig_P2 = (dig_P2 & 0b0111111111111111) - 32768

dig_P3 = (dig_P3_msb[1] << 8) | (dig_P3_lsb[1])
if dig_P3 >> 15 == 1:
    dig_P3 = (dig_P3 & 0b0111111111111111) - 32768

dig_P4 = (dig_P4_msb[1] << 8) | (dig_P4_lsb[1])
if dig_P4 >> 15 == 1:
    dig_P4 = (dig_P4 & 0b0111111111111111) - 32768

dig_P5 = (dig_P5_msb[1] << 8) | (dig_P5_lsb[1])
if dig_P5 >> 15 == 1:
    dig_P5 = (dig_P5 & 0b0111111111111111) - 32768

dig_P6 = (dig_P6_msb[1] << 8) | (dig_P6_lsb[1])
if dig_P6 >> 15 == 1:
    dig_P6 = (dig_P6 & 0b0111111111111111) - 32768

dig_P7 = (dig_P7_msb[1] << 8) | (dig_P7_lsb[1])
if dig_P7 >> 15 == 1:
    dig_P7 = (dig_P7 & 0b0111111111111111) - 32768

dig_P8 = (dig_P8_msb[1] << 8) | (dig_P8_lsb[1])
if dig_P8 >> 15 == 1:
    dig_P8 = (dig_P8 & 0b0111111111111111) - 32768

dig_P9 = (dig_P9_msb[1] << 8) | (dig_P9_lsb[1])
if dig_P9 >> 15 == 1:
    dig_P9 = (dig_P9 & 0b0111111111111111) - 32768

var1 = t_fine / 2.0 - 64000.0
var2 = var1 * var1 * float(dig_P6) / 32768.0
var2 = var2 + var1 * float(dig_P5) * 2.0
var2 = var2 / 4.0 + float(dig_P4) * 65536.0
var1 = (float(dig_P3) * var1 * var1 / 524288.0 + float(dig_P2) * var1) / 524288.0
var1 = (1.0 + var1 / 32768.0) * float(dig_P1)

if var1 == 0.0:
   quit() 

p = 1048576.0 - float(adc_P)
p = (p - var2 / 4096.0) * 6250.0 / var1
var1 = float(dig_P9) * p * p / 2147483648.0
var2 = p * float(dig_P8) / 32768.0
p = p + (var1 + var2 + float(dig_P7)) / 16.0
p_sea = p*(1 - (0.0065*115.3) / (T + 0.0065*115.3 + 273.15))**-5.257

print('{:5.1f}'.format(p/100) + ' hPa')
print('{:5.1f}'.format(p_sea/100) + ' hPa')

hum_msb_address = [0xFD, 0x00]
hum_lsb_address = [0xFE, 0x00]
dig_H1_address = [0xA1, 0x00]
dig_H2_lsb_address = [0xE1, 0x00]
dig_H2_msb_address = [0xE2, 0x00]
dig_H3_address = [0xE3, 0x00]
dig_H4_msb_address = [0xE4, 0x00]
dig_H4H5_address = [0xE5, 0x00]
dig_H5_msb_address = [0xE6, 0x00]
dig_H6_address = [0xE7, 0x00]
hum_msb = spi.xfer2(hum_msb_address)
hum_lsb = spi.xfer2(hum_lsb_address)
dig_H1 = spi.xfer2(dig_H1_address)
dig_H2_lsb = spi.xfer2(dig_H2_lsb_address)
dig_H2_msb = spi.xfer2(dig_H2_msb_address)
dig_H3 = spi.xfer2(dig_H3_address)
dig_H4_msb = spi.xfer2(dig_H4_msb_address)
dig_H4H5 = spi.xfer2(dig_H4H5_address)
dig_H5_msb = spi.xfer2(dig_H5_msb_address)
dig_H6 = spi.xfer2(dig_H6_address)
adc_H = (hum_msb[1] << 8) | (hum_lsb[1])

dig_H2 = (dig_H2_msb[1] << 8) | (dig_H2_lsb[1])
if dig_H2 >> 15 == 1:
    dig_H2 = (dig_H2 & 0b0111111111111111) - 32768

dig_H4 = (dig_H4_msb[1] << 4) | (dig_H4H5[1] & 0b00001111)
if dig_H4 >> 11 == 1:
    dig_H4 = (dig_H4 & 0b011111111111) - 2048 

dig_H5 = (dig_H5_msb[1] << 4) | (dig_H4H5[1] & 0b11110000 >> 4)
if dig_H5 >> 11 == 1:
    dig_H5 = (dig_H5 & 0b0111111111111111) - 2048

if dig_H6[1] >> 7 == 1:
    dig_H6[1] = (dig_H6[1] & 0b0111111111111111) - 128

var_H = t_fine-76800.0
var_H = (adc_H - (dig_H4 * 64.0 + dig_H5 / 16384.0 * var_H)) * (dig_H2 / 65536.0 * (1 + dig_H6[1] / 67108864.0 * var_H * (1.0 + dig_H3[1] / 67108864.0 * var_H)))
var_H *= 1.0 - dig_H1[1] * float(var_H) / 524288.0

if var_H > 100:
    var_H = 100
elif var_H < 0:
    var_H = 0
    
print('{:3.1f}'.format(var_H) + ' %')

spi.close
