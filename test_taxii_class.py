from taxiiClass import TaxiiClass

verbose = True
url = "hailataxii.com"
use_https = False
discovery_path = '/taxii-discovery-service'
uri = "http://hailataxii.com/taxii-data"

# Create the class object
taxii = TaxiiClass(url, use_https, discovery_path)
# Get the list of services
taxii.get_services(verbose)

# Get the list of feeds
taxii.get_coll(uri, verbose)

# Poll the feed lists
taxii.poll_collection(taxii.feed_list[0])
