from dotenv import load_dotenv
import os
import uvicorn

import numpy as np
from flask import Flask, redirect, render_template, request, send_file
from flask_caching import Cache
from main import *
from view.front import *


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key= API_KEY


#This API was created to link the backend of the Deux project with the Wordpress Website
#This is the main file of the API to be run.
#The project includes the files  config.json, main.py, front.py which are used to create the conversations and display them in a python app.


app = Flask(__name__, template_folder="APIhero")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route('/main', methods=['POST'])
def success():
        #Requesting the user input, the values of the checkboxes and the different religions.
        choice = request.form.get('choice')
        religion1 = request.form['religion1']
        religion2 = request.form['religion2']
        print(religion1)
        print(religion2)
        cache.set('religion1', religion1)
        cache.set('religion2', religion2)
        #This print() was created to test the value of the checkboxes.
        print(choice)

        if choice == "human":
            return redirect("/human.html")
        elif choice == "robot":
            return redirect("/robot.html")


@app.route('/human', methods = ['POST'])
def human():
    if request.method == 'POST':
        #Configuring the parameters of the conversation.
        conf = config.load_config(CONFIG_FILE)
        
        #Creating the conversation.
        #Requesting what the user put inside the input field.
        #The question the user asked is the input he gave.
        #The user's question always starts with "Human:"
        #religion1 gets the religion the user chose which was stored in the cache.
        #prompt_text is the question and religion to be passed in the gpt3() function.
        #result is the response of the gpt3() function.
        #The response needs to be split into two, the beginning is "Human: {user's question}" and the second "Religion: {Bot's answer}".
        #index opens the human.html file and displays both responses.
        #index is returned.
        user_text = request.form['user_text']
        question = user_text
        user = "Human: "
        religion1 = cache.get('religion1')
        prompt_text = f'{user} {question}\n {religion1}: '
        result = gpt3_call(prompt_text)
        split_result = result.split("\n")
        human_result = split_result[0]
        robot_result = split_result[1]
        index = open("human.html").read().format(human_result=human_result, robot_result=robot_result)
        return index

    cache.clear()         
    return "End of conversation"

@app.route('/robot', methods = ['POST'])
def robot():
    if request.method == 'POST':
        #Configuring the parameters of the conversation.
        conf = config.load_config(CONFIG_FILE)

        #Creating the conversation.
        #Requesting which religions the user chose.
        #Requesting what topic the user put into the input field.
        #restart_sequence is the phrase the first bot will say.
        #start_sequence is the phrase the second bot will say.
        #the topic is set to the user's input
        #The introduction to both religions are macthed.
        religion1= cache.get('religion1')
        religion2= cache.get('religion2')
        user_text = request.form['user_text']
        restart_sequence = religion1
        start_sequence = religion2
        topic = user_text
        religion1_intro = ""
        religion2_intro = ""

        if religion1 == "Pastafarianism":
            religion1_intro = "a religion centered around the Flying Spaghetti Monster, a creator deity who resembles spaghetti and meatballs."
        elif religion1 == "Islam":
            religion1_intro = "the religion of the Muslims, a monotheistic faith regarded as revealed through Muhammad as the Prophet of Allah. "
        elif religion1 == "Zeus" :
            religion1_intro = "in Greek mythology, is the greatest of the gods, the god of the sky and the weather, who ruled over human beings and the other gods"
        elif religion1 == "Odin":
            religion1_intro = "the main god in norse mythology, he is the god of war and death "
        elif religion1 == "Christianity":
            religion1_intro = "a religion based on belief in God and the life and teachings of Jesus Christ, and on the Bible"
        elif religion1 == "Judaism":
            religion1_intro = "the religion of the Jewish people, based on belief in one God and on the laws contained in the Torah and Talmud"
        elif religion1 == "Buddhism":
            religion1_intro = "a religion that originally comes from South Asia, and teaches that personal spiritual improvement will lead to escape from human suffering"
        
        if religion2 == "Pastafarianism":
            religion2_intro = "a religion centered around the Flying Spaghetti Monster, a creator deity who resembles spaghetti and meatballs."
        elif religion2 == "Islam":
            religion2_intro = "the religion of the Muslims, a monotheistic faith regarded as revealed through Muhammad as the Prophet of Allah. "
        elif religion2 == "Zeus" :
            religion2_intro = "in Greek mythology, is the greatest of the gods, the god of the sky and the weather, who ruled over human beings and the other gods"
        elif religion2 == "Odin":
            religion2_intro = "the main god in norse mythology, he is the god of war and death "
        elif religion2 == "Christianity":
            religion2_intro = "a religion based on belief in God and the life and teachings of Jesus Christ, and on the Bible"
        elif religion2 == "Judaism":
            religion2_intro = "the religion of the Jewish people, based on belief in one God and on the laws contained in the Torah and Talmud"
        elif religion2 == "Buddhism":
            religion2_intro = "a religion that originally comes from South Asia, and teaches that personal spiritual improvement will lead to escape from human suffering"
        
        intro = "The {} religion is {}. \n" \
                "The {} religion is {}.\n" \
                "The following is a conversation between {} and {} about {}."\
            .format(religion1,
                    religion1_intro,
                    religion2,
                    religion2_intro,
                    religion1,
                    religion2,
                    topic)
        prompt_text = "{}\n{}: ".format(intro, religion2)

        #TODO: Check for errors during the conversation.
        #TODO: Correct how the conversationis printed in the html file

        
        robot2_result=""
        robot1_result=""
        print(intro)
        robot1_array = np.array(12)
        robot2_array = np.array(12)
        i = 0

        turn = True
        for _ in range(12):
            result = gpt3_call(prompt_text)
            split_result = result.split("\n")
            if turn:
                robot2_result = split_result[3]
                np.append(robot2_result,robot2_result)
                print(robot2_array)
                out_robot2 = open("robot.html").read().format(robot_result1=robot1_array[0], robot_result2=robot2_array[0])
                prompt_text=f"{intro} {robot2_result} \n{religion1}: "
                return out_robot2
            elif turn==False:
                robot1_result = split_result[3]
                np.append(robot1_result,robot1_result)
                print(robot1_result)
                out_robot1 = open("robot.html").read().format(robot_result1=robot1_array, robot_result2=robot2_array)
                prompt_text=f"{intro} {robot1_result} \n{religion2}: "
                return out_robot1
            if turn == False:
                turn = True
            else:
                turn = False
            i += 1
                




    cache.clear()         
    return "End of conversation"       
    

@app.route('/human.html', methods = ['GET'])
def show_human():
    return open("human.html").read()

@app.route('/robot.html', methods = ['GET'])
def show_robot():
    return open("robot.html").read()

#GET request to open and display the style.css file such that the styles are still present after a request.
@app.route('/human.css', methods = ['GET'])  
def style_human():
    return open("human.css").read()

#GET request to open and display the style.css file such that the styles are still present after a request.
@app.route('/robot.css', methods = ['GET'])  
def style_robot():
    return open("robot.css").read()

#GET request for the pexels.jpg file.
#Will give a 304 rederection code afger a first run of the api since the image will already be saved in the cache.
#(304 Not Modified client redirection response code indicates that there is no need to retransmit the requested resources.)
@app.route('/pexels.jpg', methods = ['GET'])
def picture():
    return send_file('pexels.jpg', mimetype='image/jpg')

@app.route('/favicon.ico', methods = ['GET'])
def favicon():
    return send_file('favicon.ico', mimetype='image/x-icon')

#Main
#if __name__ == '__main__':
#   app.run(debug=True)
if __name__ == "__main__":
    app.run(threaded=True, port=5000)
