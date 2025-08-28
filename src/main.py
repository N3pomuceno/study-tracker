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
    print("5. Weekly Report")
    print("6. Monthly Report")
    print("7. Export data")
    print("8. Import data")
    print("9. Exit")


def make_choice() -> str:
    choice = input("Please enter your choice: ")
    while choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        choice = input("Invalid choice. Please enter a number between 1 and 9: ")
    return choice


def main():
    logger.info("Starting the Study Tracker application.")
    with Session(setup_engine()) as session:

        display_menu()
        choice = make_choice()
        logger.info(f"User selected option {choice}.")

        while choice != "9":
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
            elif choice == "5":
                logger.info("User chose to view the weekly report.")
                # Call the function to generate a weekly report
                try:
                    features.generate_weekly_report(session)
                except Exception as e:
                    logger.error(f"Error generating weekly report: {e}")
            elif choice == "6":
                logger.info("User chose to view the monthly report.")
                # Call the function to generate a monthly report
                try:
                    features.generate_monthly_report(session)
                except Exception as e:
                    logger.error(f"Error generating monthly report: {e}")
            elif choice == "7":
                logger.info("User chose to export data.")
                try:
                    features.export_data(session)
                except Exception as e:
                    logger.error(f"Error exporting data: {e}")
            elif choice == "8":
                logger.info("User chose to import data.")
                try:
                    features.import_data(session)
                except Exception as e:
                    logger.error(f"Error importing data: {e}")

            display_menu()
            choice = make_choice()
            logger.info(f"User selected option {choice}.")

    logger.info("User exited the program.")


main()
