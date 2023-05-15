import os
import telebot
from dotenv import dotenv_values
import requests
from bs4 import BeautifulSoup
import random

config = dotenv_values(".env")
BOT_TOKEN = config['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome = "Welcome to Fetcherr.\n\nThis is a bot to fetch solutions for problems on Leetcode. \n\nPlease enter a valid number between 1 and 2654 which represents the problem number of your problem along with a language of your preference out of the following options(optional):\nC++\nJava\nPython\nFor example, to fetch solution for problem 45 in Java, enter 0045 Java.\n\nYou can also request a random problem from leetcode by sending the word 'question' as message.\n\nTry sending the same message a few times if it doesn't work right away cuz good things take time ;-).\n\nThis bot is made by Omkar Wadekar"
    bot.reply_to(message, welcome)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    inputt = message.text
    if(inputt.lower() == "question"):
        getQuestion(message)
    else:
        sendSolution(message)
    
def get_solution(number):
    url = "https://walkccc.me/LeetCode/problems/"+number+"/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    # tag = soup.code
    tag2 = soup.find_all("h1")
    tag3 = soup.find_all("pre")
    # print(tag.text)
    return [tag2[0].text, tag3]

def sendSolution(message):
    inputt = message.text
    rcv_array = inputt.split(" ")
    # print(rcv_array)
    prob_num = rcv_array[0]
    prob_lang = rcv_array[1] if len(rcv_array)==2 else "c++"
    s = ""
    for i in range(0,55):
        s = s+ "-"
    if(prob_num.isdigit() and int(prob_num) > 0 and int(prob_num) < 2655):
        solution = get_solution(prob_num)
        # print(solution)
        languages = solution[1]
        resp = s + "\n\n" +solution[0] + "\n\n" + s + "\n\n"
        if(prob_lang=='c++'):
            resp = resp + "C++ Solution: \n\n"+ s+ "\n\n" + languages[1].text + "\n\n"
        elif(prob_lang=='java'):
            resp = resp + "Java Solution: \n\n" + s+ "\n\n"+ languages[3].text + "\n\n"
        elif(prob_lang=='python'):
            resp = resp + "Python Solution: \n\n"+ s+ "\n\n" + languages[5].text + "\n\n"
        bot.reply_to(message, resp)
        return
    else:
        bot.reply_to(message, 'Please enter a valid input.')
        return
    
def getProblemName():
    with open('list.txt', 'r') as file:
         file_contents = file.readlines()
    my_list = [line.strip() for line in file_contents]
    random_number = random.randint(0, len(my_list)-1)
    return [my_list[random_number], random_number]
    
def getQuestion(message):
    pack = getProblemName()
    name = pack[0]
    prob_num = str(pack[1])
    name = name.lower()
    name = name.replace(" ","-")
    url = "https://leetcode.com/problems/" + name + "/"
    add = "\n\nName : " + pack[0] + "\nProblem Number: "+ prob_num +"\nLink to the question: " + url

    bot.reply_to(message,add)

bot.infinity_polling()