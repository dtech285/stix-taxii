#!/home/david/envs/stix-taxii/bin/python
from cabby import create_client

class TaxiiClass:

    def __init__(self, url, use_https, discovery_path):
        self.feed_list = []
        self.url = url
        self.use_https = use_https
        self.discovery_path = discovery_path

        self.client = create_client(self.url, self.use_https, self.discovery_path)
        """ (host=None, port=None, discovery_path=None, use_https=False, version='1.1', headers=None)
            Create a client instance (TAXII version specific).

            host, port, use_https, discovery_path values can be overridden per request with uri argument passed to a client’s method.
        """


    def get_services(self, verbose=False):
        """ Get services advertised by TAXII server.

        This method will try to do automatic discovery by calling discover_services()
        from the Cabby library.

        Parameters:
            service_type (str) – filter services by specific type. Accepted values are listed in cabby.entities.SERVICE_TYPES
            service_types (str) – filter services by multiple types. Accepted values are listed in cabby.entities.SERVICE_TYPES
        Returns:
            list of service instances

        Return type:
            list of cabby.entities.DetailedServiceInstance (or cabby.entities.InboxDetailedService)

        Raises:
            ValueError – if URI provided is invalid or schema is not supported
            cabby.exceptions.HTTPError – if HTTP error happened
            cabby.exceptions.UnsuccessfulStatusError – if Status Message received and status_type is not SUCCESS
            cabby.exceptions.ServiceNotFoundError – if no service found
            cabby.exceptions.AmbiguousServicesError – more than one service with type specified
            cabby.exceptions.NoURIProvidedError – no URI provided and client can’t discover services

        """
        print ("\nDiscover Services:")
        services = self.client.discover_services()
        if verbose == True:
            for service in services:
                print('Service type= {s.type} , address= {s.address}' .format(s=service))


    def get_coll(self, uri, verbose=False):
        """
        Get collections from Feed Management Service.

        if uri is not provided, client will try to discover services and find Feed Management Service among them.

        Parameters:
            uri (str) – URI path to a specific Feed Management service

        Returns:
            list of collections

            Return type:
            list of cabby.entities.Collection

        Raises:
            ValueError – if URI provided is invalid or schema is not supported
            cabby.exceptions.HTTPError – if HTTP error happened
            cabby.exceptions.UnsuccessfulStatusError – if Status Message received and status_type is not SUCCESS
            cabby.exceptions.ServiceNotFoundError – if no service found
            cabby.exceptions.AmbiguousServicesError – more than one service with type specified
            cabby.exceptions.NoURIProvidedError – no URI provided and client can’t discover services
        """
        feed_list = []
        print ("\nDiscover Collections:")
        collections = self.client.get_collections(uri)

        for collection in collections:
            self.feed_list.append(collection.name)
            if verbose == True:
                print(collection.name)
        #return feed_list

    def poll_collection(self, feed_name):
        """
        (collection_name, begin_date=None, end_date=None, subscription_id=None, content_bindings=None, uri=None)
        Poll content from Polling Service.

        if uri is not provided, client will try to discover services and find Polling Service among them.

        Parameters:
            collection_name (str) – feed to poll
            begin_date (datetime) – ask only for content blocks created after begin_date (exclusive)
            end_date (datetime) – ask only for content blocks created before end_date (inclusive)
            subsctiption_id (str) – ID of the existing subscription
            content_bindings (list) – list of stings or cabby.entities.ContentBinding objects
            uri (str) – URI path to a specific Inbox Service
        Raises:
            ValueError – if URI provided is invalid or schema is not supported
            cabby.exceptions.HTTPError – if HTTP error happened
            cabby.exceptions.UnsuccessfulStatusError – if Status Message received and status_type is not SUCCESS
            cabby.exceptions.ServiceNotFoundError – if no service found
            cabby.exceptions.AmbiguousServicesError – more than one service with type specified
            cabby.exceptions.NoURIProvidedError – no URI provided and client can’t discover services
        """
        print ("Polling :", feed_name, ".. could take a while, please be patient..")
        file = open((feed_name + ".xml"), "w")
        content_blocks = self.client.poll(collection_name=feed_name)

        count =1
        for block in content_blocks:
            taxii_message=block.content.decode('utf-8')
            file.write(taxii_message)
            count+=1
            if count > 20: # just getting the 20 top objects because the lists are huge
                break
        file.close()
