#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  kostal_modbusquery - Read only query of the Kostal Plenticore Inverters using TCP/IP modbus protocol
#  Copyright (C) 2018  Kilian Knoll
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#  Please note that any incorrect or careless usage of this module as well as errors in the implementation can damage your Inverter!
#  Therefore, the author does not provide any guarantee or warranty concerning to correctness, functionality or performance and does not accept any liability for damage caused by this module, examples or mentioned information.
#  Thus, use it at your own risk!
#
#
#  Purpose:
#           Query values from Kostal inverter
#           Used with Kostal Plenticore Plus 10
#  Based on the documentation provided by Kostal:
#           https://www.kostal-solar-electric.com/en-gb/download/download#PLENTICORE%20plus/PLENTICORE%20plus%204.2/Worldwide/Interfaces%20protocols/
#
# Requires pymodbus
# Tested with:
#           python 3.5
#           pymodbus 2.10
# Please change the IP address of your Inverter (e.g. 192.168.178.41 and Port (default 1502) to suite your environment - see below)
#
import pymodbus
from time import sleep
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

class kostal_modbusquery:
    def __init__(self):
        #Change the IP address and port to suite your environment:
        self.inverter_ip="192.168.2.231"
        self.inverter_port="1502"
        #No more changes required beyond this point
        self.KostalRegister = []

        self.Adr108=[]
        self.Adr108 =[108]
        self.Adr108.append("Home own consumption from grid")
        self.Adr108.append("Float")
        self.Adr108.append(0)

        self.Adr116=[]
        self.Adr116 =[116]
        self.Adr116.append("Home own consumption from PV")
        self.Adr116.append("Float")
        self.Adr116.append(0)

        self.Adr575=[]
        self.Adr575 =[575]
        self.Adr575.append("Inverter Generation Power (actual)")
        self.Adr575.append("S16")
        self.Adr575.append(0)

    #-----------------------------------------
    # Routine to read a string from one address with 8 registers
    def ReadStr8(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,8,unit=71)
        STRG8Register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big)
        result_STRG8Register =STRG8Register.decode_string(8)
        return(result_STRG8Register)
    #-----------------------------------------
    # Routine to read a Float from one address with 2 registers
    def ReadFloat(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,2,unit=71)
        FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
        return(result_FloatRegister)
    #-----------------------------------------
    # Routine to read a U16 from one address with 1 register
    def ReadU16_1(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,1,unit=71)
        U16register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U16register = U16register.decode_16bit_uint()
        return(result_U16register)
    #-----------------------------------------
    # Routine to read a U16 from one address with 2 registers
    def ReadU16_2(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,2,unit=71)
        U16register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U16register = U16register.decode_16bit_uint()
        return(result_U16register)
    #-----------------------------------------
    # Routine to read a U32 from one address with 2 registers
    def ReadU32(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,8,unit=71)
        U32register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U32register = U32register.decode_32bit_uint()
        return(result_U32register)
    #-----------------------------------------
    # Routine to read a U32 from one address with 2 registers
    def ReadS16(self,myadr_dec):
        r1=self.client.read_holding_registers(myadr_dec,1,unit=71)
        S16register = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_S16register = S16register.decode_16bit_uint()
        return(result_S16register)


    try:
        def run(self):

            self.client = ModbusTcpClient(self.inverter_ip,port=self.inverter_port)
            self.client.connect()
            self.Adr108[3]=self.ReadFloat(self.Adr108[0])
            self.Adr116[3]=self.ReadFloat(self.Adr116[0])
            self.Adr575[3]=self.ReadS16(self.Adr575[0])


            self.KostalRegister=[]
            self.KostalRegister.append(self.Adr108)
            self.KostalRegister.append(self.Adr116)
            self.KostalRegister.append(self.Adr575)
            self.client.close()

    except Exception as ex:
            print ("Hit the following error :From subroutine kostal_modbusquery :", ex)

def return_data():
        try:
                Kostalvalues =[]
                Kostalquery = kostal_modbusquery()
                Kostalquery.run()
        except Exception as ex:
                print ("Issues querying Kostal Plenticore -ERROR :", ex)
        KostalVal ={}
        for elements in Kostalquery.KostalRegister:
                KostalVal.update({elements[1]: elements[3]})
        return KostalVal

def get_charging_power():
        from requests import get
        url = "http://192.168.2.203/api/status?filter=nrg"
        response = get(url)
        response.raise_for_status()
        return response.json()['nrg'][11]

def rdtn25(num):
    # Find the remainder when divided by 25
    remainder = num % 25
    # Subtract the remainder from the original number to round down
    return num - remainder

def return_data_to_script():
        KostalVal = return_data()
        home_consumption = round(KostalVal['Home own consumption from grid'] + KostalVal['Home own consumption from PV'],2)
        pv_power = round(KostalVal['Inverter Generation Power (actual)'],2)
        grid_to_home = round(KostalVal['Home own consumption from grid'],2)
        actual_charging_power = get_charging_power()
        return pv_power, home_consumption, actual_charging_power, grid_to_home

if __name__ == "__main__":
        #print (return_data_to_script())
        print ("\n")
        while True:
                KostalVal = return_data()
                goe_power = get_charging_power()
                total_home_consumption = round((KostalVal['Home own consumption from grid'] + KostalVal['Home own consumption from PV']),2)
                power_to_from_grid = round(KostalVal['Inverter Generation Power (actual)'] - total_home_consumption,2)
                pv_power = KostalVal['Inverter Generation Power (actual)']
                if power_to_from_grid > 0:
                        PowertoGridStr = " + " + str(power_to_from_grid)
                else:
                        PowertoGridStr = " - " + str(power_to_from_grid * -1)
                print ("\033[4A\033[K", end='')
                print ("PV Power:", pv_power, "W     ")
                print ("Power from (-) / to (+) grid:", PowertoGridStr, "W     ")
                print ("Total current Home consumption is:", total_home_consumption, "W     ")
                print ("Go-eCharger Power:", goe_power, "W      ")
                sleep(.25)
