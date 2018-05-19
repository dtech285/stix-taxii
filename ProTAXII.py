#!/home/david/envs/stix-taxii/bin/python
from cabby import create_client


def get_client(url, use_https, discovery_path):
    client = create_client(url, use_https, discovery_path)
    return client


def get_services(client):
    print ("\nDiscover Services:")
    services = client.discover_services()
    for service in services:
        print('Service type= {s.type} , address= {s.address}' .format(s=service))

def get_collections(client, verbose=False):
    feed_list = []
    print ("\nDiscover Collections:")
    collections = client.get_collections(
        uri='http://hailataxii.com/taxii-data')

    for collection in collections:
        feed_list.append(collection.name)
        if verbose == True:
            print(collection.name)
    return feed_list

def poll_collection(client, feed_name, uri):
    print ("Polling :", feed_name, ".. could take a while, please be patient..")
    file = open((feed_name + ".xml"), "w")
    content_blocks = client.poll(collection_name=feed_name)

    count =1
    for block in content_blocks:
        taxii_message=block.content.decode('utf-8')
        file.write(taxii_message)
        count+=1
        if count > 20: # just getting the 20 top objects because the lists are huge
            break
    file.close()


def main():

    url = 'hailataxii.com'
    use_https = False
    discovery_path = '/taxii-discovery-service'
    client = get_client(url, use_https, discovery_path)

    feed_list = get_collections(client, verbose = True)


if __name__== '__main__':
    main()
