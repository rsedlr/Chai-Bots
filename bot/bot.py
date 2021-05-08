from random import choice as randChoice
from chai_py import ChaiBot, Update


class Bot(ChaiBot):
    numberOfRounds = 10
    moves = ["Rock 🪨", "Paper 📰", "Scissors ✂️", "Water Bomb 💦", "Dynamite 🧨"]
    winningMoves = {
        0: 2,  # Rock beats Scissors
        1: 0,  # Paper beats Rock
        2: 1,  # Scissors beats Paper
        # Water Bomb and Dynamite are handled separately
    }

    HELP_TEXT = (
        'Type "rock", "paper", "scissors", "dynamite" or "water bomb" to make a move!'
    )

    def setup(self):
        self.logger.info("Setting up...")
        self.resetScores()

    def resetScores(self):
        self.dynamiteLeft = [2, 2]  # [bot, user]
        self.score = [0, 0]  # [bot, user]
        self.currentRound = 0

    async def on_message(self, update: Update) -> str:
        if update.latest_message.text == self.FIRST_MESSAGE_STRING:
            return f"Hi! Are you ready to play Rock Paper Scissors? {self.HELP_TEXT}"

        moves = [0, 1, 2]
        if self.dynamiteLeft[1] > 0:  # if user has dynamite left
            moves.append(3)
        if self.dynamiteLeft[0] > 0:  # if bot has dynamite left
            moves.append(4)
        botMove = randChoice(moves)

        if botMove == 4:
            self.dynamiteLeft[0] -= 1

        userResponse = update.latest_message.text.lower()
        if "rock" in userResponse:
            userMove = 0
        elif "paper" in userResponse:
            userMove = 1
        elif "scissors" in userResponse:
            userMove = 2
        elif "water" in userResponse or "bomb" in userResponse:
            userMove = 3
        elif "dynamite" in userResponse:
            userMove = 4
            if self.dynamiteLeft[1] <= 0:
                return "You've run out of Dynamite! Make another move"
            self.dynamiteLeft[1] -= 1
        else:
            return f"Could not detect a move in your response 😕 {self.HELP_TEXT}"

        self.currentRound += 1

        if userMove == botMove:
            return self.draw(botMove)
        if userMove == 4:
            if botMove == 3:
                return self.draw(botMove)
            return self.userWin(botMove)
        if botMove == 4:
            if userMove == 3:
                return self.draw(botMove)
            return self.botWin(botMove)
        if userMove == 3:
            return self.botWin(botMove)
        if botMove == 3 or self.winningMoves[userMove] == botMove:
            return self.userWin(botMove)
        return self.botWin(botMove)

    def getScore(self):
        message = (
            f"\n\nRound {self.currentRound} of {self.numberOfRounds} "
            + f"\n\nScore: {self.score[0]}-{self.score[1]} "
            + f"\n\nDynamite 🧨 left: {self.dynamiteLeft[0]}:{self.dynamiteLeft[1]}"
        )

        if self.currentRound == self.numberOfRounds:
            message += f", \n\n"
            if self.score[0] > self.score[1]:
                message += f"**I win the round 🎊🎊🎊**"
            elif self.score[0] < self.score[1]:
                message += f"**You win the round 🎉🎉🎉**"
            else:
                message += f"**It's a draw!**"
            message += f"\n\nWanna play again? {self.HELP_TEXT}"
            self.resetScores()
        return message

    def userWin(self, botMove):
        self.score[1] += 1
        return f"{self.moves[botMove]}  - You win 🎉 {self.getScore()}"

    def botWin(self, botMove):
        self.score[0] += 1
        return f"{self.moves[botMove]}  - I win 🎊 {self.getScore()}"

    def draw(self, botMove):
        return f"{self.moves[botMove]}  - Draw! {self.getScore()}"
