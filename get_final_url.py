#! python
import grequests
import time

def num_of_redirection(resp):
    """
    return number of redirection
    """
    redirection_code = [301, 302]
    return sum([r.status_code in redirection_code for r in resp.history])

def process_resp(resp, init_url):
    """
    return (number of redirection, final url)
    if exception occured => return (0, initial url) 
    """
    try:
        return (num_of_redirection(resp), resp.url)
    except Exception as e:
        print("{0} has exceptions".format(init_url))
        return (0, init_url)

def get_final_urls(init_urls):
    """
    build a map from initial url to (num of redirection, final_url)
    """
    req = [grequests.get(url) for url in init_urls]
    resp = grequests.map(req)
    final_urls = [process_resp(r, url) for r, url in zip(resp, init_urls)]
    return dict((key, value) for (key, value) in zip(init_urls, final_urls))
    

def main():


    # replace init_urls with your real url list
    init_urls = [
        'http://www.groupon.be/deals/antwerpen_fr/aesthetics-beauty-clinics-2/40127870'
      , 'http://www.google.com'
      , 'http://www.facebook.com'
      , 'http://www.amazon.com'
    ]
    
    s = time.time()
    final_urls = get_final_urls(init_urls)
    """
    final_urls should look like this 
    {
        'http://www.groupon.be/deals/antwerpen_fr/aesthetics-beauty-clinics-2/40127870': (2, 'https://www.groupon.be/deals/aesthetics-beauty-clinics-2'), 
        'http://www.google.com'   : (0, 'http://www.google.com/'), 
        'http://www.facebook.com' : (1, 'https://www.facebook.com/'), 
        'http://www.amazon.com'   : (1, 'https://www.amazon.com/')
    }
    """
    e = time.time()
    print("took {0} seconds to sent {1} url".format(e - s, len(init_urls)))

    """
    your post processing with final urls
    """

if __name__ == "__main__":
    main()