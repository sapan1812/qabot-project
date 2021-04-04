# ----------------- All below commands if want to execute from command line -----------

# On windows #
docker build . #no-cache -t sapan1812/qabot

# on windows go to \actions directory
docker build . #no-cache -t sapan1812/qabotactions:1.1


#create connection
docker network create qabot-connect


#Run Shell
docker run #user 1001 -it -v %cd%:/app -p 5005:5005 #net qabot_connect  sapan1812/qabot shell

- run actions
docker run -d -v %cd%:/app/actions #net qabot_connect #name qabot-action sapan1812/qabotactions:1.1

# docker train
docker run #user 1001 -v %cd%:/app sapan1812/qabot train

# ----------------- All below steps to execute Ui interactive shell ----------------
1. install docker on windows
2. go to cloned repostiry folder
3. open command line & execute  : "docker-compose up"
4. once all 3 services are started then click on Rasa-X : localhost:5002/login or any same url shown on console.

Once Rasa-x opened
1. go to left panel
2. open Training menu
3. Update Model -> Train model
