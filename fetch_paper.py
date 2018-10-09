import argparse
import pickle
import urllib.request
import feedparser



def parse_arxiv_url(url):
  """ 
  examples is http://arxiv.org/abs/1512.08756v2
  we want to extract the raw id and the version
  """
  ix = url.rfind('/')
  idversion = url[ix+1:] # extract just the id (and the version)
  parts = idversion.split('v')
  assert len(parts) == 2, 'error parsing url ' + url
  return parts[0], int(parts[1])

def encode_feedparser_dict(d):
  """ 
  helper function to get rid of feedparser bs with a deep copy. 
  I hate when libs wrap simple things in their own classes.
  """
  if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
    j = {}
    for k in d.keys():
      j[k] = encode_feedparser_dict(d[k])
    return j
  elif isinstance(d, list):
    l = []
    for k in d:
      l.append(encode_feedparser_dict(k))
    return l
  else:
    return d


if __name__ == "__main__":
    #parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--search-query', type=str,
                        default='cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML',
                        help='query used for arxiv API. See http://arxiv.org/help/api/user-manual#detailed_examples')
    parser.add_argument('--start-index', type=int, default=0, help='0 = most recent API result')
    parser.add_argument('--max-index', type=int, default=10000, help='upper bound on paper index we will fetch')
    parser.add_argument('--results-per-iteration', type=int, default=10, help='passed to arxiv API')
    parser.add_argument('--wait-time', type=float, default=5.0, help='lets be gentle to arxiv API (in number of seconds)')
    parser.add_argument('--break-on-no-added', type=int, default=1, help='break out early if all returned query papers are already in db? 1=yes, 0=no')
    args = parser.parse_args()

    base_url = 'http://export.arxiv.org/api/query?' # base api query url
    query_str = 'search_query={}&sortBy=lastUpdatedDate&start={}&max_result={}'.format( \
                    args.search_query, args.start_index, args.results_per_iteration)
    print(base_url + query_str)
    with urllib.request.urlopen(base_url+query_str) as url:
      resp = url.read()
    
    db={}
    parse = feedparser.parse(resp)
    for e in parse.entries:
        _rawid, _version = parse_arxiv_url(e['id'])
        e['_rawid'] = _rawid
        e['_version'] = _version
        db[_rawid] = e

    f = open('w.txt', 'wb')
    b1 = pickle.dumps(db, fix_imports=-1)
    print(len(b1))



