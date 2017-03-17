Scale My Short URL 
=== 

Goal is to build a scalable **URL Shortner**, which is exposed by following endpoints

| Endpoints | Description | 
|:---: | :---:
|`/api/v1/get/short_url=<short_url>` | Redirects to the original url. |
|`/api/v1/create/service=<service>&url=<url>&alias=/<alias>` | Converts a url to shortend url |
|`/api/v1/analytics/short_url=<short_url>` | Gets the analytics for a shortend url |

*`<alias>`* lets you define the url shortend name, if available. *It is optional.*
*`<service>`* lets you configure and customize url_shortner as self-hosted service.

For design aspect of url shortner, you can check out [Design](#design) section. 
## Usage
### Run locally 

```bash
# run url_short.py
$> ./run.sh
#  Basic Testing 
$> ./test.sh
```

### One Click Demo
1. [Install docker-compose](https://docs.docker.com/v1.5/compose/install/)
2. docker-compose up 
3. [curl localhost:8001/api/v1/create&service=cntrl.way&url=https://google.com](#examples) 

### Dependencies

- - **Python 2.7**
	- pymongo
	- redis
	- requests

## Examples
1. `/api/v1/create/service=cntrl.way&url=https://google.com`
2. `/api/v1/create/service=cntrl.way&url=https://google.com&alias=g00`
3. `/api/v1/get/short_url=http://cntrl.way/g00`
4. `/api/v1/analytics/short_url=http://cntrl.way/g00`

## Design

### Chief components 

1. Utilizes an epoll based socket server, for serving clients
	- GIL locks makes threading uncomfortable in python
	- process based parallelism is not scalable one
	- leveraging edge triggered polling to interleave within one process.
	- I have little knowledge on frameworks like twisted, flask, django
2. Redis for caching the responses of recent short urls
	- Need to serve short urls at much faster rate than short url analytics.
	- 80% of most active short urls might have temporal locality.
3. MongoDB for persistent store
	- Can store analytics in document oriented way, so have spatial locality
	- json based documents, easily compliant with rest based applications.

### Data Structures 
1. hasing function 
	- Can use cryptographic hash function md5, but not needed
	-  non-secure hashing function will do
2. Analytics Data structure
	- `read_count`
	-  `expiration_date`
	-  `click-timeline`
	-  `ip-addresses`
	-  `Platform`
	-  `Browser`
3. Shorten URL data structure
	- `hashed_url`
	- `orginal-url`



### Capacity planning
Scalability
Reliability / Fault Tolerance
Consistency
Deployment
Statistics and Metrics