import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tkinter as tk
from tkintertable import TableCanvas, TableModel
from tkinter import *
import json
BG_COLOR="#213252"
BG_COLOR2="#0f1829"
host_addr= "localhost"
X_Auth_Token=""
queryField = ""

def refreshOAuthToken():
    global X_Auth_Token

    url = f"https://{host_addr}:3443/oauth2/token"
    payload='username=jefe%40sco.com&password=scopass&grant_type=password'
    headers = {
    'Authorization': 'Basic MmQ4MGM1MGUtYTg2Mi00NTRlLTk4YzctNTQ2MGNjNWM0NWY5Ojk0YWU5YmJhLTNkN2MtNDBhYS04YTEyLTFkYTcxYzFkZjZmZA==',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=120)
    X_Auth_Token= response.json()['access_token']
    #print(f"Obtained OAuthToken: {X_Auth_Token}")

def sendRequest(rqType=0, rqFields =""):
    refreshOAuthToken()
    if rqType == 0:
        ## refresh containers
        url = f"https://{host_addr}:8050/v2/entities/?type=Contenedor"
        payload={}
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'X-Auth-Token': X_Auth_Token,
        }
        response = requests.request("GET", url, headers=headers, data=payload,verify=False, timeout=120)
        toTables = response.json()
    if rqType == 1:
        ## refresh IR Sensors
        url = f"https://{host_addr}:8050/v2/entities/?type=IRSensor"
        payload={}
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'X-Auth-Token': X_Auth_Token,
        }
        response = requests.request("GET", url, headers=headers, data=payload,verify=False, timeout=120)
        toTables = response.json()
    if rqType == 2:
        ## query for meds
        url = f"https://{host_addr}:8050/v2/entities/?type=Medicamento"
        payload={}
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'X-Auth-Token': X_Auth_Token,
        }
        response = requests.request("GET", url, headers=headers, data=payload,verify=False, timeout=120)
        medId = -1
        for item in response.json():
            if(item['name']['value'] == queryField):
                medId = item
                break
        if medId == -1:
            return tablerize(medId, medId)
        ## query for meds
        url = f"https://{host_addr}:8050/v2/entities/?type=InventoryItem"
        payload={}
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'X-Auth-Token': X_Auth_Token,
        }
        response = requests.request("GET", url, headers=headers, data=payload,verify=False, timeout=120)
        toTables = (medId, response.json())
    if rqType == 3 or rqType == 4:
        ## setting AC on/off

        #print(f"Sending AC on/of msg")
        url = f"https://{host_addr}:8050/v2/entities/?type=IRSensor"
        payload={}
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'X-Auth-Token': X_Auth_Token,
        }
        response = requests.request("GET", url, headers=headers, data=payload,verify=False, timeout=120)
        toTables = response.json()


        url = f"https://{host_addr}:8050/v2/entities/urn:ngsi-ld:ACActuador:001/attrs"
        if rqType == 3: 
            payload = json.dumps({
            "ACOn": {
                "type": "command",
                "value": ""
            }
            })
        else: 
            payload = json.dumps({
            "ACOff": {
                "type": "command",
                "value": ""
            }
            })
           
        headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/',
        'Content-Type': 'application/json',
        'X-Auth-Token': X_Auth_Token,
        }

        response = requests.request("PATCH", url, headers=headers, data=payload,verify=False,)
        toTables = ""
    if response.ok:
        data = tablerize(toTables, rqType)
    else:
        print(f"Error ocurred during HTTP request.\nResponse:\n{response.text}")
    #print(data)
    return data

def tablerize(dataJSON, rqType):
    tablerizedData= dict([])
    if rqType == 0:
        for item in dataJSON:
            #print (f"{item['id']} t {item['temp']['value']} h {item['humidity']['value']}")
            tablerizedData[item['id']] = {'id': item['id'][-14:] ,'Temperature': item['temp']['value'], 'Humidity': item['humidity']['value'], 'Updated at': item['temp']['metadata']['TimeInstant']['value']}
    if rqType == 1:
        for item in dataJSON:
            #print (f"{item['id']} ir {item['IRValue']['value']}")
            tablerizedData[item['id']] = {'id': item['id'][-12:] ,'IRValue': item['IRValue']['value'], 'Updated at': item['IRValue']['metadata']['TimeInstant']['value']}
    if rqType == 2:
        #print(dataJSON)
        for item in dataJSON[1]:
            if(item['refMedicamento']['value'] == dataJSON[0]['id']):
                tablerizedData[item['id']] = {'id': dataJSON[0]['id'][-15:], 'name': dataJSON[0]['name']['value'] ,'Stored at': item['refStore']['value'][-13:], 'Stock': item['stockValue']['value']}
    if rqType == 3:
        tablerizedData['id'] = {'AC': "AC On command sent." }
    if rqType == 4:
        tablerizedData['id'] = {'AC': "AC Off command sent." }
    if rqType == -1:
        tablerizedData['id'] = {'id': "No item found." }
    #print(tablerizedData)
    return tablerizedData
    
