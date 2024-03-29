# whi_mongodb_server
database server of MongoDB

## Dependency
```
pip3 install rospkg
pip3 install pymongo
```

## Install MongoDB on Jetson nano
1. Go to the official download [website](https://www.mongodb.com/try/download/community). In the "MongoDB Community Server Download" section, select version "3.6.23", platform "Ubuntu 16.04 ARM 64", package "tgz":
   ![image](https://github.com/xinjuezou-whi/whi_mongodb_server/assets/72239958/61a6f480-47d4-4040-85fb-ccaef7c6c8b3)

   > NOTE: if your Ubuntu is later than 18.04, please select version 7.0.6. Meanwhile, replace the following contents that are related to the selected package

3. Extract files with the following command:

   ```
   tar -zxvf mongodb-linux-aarch64-ubuntu1604-3.6.23.tgz
   ```

4. Add the MongoDB's path to environment by editing bashrc:
   
   ```
   nano ~/.bashrc
   ```

   Add the following contents. Please do replace <path_of_extracted> with your extracted path:
   ```
   # mongodb
   export MONGODB_HOME=<path_of_extracted>/mongodb-linux-aarch64-ubuntu1604-3.6.23
   export PATH=$MONGODB_HOME/bin:$PATH
   ```

   Then, source the bash with command:
   ```
   source ~/.bashrc
   ```

5. Create a path for recording db data. Please do replace <yours> with yours:

   ```
   mkdir -p /<yours>/mongodb/data
   mkdir /<yours>/mongodb/logs
   ```
      
6. Create configure file for MongoDB
   ```
   nano /<yours>/mongodb/mongod.conf
   ```

   Write the following contents:
   ```
   storage:
     dbPath: /<yours>/mongodb/data
    journal:
      enabled: true

   systemLog:
     destination: file
     logAppend: true
     path: /<yours>/mongodb/logs/mongod.log

   net:
     port: 27017
     bindIp: 0.0.0.0
   ```

   ctrl-o to save, and ctrl-x to quit
   
7. Launching the server and a client
   Open a terminal for the server:
   ```
   mongod --dbpath /<yours>/mongodb/data/ --logpath /<yours>/mongodb/logs/mongod.log –fork
   ```
   ![image](https://github.com/xinjuezou-whi/whi_mongodb_server/assets/72239958/8f365193-c714-428a-b245-b1110da52a24)


   Open another terminal for the client:
   ```
   mongo --host 127.0.0.1 --port 27017
   ```
   ![image](https://github.com/xinjuezou-whi/whi_mongodb_server/assets/72239958/4ae1d5df-cd56-4376-88dc-acde75bdf2b3)
