#! For Running App: python -m streamlit run .\main_application.py
'''
/* CHANGE HISTORY

--- CREATED BY ------ CREATION DATE ------ VERSION ------ PURPOSE --------------------------------------------------------
    Jay Patel         04-APR-2023          1.0            Initial Version of K8S Control Panel's "Home Page"

*/
'''
#* Import all the Important Modules
import time
import yaml
import json
import logging
import traceback
import hydralit_components as hc
from yaml.loader import SafeLoader
from kubernetes import config, client

#* Import all the Important Modules using 'Aliases'
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

#* Import Scripted Modules
from scripts.deployment_page import deployment_page
from scripts.pod_page import pod_page

#* Set Page width to 'Wide'
st.set_page_config(layout= "wide", menu_items= {}, page_icon= "media/K8s Control Panel.png")

#* Hide 'Streamlit' Watermark
with open("template/watermark_removal/watermark_removal_script.html", "r") as watermark_removal_file: hide_st_style= watermark_removal_file.read()
st.markdown(hide_st_style, unsafe_allow_html= True)

#* Initialization of all the Important Variables
config_path = './config'
app_config_path = f'{config_path}/config.json'
credential_config_path = f'{config_path}/credential.yaml'
kube_config_path = f'{config_path}/k8sconfig.txt'

#* Unpack all the important variables from 'app_config_path' file
with open(app_config_path, 'r', encoding= 'utf-8') as app_conf_file: 
    app_conf_json_str = app_conf_file.read()
    app_config_dict = json.loads(app_conf_json_str)

#! This both variables are used to 'Hash' new password using 'decrypted_password_jay_user' which later on pasted into 'credential.yaml'
decrypted_password_jay_user = app_config_dict['decrypted_password_jay_user']
password_hashing_flag = eval(app_config_dict['password_hashing_flag']) 
loader_time = app_config_dict['loader_configurations']['time']
loader_color = app_config_dict['loader_configurations']['color']
loader_index = app_config_dict['loader_configurations']['index'] #? 'Loader Index' for hydrate_component's 'standard_loaders'

#* Load 'Kube Config' for the configuration of 'Core API' and 'Apps API'
config.load_kube_config(kube_config_path)
v1, a1 = client.CoreV1Api(), client.AppsV1Api()

def user_login():
    '''
    Description:
    -------------
        - This Function is used to 'Log In' and 'Authenticate' User before making any changes in 'K8s Cluster'
    
    Return:
    -------------
        - authentication_status (`bool`): return 'True' if 'user' is 'Logged in' with correct credentials else return 'False'
    '''
    try:
        logging.info("streamlit : K8S Control Panel : user_login : Execution Start")

        #* Open 'Credential File' for the 'User Authentication' purpose
        with open(credential_config_path) as credential_conf_file: credential_config_dict = yaml.load(credential_conf_file, Loader= SafeLoader)

        #* Instantiate an 'authenticator' variable
        authenticator = stauth.Authenticate(
                                            credential_config_dict['credentials'],
                                            credential_config_dict['cookie']['name'],
                                            credential_config_dict['cookie']['key'],
                                            credential_config_dict['cookie']['expiry_days'],
                                            credential_config_dict['preauthorized']
                                        )

        #* Hash the Password if needed
        if password_hashing_flag:
            hashed_passwords = stauth.Hasher([decrypted_password_jay_user]).generate()
            logging.info(f"streamlit : K8S Control Panel : user_login :Paste this password into 'config/credential.yaml' File and change the 'password_hashing_flag' in 'config/config.json' File to 'False': {hashed_passwords}")

        #* Authenticate User and return status based on the 'Authentication Process'
        name, authentication_status, username = authenticator.login('Application Login', 'main')
        logging.info(f"streamlit : K8S Control Panel : user_login : name : {name}")
        logging.info(f"streamlit : K8S Control Panel : user_login : authentication_status : {authentication_status}")
        logging.info(f"streamlit : K8S Control Panel : username : name : {username}")
        logging.info("streamlit : K8S Control Panel : user_login : Execution End")

        return authentication_status

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : user_login : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : user_login : traceback : {traceback.format_exc()}")
        st.exception(exe)

def main_page():
    '''
    Description:
    -------------
        - This Function is used to traverse in the 'Main Page' of the Application after 'User Authentication'
    
    '''
    try:
        logging.info("streamlit : K8S Control Panel : main_page : Execution Start")
        time.sleep(0.2) #? Sleep Module for the 'Pre Loading' of Application. To start the 'Hydrate Loader Component' Properly

        #* Lazy Loader for loading an application properly.
        #? NOTE: This loader will only load once at the 'Application Startup' after 'Login'
        if 'has_run' not in st.session_state:
            st.session_state.has_run = True #* Set Session state to 'True' after 'Loader' runs successfully
            with hc.HyLoader('', hc.Loaders.standard_loaders, primary_color= loader_color, index=[loader_index]): time.sleep(loader_time)

        #* Instantiation of all the 'Tabs'
        selected_tab = option_menu(
            None, 
            ["Deployment Operations", "Pod Operations"], 
            icons= ['hdd-stack', 'window-stack'], 
            menu_icon= "cast", 
            default_index= 0, 
            orientation= "horizontal") 

        #* Open Pages based on the 'on-click' method
        if selected_tab == 'Deployment Operations':
            deployment_page(v1= v1, a1= a1) #? Call the 'Deployment Page'
        if selected_tab == 'Pod Operations':
            pod_page(v1= v1, a1= a1) #? Call the 'Deployment Page'

        logging.info("streamlit : K8S Control Panel : main_page : Execution End")
    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : main_page : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : main_page : traceback : {traceback.format_exc()}")
        st.exception(exe)

def main():
    try:
        logging.info("streamlit : K8S Control Panel : main : Execution Start")

        if authentication_status := user_login():
            main_page() #? Enter the 'Main Page' after successful login
        elif authentication_status is False:
            st.error('Username/Password is Incorrect')
        elif authentication_status is None:
            st.warning("Please enter your 'Username' and 'Password'")

        logging.info("streamlit : K8S Control Panel : main : Execution End")

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : main : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : main : traceback : {traceback.format_exc()}")
        st.exception(exe)
    
if __name__ == '__main__':
    #* Title of the Application
    # st.title('Welcome to K8s Control Panel 🕵️‍♀️', text_align= "center")
    st.markdown("<h1 style='text-align: center;'>Welcome to K8s Control Panel 🕵️‍♀️</h1>", unsafe_allow_html=True)
    main()