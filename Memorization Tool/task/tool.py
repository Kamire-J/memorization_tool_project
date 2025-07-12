from sqlalchemy.orm import sessionmaker, declarative_base

from constants import MAIN_MENU, SUB_MENU
from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box_number = Column(Integer, default=1)


    def __repr__(self):
        return "<Flashcard(question='%s', answer='%s')>"


# write your code here
class MemorizationTool:
    def __init__(self, db_url="sqlite:///flashcard.db?check_same_thread=False"):
        self.menu = MAIN_MENU
        self.add_menu = SUB_MENU
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def menu_display(self):
        print(self.menu)

    def sub_menu(self):
        print(self.add_menu)

    def update_flashcard(self, card):
        session = self.Session()

        response = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n').lower()

        if response == "d":
            session.query(Flashcard).filter(Flashcard.id == card.id).delete()
            session.commit()

        elif response == "e":
            print(f"current question: {card.first_column}")
            new_question = input('please write a new question:\n')
            print(f"current answer: {card.second_column}")
            new_answer = input("please write a new answer:\n").strip()

            session.query(Flashcard).filter(Flashcard.id == card.id).update({
                Flashcard.first_column: new_question,
                Flashcard.second_column: new_answer
            })
            session.commit()
        else:
            print(f"{response} is not an option")



    def add_flashcards(self):
        session = self.Session()
        while True:
            self.sub_menu()
            sub_input = input().strip()
            if sub_input == "1":
                while True:
                    question = input("Question:\n").strip()
                    if question:
                        break
                    print("the question can't be empty!")
                while True:
                    answer = input("Answer:\n").strip()
                    if answer:
                        break
                    print("the answer can't be empty!")
                new_data = Flashcard(first_column=question, second_column=answer)
                session.add(new_data)
                session.commit()
            elif sub_input == "2":
                print()
                break
            else:
                print(f"{sub_input} is not an option")

    def practice_flashcards(self):
        session = self.Session()
        flashcards = session.query(Flashcard).all()



        if not flashcards:
            print("There is no flashcard to practice!")

        for card in flashcards:
            print(f"Question: {card.first_column}")
            see_answer = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n').strip()
            if see_answer == "y":
                print(f"Answer: {card.second_column}")
                user_response = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n').strip()
                if user_response == "y":
                    session.query(Flashcard).filter(Flashcard.id == card.id).update({
                        card.box_number: 2,
                    })
                elif user_response == "n":
                    continue
                else:
                    print(f"{user_response} is not an option")
            elif see_answer == "n":
                continue
            elif see_answer == "u":
                self.update_flashcard(card)
            else:
                print(f"{see_answer} is not an option")


    def run(self):
        while True:
            self.menu_display()
            main_input = input().strip()
            print()
            if main_input == "1":
                self.add_flashcards()
            elif main_input == "2":
                self.practice_flashcards()
            elif main_input == "3":
                print("Bye!")
                break
            else:
                print(f"{main_input} is not an option")


if __name__ == '__main__':
    tool = MemorizationTool()
    tool.run()
