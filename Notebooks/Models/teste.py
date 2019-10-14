# imports necessarios para se manipular xmls
import xml.etree.ElementTree as ET
import requests

Strings = ET.parse("..\\Xmls\\Strings_en.xml").getroot()

print(Strings.find("DataBase/modifyHeader/string[@name='s1']").text)
arq = input(Strings.find("DataBase/dropColumn/string[@name='s1']").text)

print (arq)