def updateXcel(dataRequest = 0):
    if dataRequest not in range(0,5) or host_addr == "":

        return 1
    data = sendRequest(dataRequest)
    
    tableXcel = TableCanvas(frameXcel,
                cellwidth=70, cellbackgr='#e3f698',
                thefont=('Arial',12),rowheight=20, rowheaderwidth=35,
                rowselectedcolor='yellow', read_only=True, data=data)
    tableXcel.show()

    return 0

def buttonLoadContainers():
    updateXcel(0)
def buttonLoadIRSensors():
    updateXcel(1)
def buttonLoadMedInfo():
    updateXcel(2)
def button_ACOn():
    updateXcel(3)
def button_ACOff():
    updateXcel(4)


def onChangeHostname(fieldHostname):
    global host_addr
    host_addr = fieldHostname.widget.get()
    if host_addr == "Hostname" or host_addr == "":
        host_addr = "localhost"
    print(f"Updated host: {host_addr}")

def onChangeQuery(fieldQueryfield):
    global queryField
    queryField = fieldQueryfield.widget.get()

    print(f"Updated queryField: {queryField}")

if __name__ == '__main__':

    root = tk.Tk()
    root.resizable(False, False)
    root.title(string = 'Storage sensors admin dashboard')
    root.iconphoto(False, tk.PhotoImage(file='./media/icon.png'))
    canvas = tk.Canvas(root,width=1280, height=720,bg=BG_COLOR)
    canvas.pack()

    frameXcel = tk.Frame(root, bg="white")
    frameXcel.place(relwidth=0.7, relheight=0.8, relx=0.05, rely=0.05)

    frameFields = tk.Frame(root,bg=BG_COLOR, highlightbackground = BG_COLOR2,highlightthickness=1, borderwidth=10)
    frameFields.place(relwidth=0.17, relheight=0.6, relx=0.8, rely=0.05)
    
    buttonACOn = tk.Button(frameFields, width=20, height=2, text = "AC On", padx= 5, pady = 12, fg="#121d33", command=button_ACOn)
    buttonACOn.pack()
    buttonACOn = tk.Button(frameFields, width=20, height=2, text = "AC Off", padx= 5, pady = 12, fg="#121d33", command=button_ACOff)
    buttonACOn.pack()
    
    buttonLoadMonitoring = tk.Button(frameFields, width=20, height=2, text = "Cargar sensores neveras", padx= 5, pady = 12, fg="#121d33", command=buttonLoadContainers)
    buttonLoadMonitoring.pack()
    buttonLoadIRMonitoring = tk.Button(frameFields, width=20, height=2, text = "Cargar sensores IR", padx= 5, pady = 12, fg="#121d33", command=buttonLoadIRSensors)
    buttonLoadIRMonitoring.pack()
     
    fieldHostname = tk.Entry(frameFields, width=20,justify='center')
    fieldHostname.insert(0, "Hostname")
    fieldHostname.pack(anchor='s', ipady = 10,side='bottom' , pady=10)
    fieldHostname.bind("<Return>", onChangeHostname)
    


    fieldQueryfield = tk.Entry(frameFields, width=20,justify='center')
    fieldQueryfield.insert(0, ' Buscar: ')
    fieldQueryfield.pack(ipady = 10, pady=10)
    fieldQueryfield.bind("<Return>", onChangeQuery)

    buttonLoadMeds = tk.Button(frameFields, width=20, height=10, text = "Buscar medicamento", padx= 5, pady = 12, fg="#121d33", command=buttonLoadMedInfo)
    buttonLoadMeds.pack(anchor='n')
   
    
    root.mainloop()