'''
/* CHANGE HISTORY

--- CREATED BY ------ CREATION DATE ------ VERSION ------ PURPOSE --------------------------------------------------------
    Jay Patel         21-APR-2023          1.0            Initial Version of K8S Control Panel's "Pod Page"

*/
'''
#* Import all the Important Modules
import json
import logging
import traceback
from PIL import Image

#* Import all the Important Modules using 'Aliases'
import streamlit as st

#* Import External Packages
from common.common_component import CommonComponent

#* Initialization of 'Class Objects'
common_obj = CommonComponent()

#* Initialization of all the Important Variables
config_path = './config'
app_config_path = f'{config_path}/config.json'

#* Unpack all the important variables from 'app_config_path' file
with open(app_config_path, 'r', encoding= 'utf-8') as app_conf_file: 
    app_conf_json_str = app_conf_file.read()
    app_config_dict = json.loads(app_conf_json_str)

#* Fetch all the important variables from 'app_config_dict'
coming_soon_image_width = app_config_dict['coming_soon_image_configurations']['width']

def choose_pod(v1, namespace, pod_col):
    '''
        Description:
        -------------
            This Function is used to Choose the Pod from the given 'K8s Cluster'
        
        Parameters:
        -------------
            - v1 (`obj`)             : K8s Core V1 API'
            - namespace (`string`)   : Namespace of the given 'K8s Cluster'
            - pod_col (`obj`)        : Pod Column Partition for the 'Pod' Selection Dropdown
            
        Returns: 
        -------------
            - selected_pod (`string`): Chosen Pod
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Execution Start")

        #* List all the Pods
        available_pods, pods = list(), v1.list_namespaced_pod(namespace= namespace)
        for pod_name in pods.items: available_pods.append(pod_name.metadata.name)

        #* Select the Pod using 'Multi Select' functionality
        selected_pod = pod_col.multiselect(f"Choose Pod for the given 'Namespace: {namespace}' 👇", available_pods)

        logging.info("streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Execution End")
        return selected_pod

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : scripts : pod_page : choose_pod : traceback : {traceback.format_exc()}")
        st.exception(exe)

def perform_pod_operation(a1, v1, selected_namespace, selected_pod, selected_pod_operations, pod_operation_status= False):
    '''
    Description:
    -------------
        - This Function is used to perform 'Pod Operations'
    
    Parameters:
    -------------
            - a1 (`obj`)                          : K8s Apps V1 API
            - v1 (`obj`)                          : K8s Core V1 API
            - selected_namespace (`str`)          : Selected 'Namespace'
            - selected_pod (`str`)                : Name of Selected Pod
            - selected_pod_operations (`str`)     : Name of Pod Operation
            - pod_operation_status (`bool`)       : Pod Operation Status
    
    Return:
    -------------
        - pod_operation_status (`bool`) : Pod Operation Status. Returns 'True' if 'Pod Operated' Successfully else return 'None'. default is 'False'
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Execution Start")

        logging.info(f"streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Chosen Operation : {str(selected_pod_operations)}")
        if selected_pod_operations == 'Delete Pod':
            logging.info("streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Pod Deletion Started")
            for pod_name in selected_pod:
                v1.delete_namespaced_pod(namespace= selected_namespace, name= pod_name)
                pod_operation_status= True
            logging.info("streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation :  Pod Deletion Completed")

        logging.info("streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Execution End")
        return pod_operation_status

    except Exception as exe:
        logging.error(
            f"streamlit : K8S Control Panel : scripts  pod_page : perform_pod_operation : Exception : {str(exe)}"
        )
        logging.error(f"streamlit : K8S Control Panel : scripts  pod_page : perform_pod_operation : traceback : {traceback.format_exc()}")
        pod_operation_status= None
        return pod_operation_status

def pod_page(v1, a1):
    '''
    Description:
    -------------
        - This Function is used to perform any kind of 'Operation' on 'Pods'
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts : pod_page : Execution Start")

        #* Initialization of 'Column Partition' for selecting 'Namespace' and 'Pod'
        namespace_col, pod_col, operation_col = st.columns(3)

        #* Select 'Namespace' from all the available options
        selected_namespace = common_obj.choose_namespace(v1, namespace_col, key= 'pod')

        #* Select the 'Pod' in the respective 'Namespace'
        selected_pod = choose_pod(v1, selected_namespace, pod_col)

        #* 'Enable/ Disable' the Dropdown option based on 'selected_pod'. If user haven't selected any pod then they will not be able to perform any kind of operations
        operation_flag = True if len(selected_pod) == 0 else False

        #* Choose Operation based on the 'Number of Pods' Selected
        operation_lst = (
            ['Delete Pod', 'Update Memory and CPU']
            if len(selected_pod) == 1
            else ['Delete Pod']
        )

        #* Choose Operations weather he/ she want to perform any of the given operations: 'Delete Pod', 'Update Memory and CPU', etc.
        selected_pod_operations = operation_col.selectbox('Choose Pod Operation 👇', operation_lst, disabled= operation_flag)

        #? Made Column Partition to make a button at center location by accessing the '3rd Partition'
        _, _, button_col_partition_1, _, _ = st.columns(5)

        #TODO After the Integration of Other Pod Operations stated below. Please shift this operation into 'perform_pod_operation' function and remove 'else-if' conditions as well
        #? 1. Update Pod Memory, Update Pod CPU, etc.
        #* 'Coming Soon ...' Redirection
        if selected_pod_operations == 'Update Memory and CPU':
            logging.info("streamlit : K8S Control Panel : scripts : pod_page : pod_page : Inside Update Memory and CPU Section ...")
            #* Open 'Coming Soon' Image
            image = Image.open('media/Coming_Soon_Image.png')
            
            #* Assign 'Center' column to the above uploaded image
            _, center_col, _ = st.columns(3)
            center_col.image(image, caption='Hold on tight, I am working on this 😮', width= coming_soon_image_width)
            
        else:
            #* Perform Pod Operation based on the Selection
            pod_operation_status= button_col_partition_1.button('Perform Pod Operation', on_click= perform_pod_operation, args= (a1, v1, selected_namespace, selected_pod, selected_pod_operations), disabled= operation_flag)

            #* If 'Pod Operated Successfully' then return 'Success' Message else return 'Error'
            if pod_operation_status:
                st.success('Pod Changes Made Successfully')
                # st.balloons() #? Animation on 'Successful' Code Execution
            elif pod_operation_status is None:
                st.error('Issue Occurred while Operating Pod') 

        logging.info("streamlit : K8S Control Panel : scripts : pod_page : Execution End")

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : scripts : pod_page : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : scripts : pod_page : traceback : {traceback.format_exc()}")
        st.exception(exe)