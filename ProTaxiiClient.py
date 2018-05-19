#!/home/david/envs/stix-taxii/bin/python
from cabby import create_client

class ProTaxiiClient():

    def __init__(self):
        class_variable = ""
        self.collection_list = []

    def create_client(self, domain, use_https=False, discovery_path):
        self.client = create_client(domain,use_https, discovery_path)

    def discovery():
        holder = ""
        service = ""


    def get_collections():
        feed_list = ""
        self.collections = self.client.get_collections(
            uri='https://otx.alienvault.com/taxii/collections')
        print("\n")
        for collection in collections:
            feed_list.append(collection.name)
        print("\n")

    def polling():
        holder = ""
        for collection_name in HailATaxiiFeedList:
            print ("Polling :", collection_name, ".. could take a while, please be patient..")
            file = open((collection_name + ".xml"), "w")
            content_blocks = client.poll(collection_name=collection_name)

            count =1
            for block in content_blocks:
                taxii_message=block.content.decode('utf-8')
                file.write(taxii_message)
                count+=1
                if count > 20: # just getting the 20 top objects because the lists are huge
                    break
            file.close()




        #client = create_client(
            #'hailataxii.com',
            #use_https=False,
            #discovery_path='/taxii-discovery-service')
