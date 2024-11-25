
# Egypt-Japan University of Science and Technology
# Artificial Intelligence and Data Science Department
# Electronics Inventory Management System for Suppliers
# Version Settings
# ---
''' This dictionary contains all of the data
     needed to be used globally.
     In the event of failure, kindly refer to
     the version info stated in the deployed app.'''
settings = {"version": "0.4.4",
            "day": 12,
            "month": 10,
            "year": 2024}
curr_user = "None"

class VersionInfo():
    ''' Class that contains all related info regarding the deployment.'''
    def get_date():
        ''' Generate date of the current application version in DD/MM/YYYY format.'''
        return "{d}/{m}/{y}".format(d = settings['day'], m = settings['month'], y = settings['year'])

    def get_title():
        ''' Generate project title'''
        return "EMS V.{v} - {d}".format(v = settings['version'], d = VersionInfo.get_date())
    
    def get_user():
        ''' Get current name of user connected. '''
        return curr_user
    
    def set_user(input):
        global curr_user
        curr_user = str(input).lower()