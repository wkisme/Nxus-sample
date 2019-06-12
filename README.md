# nxos-sample
Use Nxus 9000v's rest api to get device's information which will be described in the website.
In the following, i'll use nxos in place of Nxus 9000v.

Nxos is a series of virtual switch of cisco which is different from traditional switch.
The diffrentation is nxos only has data plane, which means it's more simple without concerning how to establish its flow table.

You can find how to deploy a nxos with the following url:
    https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/92x/nx-osv/configuration/guide/b-cisco-nexus-9000v-guide-92x/b-cisco-nexus-9000v-guide-92x_chapter_010.html
    
    
And about the nxos's rest-api information, look this website
    https://developer.cisco.com/site/cisco-nexus-nx-api-references/
    
************************************************************************************
Now, i'll talk about the files that i upload.

The HelloWord directory is a Django project, which can commit information to front end.
My main work is in the HelloWord/HelloWord/view.py where you can see how i user rest-api to get information and send it to the front end. 
There is a function called readcpu which will read data from mysql database and send it to the front end.

The 



