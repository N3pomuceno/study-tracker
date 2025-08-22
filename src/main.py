from util.logger import setup_logger
from util.db_config import setup_engine
from sqlalchemy.orm import Session
import features

logger = setup_logger()


def display_menu():
    print("Menu:")
    print("1. Add new Study Session in Database")
    print("2. View Study Sessions")
    print("3. Edit Categorias")
    print("4. Edit Matérias")
    # print("3. Edit Study Session")
    # print("4. Delete Study Session")
    print("5. Exit")


def make_choice() -> str:
    choice = input("Please enter your choice: ")
    while choice not in ["1", "2", "3", "4", "5"]:
        choice = input("Invalid choice. Please enter a number between 1 and 5: ")
    return choice


def main():
    logger.info("Starting the Study Tracker application.")
    with Session(setup_engine()) as session:

        display_menu()
        choice = make_choice()
        logger.info(f"User selected option {choice}.")

        while choice != "5":
            if choice == "1":
                logger.info("User chose to add a new study session.")
                # Call the function to add a study session
                try:
                    features.add_study_session(session)
                except Exception as e:
                    logger.error(f"Error adding study session: {e}")
            elif choice == "2":
                logger.info("User chose to view study sessions.")
                # Call the function to view study sessions
                try:
                    features.view_recent_study_sessions(session)
                except Exception as e:
                    logger.error(f"Error viewing study sessions: {e}")
            elif choice == "3":
                logger.info("User chose to edit a study session.")
                # Call the function to edit a study session
                # features.edit_study_session(session_id, updated_data)
            elif choice == "4":
                logger.info("User chose to delete a study session.")
                # Call the function to delete a study session
                # features.delete_study_session(session_id)

            display_menu()
            choice = make_choice()
            logger.info(f"User selected option {choice}.")

    logger.info("User exited the program.")


main()
