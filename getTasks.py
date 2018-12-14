import http.client
import json
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def getRequestURL(url):

    conn = http.client.HTTPSConnection("3.basecampapi.com")
    payload = ""
    token = config['DEFAULT']['token']
    headers = { 'User-Agent' : 'COMQUAS',
        'Authorization': "Bearer " + token }
    conn.request("GET", "/" + config['DEFAULT']['account'] + "/" + url, payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    return json.loads(data)

projects = getRequestURL("/projects.json")


for project in projects:
    toprint = "NAME :" + project["name"]
    projectID = str(project["id"])
    count = 0
    for dock in project["dock"]:
        if dock["name"] == "todoset" :
            setID = str(dock["id"])
            #now, try to get the todo set
            
            todolists = getRequestURL("/buckets/" + projectID + "/todosets/" + setID + "/todolists.json")
            
            for todolist in todolists:
                todolistID = str(todolist["id"])
                todos = getRequestURL("/buckets/" + projectID + "/todolists/" + todolistID + "/todos.json")
                toprint = toprint + "\nList Name: " + todolist["title"]
                toprint = toprint + "\n=========="
                
                for todo in todos:
                    if todo["completed"] == False:
                        count = count + 1
                        #time to print it
                        toprint = toprint + "\nTasks: " + todo["title"]
                        assignees = todo["assignees"]
                        for assignee in assignees:
                            toprint = toprint + "\nAssign: " + assignee["name"]
                        toprint = toprint + "\n"

    toprint = toprint + "\n\n"
    if count != 0 :
        print(toprint)