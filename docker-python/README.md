# http://arnaudchenyensu.com/create-a-python-3-environment-using-docker/
# docker build -t python3-env .
# cd /vagrant/
# sudo docker run -i python3-env pip3 install requests
# sudo docker ps -l
# sudo docker commit 3790312f3c4a  python3-env
# sudo docker run -i python3-env python3 < opera.py

---------------------------------------------------------------------------------------

docker build -t lera/opera .
sudo docker run lera/opera python3 /src/opera.py

----------------------------------------------------------------------------------------

# links
# packaging: http://www.diveintopython3.net/packaging.html
# importing: http://chimera.labs.oreilly.com/books/1230000000393/ch10.html
# https://civisanalytics.com/blog/engineering/2014/08/14/Using-Docker-to-Run-Python/

-----------------------------------------------------------------------------------------

http://www.gbopera.it/2011/08/monteverdi-in-festa-a-macerata/


