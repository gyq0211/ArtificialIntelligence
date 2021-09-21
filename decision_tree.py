import time
import sys
import pprint
P = 1
#SPOT = False # True
#cf = True
#DUSTY_SPOT = False
consumption = 10
#CLEANFlag = True
#GENERAL = True
BB = {"GENERAL":"True","CLEANFlag":"False","DUSTY_SPOT":"False","cf":"True","SPOT":"False","BATTERY_LEVEL":100}
# Node dictionary is a dictionary of behavioral tree's nodes based on their BFS traversal, in the beginning they are all initialized with failed
NodesDic ={"Node1":"Failed", "Node2":"Failed", "Node3":"Failed", "Node4":"Failed", "Node5":"Failed", "Node6":"Failed", "Node7":"Failed", "Node8":"Failed", "Node9":"Failed"}
def charging():
       global   BATTERY_LEVEL
       print "find the path"
       print "going home"
       print "Dock"
       ## This node only consumes 10% of the power
       BB["BATTERY_LEVEL"] = BB["BATTERY_LEVEL"] - consumption
       #SPOT = False
       # The find home command is requested
       #GENERAL = True
       HOME_PATH = "Home"
       # status shows the status of the subtree , whether is suceed, failed, and running, 
       NodesDic["Node2"] = "SUCCEED"
       # battery is fully charged    
       BB["BATTERY_LEVEL"] = 100 
       P = 2
BB["BATTERY_LEVEL"] = 100  
## is it a while(1) and is the priority an input??
t_run = time.time() + 160
while(time.time() < t_run ):
 NodesDic["Node1"] = "Running"
 print("inside main while, BATTERY_LEVEL",BB["BATTERY_LEVEL"])
# check for the priority
 if (P==1):
   NodesDic["Node2"] = "Running"
  
   if (BB["BATTERY_LEVEL"] < 30):
       print "find the path"
       print "going home"
       print "Dock"
       ## This node only consumes 10% of the power
       BB["BATTERY_LEVEL"] = BB["BATTERY_LEVEL"] - consumption
       #SPOT = False
       # The find home command is requested
       #GENERAL = True
       HOME_PATH = "Home"
       # status shows the status of the subtree , whether is suceed, failed, and running, 
       NodesDic["Node2"] = "SUCCEED"
       # battery is fully charged    
       BB["BATTERY_LEVEL"] = 100 

   else:   
       NodesDic["Node2"] = "FAILED"
       BB["BATTERY_LEVEL"] -= consumption

   P = 2    
   #   yeild STATUS 



 if (P==2):
   # most left child of priority 2
    NodesDic["Node3"] = "Running"

    if(BB["SPOT"] == "True"):
       NodesDic["Node4"] = "Running"
       #print("Nodes state dictionary when P=2 and SPOT = True: ")
       #pprint.pprint(NodesDic) 
        # wait for 20s 
       t_end = time.time() + 20
       while time.time() < t_end:
           CLEAN_SPOT = "Running"
          
           # each node consumes 1% * time spent
       CLEAN_SPOT = "SUCCEED"  
       NodesDic["Node4"] = "Succeed"

       BB["BATTERY_LEVEL"] -= 20 * consumption
       DONE_SPOT = True
       print "DONE_SPOT = True"
    ### since it is sequencial, then one sub task completeing succefully, the entire branch status is true
    else:
        print("DONE_SPOT = FALSE")
        BB["BATTERY_LEVEL"] -= 10 * consumption

        NodesDic["Node4"] = "Failed"
 #       print("Node4", NodesDic["Node4"]  ,"but node 3 and the right subtree needs to be calculated")
        if(BB["cf"]=="False"):
           NodesDic["Node7"] = "Failed" 
           NodesDic["Node6"] = "Failed" 
           NodesDic["Node5"] = "Failed" 
           NodesDic["Node3"] = "Failed" 
      #     print("cf", BB["cf"]," SPOT is  ", BB["SPOT"]   )
           #pprint.pprint(NodesDic)   
           print("DONE_SPOT = FALSE")
           print("GENERAL = DONE")
   #     #pprint.pprint(NodesDic)
#    GENERAL = True
    #if one subtree suceeds the whole selection operation seucceeds
#    STATUS = "SUCCEED"
    # second child of successtion 
