from random import randrange
from math import floor
from chai_py import ChaiBot, Update
import re

# TODO:
# if an invalid response is given, repeat the question
# add more Q's
# remove ability to restart over at any point? is that really helpful?
# change 'a' to 'an' on percentages that start with a vowel


class Bot(ChaiBot):

    score = 0
    scaleMessage = "On a scale of 0 to 10, how well can you"

    questions = [  # [question, is10Good?]
        [f"{scaleMessage} walk in a straight line?", 1, True],
        ["How many drinks you have had? If you can't remember put '10'", -1, True],
        [f"{scaleMessage} close your eyes and touch your nose?", 1, True],
        [f"Did you text your ex at any point tonight?", 2, True],
        [f"Can you remember your last drink?", 2, True],
        [f"What's 12x12?", 3, True, "144"],  # randomise??
    ]
    usedQuestionIndexes = []
    prevQuestionIndex = -1
    prevQuestionPositive = True  # value doesn't matter on init
    questionsOver = False

    drunkLevelEmojis = ["😇", "😃", "😅", "😬", "🥴"]

    def setup(self):
        self.logger.info("Setting up...")

    def resetQuestions(self):
        self.score = 0
        self.prevQuestionIndex = -1
        self.usedQuestionIndexes = []
        self.questionsOver = False

    async def on_message(self, update: Update) -> str:

        userResponse = update.latest_message.text.lower()

        if update.latest_message.text == self.FIRST_MESSAGE_STRING:
            question = self.getQuestion()
            return f"Hi! Let's test if you're drunk! {question}"
        else:
            if userResponse == "reset" or self.questionsOver:
                self.resetQuestions()
            else:
                errorMessage = self.calcScore(userResponse)
                if errorMessage:
                    return (
                        errorMessage
                        + "\n\n"
                        + self.questions[self.prevQuestionIndex][0]
                    )

                if self.checkDone():
                    percentage = self.getPercentage()
                    emoji = self.drunkLevelEmojis[floor(percentage / 20)]
                    self.questionsOver = True
                    return f"Theres a {percentage}% chance you're drunk! {emoji} \n\nType anything to start again"  # reword?

            question = self.getQuestion()
            return question

    def calcScore(self, userResponse):
        questionCode = self.questions[self.prevQuestionIndex][1]

        if 2 <= questionCode <= 3:
            if "yes" in userResponse:
                self.score += 5
            elif "no" in userResponse:
                self.score += 5
            else:
                return f"Could not detect a 'yes' or 'no' in your response 😕"
        else:
            number = re.search(r"\d+", userResponse)

            if number:
                number = int(number.group(0))
                if 0 <= number <= 10:
                    if self.prevQuestionPositive:
                        number = 10 - number
                    self.score += number
                else:
                    return f"Number must be between 0 and 10 😕"
            else:
                return f"Could not detect a number in your response 😕"

    def checkDone(self):
        return len(self.usedQuestionIndexes) == len(self.questions)

    def getPercentage(self):
        return round((self.score / len(self.questions)) * 10)

    def getQuestion(self):
        if self.checkDone():
            return "oh no, im broken"

        while True:  # find a question that hasn't already been used
            index = randrange(len(self.questions))
            if index not in self.usedQuestionIndexes:
                break

        self.usedQuestionIndexes.append(index)
        self.prevQuestionIndex = index
        self.prevQuestionPositive = self.questions[index][1]

        return self.questions[index][0]
