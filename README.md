# pyJobWeb
Shows status of concurrent job execution in python/flask webapp

The installed version may be viewed at this URL:

http://45.55.0.197:5000/web/appTest.html

The above URL should display a Google chart of Job phase times along with a table below indicating the job details. The site will mostly be up (occasionally brought down to update software).

Note: Refresh page, if response is tardy or page partially displayed. (This site is in the cloud (Digital Ocean), and may be in a swapped out state due to infrequent access, and the first subsequent request will be slow).

## Appendix
To deploy currently do the following: 

1. install python3.5.2 on the deployment machine
2. install pip for this python version (pip35)
3. Install the following: flask, flask-restful, flask-cors
4. copy the files (directory tree) into $dir
5. use:
nohup python3.5 $doJobsWeb/pyjobweb.py > /tmp/pyjobweb.log 2>&1 &
to start the job in the background