#    NodesDic["Node5"] = "Running" 
  
    if(BB["GENERAL"] == "True"):
        # Q : what else we do here?  
      NodesDic["Node6"] = "Running" 
      print("GENERAL = Running")
    
      Node1_STATUS = "SUCCEED"
      if(BB["cf"]=="True"):
            NodesDic["Node7"] = "Running" 

            # implimenting the not decorative in the if condition
            if(BB["BATTERY_LEVEL"]>=30):
                NodesDic["Node8"] = "Running" 


                STATUS = "Running"
                if (BB["DUSTY_SPOT"]=="True"):
                    NodesDic["Node9"] = "Running" 
                    #Q should we set the SPOT status as well or not?
                    # A task was requested
                    BB["GENERAL"] = "True"
                    STATUS = "Running"
                    t_end1 = time.time() + 35

                    while time.time() < t_end1:
                       CLEAN_SPOT = "Running"
                       CLEAN = "RUNNING"
                       # battery level is decresed by 1 on each loop iteration
                    BB["BATTERY_LEVEL"] -=  35 * consumption
                    CLEAN_SPOT = "DONE"
                    NodesDic["Node9"] = "SUCCEED" 
                    NodesDic["Node8"] = "SUCCEED" 
                    NodesDic["Node7"] = "SUCCEED" 
                    NodesDic["Node6"] = "SUCCEED" 
                    CLEAN = "DONE"
                    print ("CLEAN = DONE")
                    print("GENERAL = DONE")
#                    #pprint.pprint(NodesDic)
                
                else:  # if nnode9 fails
                   NodesDic["Node9"] = "Failed"

                # clean is a variable that should come from sensors
                   if(BB["CLEANFlag"]=="True"):
                       NodesDic["Node8"] = "SUCCEED" 
                       NodesDic["Node7"] = "SUCCEED" 
                       if (BB["GENERAL"] == "True"):
                          NodesDic["Node6"] = "SUCCEED"
                          print("GENERAL = DONE")
                          NodesDic["Node5"] = "SUCCEED"
                          NodesDic["Node3"] = NodesDic["Node4"] 

                   else:
                       print("Node6 and GENERAL Failed")
                       NodesDic["Node8"] = "Failed" 
                       NodesDic["Node7"] = "Failed"
                       NodesDic["Node6"] = "Failed"
                       NodesDic["Node5"] = "Failed"
                       NodesDic["Node3"] = NodesDic["Node4"]       
        #               print("CF is True, General is true, DUSTY_SPOT and CLEANFlag are False")
            #           #pprint.pprint(NodesDic)
            #if battery level <35
            else:
                    print("battery is less than 30%")
                    charging()
                    
            #No matter the result the requested task has been fulfilled => battery level decreeses 
            BB["BATTERY_LEVEL"] -=  consumption
            if( NodesDic["Node7"]=="SUCCEED"):
           #     if(GENERAL == "Done"):
                NodesDic["Node6"] = "SUCCEED" 
                print("GENERAL = DONE")
                NodesDic["Node5"] = "SUCCEED" 
#                print("CF  GENERAL = True, Node7:", NodesDic["Node7"])
                #pprint.pprint(NodesDic)
     
      else: 
          print("CF is False")
          NodesDic["Node6"] = "Failed"
          print("Node6 and GENERAL Failed")

          NodesDic["Node5"] = "Failed"
          NodesDic["Node3"] =  NodesDic["Node4"]     

    
    else:
            print("GENERAL is False")
        #if (GENERAL == False):
            NodesDic["Node5"] = "Failed"
            #if node5 fails, node3 depends on node4, if node4 is running, node3 is running. If it fails or succeeds, node3 will fail/succeed too.
            NodesDic["Node3"] = NodesDic["Node4"] #"Failed"
            print("Node5: ", NodesDic["Node5"] ,"and node4 has ", NodesDic["Node4"])
 #          print("Nodes state dictionary when P=2 and GENERAL = Done: ")
            #pprint.pprint(NodesDic)
    ### check the status of all nodes
    if(NodesDic["Node4"] == "SUCCEED" or NodesDic["Node5"] == "SUCCEED"):
             NodesDic["Node3"] = "SUCCEED"

#             print("Nodes state dictionary when P=2 and SPOT = False and Node4 =", NodesDic["Node4"]," or Node5 = ", NodesDic["Node5"] )
             #pprint.pprint(NodesDic)

                   
    P =3    
    print("TASK and Therefore GENERAL is Done")

 else:
      print (" P =3 - do nothing")
      P = 1
      BB["BATTERY_LEVEL"] = BB["BATTERY_LEVEL"] - consumption
      print ("BATTERY_LEVEL",BB["BATTERY_LEVEL"])
      NodesDic["Node1"]  = "SUCCEED"
     
#      print("TASK and Therefore GENERAL is Done")
