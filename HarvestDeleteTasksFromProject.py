import os
import json
import urllib.request


def getAllTAMProjectIDs():
    projectPageIndex = 1
    projectFinalPage = 1

    # Create a list of TAM Project IDs
    TAMProjects = []

    while projectPageIndex <= projectFinalPage:
        url = "https://api.harvestapp.com/v2/projects?page=" + str(projectPageIndex)
        headers = {
            "User-Agent": "Braze (joshua.collins@braze.com)",
            "Authorization": "Bearer 2646814.pt.4Pxnh1PNjWk6gX3GyTMUo8nSOQAV_p5h1pBvtFjG_Autb8dTzX6dBWOgu6yWdxYPOJI2G6D3QzNdPajw_w36fg",
            "Harvest-Account-ID": 1049349
        }

        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request, timeout=5)
        responseBody = response.read().decode("utf-8")
        jsonResponse = json.loads(responseBody)

        # Troubleshooting to check that page traversing is correct and projects are recorded
        # print(json.dumps(jsonResponse, sort_keys=True, indent=4))
        # print("==================================================")
        # print(jsonResponse["projects"])


        # print("HERE:" + str(jsonResponse["total_pages"]))

        #set the finalPage index for the loop at the final total page
        projectFinalPage = jsonResponse["total_pages"]
        for item in range(0, len(jsonResponse["projects"])):
            # Parsing out all project Data
            if "TAM Paid Service" in jsonResponse["projects"][item]["name"]:
                #print(jsonResponse["projects"][item]["name"])
                #Add the project name and id to the list
                #TAMProjects.append(jsonResponse["projects"][item]["name"])

                #Add the project IDs to the list of TAM projects
                TAMProjects.append(jsonResponse["projects"][item]["id"])
        #Increment the page count
        projectPageIndex = projectPageIndex + 1

    deleteAllNonTAMTasks(TAMProjects)


#=========================================================================
def deleteTasks(projectID, listOfAssignments):

    for item in listOfAssignments:
        url = "https://api.harvestapp.com/v2/projects/" + str(projectID) + "/task_assignments/" + str(item)
        headers = {
            "User-Agent": "Braze (joshua.collins@braze.com)",
            "Authorization": "Bearer 2646814.pt.4Pxnh1PNjWk6gX3GyTMUo8nSOQAV_p5h1pBvtFjG_Autb8dTzX6dBWOgu6yWdxYPOJI2G6D3QzNdPajw_w36fg",
            "Harvest-Account-ID": 1049349
        }

        request = urllib.request.Request(url=url, headers=headers, method='DELETE')
        try:
            response = urllib.request.urlopen(request, timeout=5)
            responseBody = response.read().decode("utf-8")
            jsonResponse = json.loads(responseBody)
        except:
            print("an error has occured in running the delete operation. Likely due to time already being associated to an unsupported type")




#=========================================================================
def deleteAllNonTAMTasks(TAMProjectIDList):
    print("PROJECT IDS HERE: !!! " + str(TAMProjectIDList))
    ProjectIDArray = TAMProjectIDList
    TAMTasksToKeepIDList = [16955620, 16676663, 16676664, 16676665, 16676666]

    for TAMPaidProject in range(0, len(ProjectIDArray)):
        currentProjectID = ProjectIDArray[TAMPaidProject]
        TAMTaskAssignmentIDsToDelete = []
        taskPageIndex = 1
        taskFinalPage = 1

        # Deleting a single project
        while taskPageIndex <= taskFinalPage:
            url = "https://api.harvestapp.com/v2/projects/" + str(currentProjectID) + "/task_assignments"
            headers = {
                "User-Agent": "Braze (joshua.collins@braze.com)",
                "Authorization": "Bearer 2646814.pt.4Pxnh1PNjWk6gX3GyTMUo8nSOQAV_p5h1pBvtFjG_Autb8dTzX6dBWOgu6yWdxYPOJI2G6D3QzNdPajw_w36fg",
                "Harvest-Account-ID": 1049349
            }

            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request, timeout=5)
            responseBody = response.read().decode("utf-8")
            jsonResponse = json.loads(responseBody)

            #Set max page in case the response is huge
            taskFinalPage = jsonResponse["total_pages"]

            for item in range(0, len(jsonResponse["task_assignments"])):
                if jsonResponse["task_assignments"][item]["task"]["id"] not in TAMTasksToKeepIDList:
                    #Add bad records to the list
                    #print(jsonResponse["task_assignments"][item])
                    TAMTaskAssignmentIDsToDelete.append(jsonResponse["task_assignments"][item]["id"])

            print("==============")
            #print(json.dumps(jsonResponse, sort_keys=True, indent=4))
            #increment to the next page if necessary
            taskPageIndex = taskPageIndex + 1

        #print(TAMTaskAssignmentIDsToDelete)
        print(len(TAMTaskAssignmentIDsToDelete))
        apiCall = deleteTasks(currentProjectID, TAMTaskAssignmentIDsToDelete)


getAllTAMProjectIDs()
