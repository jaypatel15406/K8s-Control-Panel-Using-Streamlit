'''
/* CHANGE HISTORY

--- CREATED BY ------ CREATION DATE ------ VERSION ------ PURPOSE --------------------------------------------------------
    Jay Patel         06-APR-2023          1.0            Initial Version of K8S Control Panel's "Deployment Page"

*/
'''
#* Import all the Important Modules
import logging
import traceback

#* Import all the Important Modules using 'Aliases'
import streamlit as st

#* Import External Packages
from common.common_component import CommonComponent

#* Initialization of 'Class Objects'
common_obj = CommonComponent()

def choose_deployment(a1, namespace, deployment_col):
    '''
        Description:
        -------------
            This Function is used to Choose the Deployment from the given 'K8s Cluster'
        
        Parameters:
        -------------
            - a1 (`obj`)             : K8s Apps V1 API'
            - namespace (`string`)   : Namespace of the given 'K8s Cluster'
            - deployment_col (`obj`) : Deployment Column Partition for the 'Deployment' Selection Dropdown
            
        Returns: 
        -------------
            - selected_deployments (`list`): List of Chosen Deployment
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : choose_deployment : Execution Start")

        #* List all the Deployment in its respective 'namespace'
        available_deps, deployment_list = [], a1.list_namespaced_deployment(namespace= namespace)
        for dep in deployment_list.items: available_deps.append(dep.metadata.name)

        #* Select the deployments using 'Multiselect' functionaliy
        selected_deployments = deployment_col.multiselect(f"Choose Deployment/s for the given 'Namespace: {namespace}' 👇", available_deps)

        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : choose_deployment : Execution End")
        return selected_deployments

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : choose_deployment : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : choose_deployment : traceback : {traceback.format_exc()}")
        st.exception(exe)

def deployment_scaling(a1, replicas, selected_namespace, selected_deployments, deployment_scaling_status= False):
    '''
    Description:
    -------------
        - This Function is used to perform 'Deployment Scaling'
    
    Parameters:
    -------------
            - a1 (`obj`)                          : K8s Apps V1 API
            - replicas (`int`)                    : Number of 'Replicas'
            - selected_namespace (`str`)          : Selected 'Namespace'
            - selected_deployments (`list`)       : List of Selected Deployments
            - deployment_scaling_status (`bool`)  : Deployment Scaling Status
    
    Return:
    -------------
        - deployment_scaling_status (`bool`) : Deployment Scaling Status. Returns 'True' if 'Deployment Scaling' is 'Successful' else return 'None'. default is 'False'
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : deployment_scaling : Execution End")

        #* Perform 'Deployment Scaling' based on the number of 'replicas'
        for deployment_name in selected_deployments:
            deployment, deployment.spec.replicas = a1.read_namespaced_deployment(name= deployment_name, namespace= selected_namespace), replicas
            a1.patch_namespaced_deployment(name= deployment_name, namespace= selected_namespace, body= deployment)
            deployment_scaling_status= True

        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : deployment_scaling : Execution End")
        return deployment_scaling_status

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : deployment_scaling : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : deployment_scaling : traceback : {traceback.format_exc()}")
        deployment_scaling_status= None
        return deployment_scaling_status

def deployment_page(v1, a1):
    '''
    Description:
    -------------
        - This Function is used to perform any kind of 'Operation' on 'Deployment'
    '''
    try:
        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : deployment_page : Execution Start")

        #* Initialization of 'Column Partition' for selecting 'Namespace' and 'Deployment'
        namespace_col, deployment_col, operation_col = st.columns(3)

        #* Select 'Namespace' from all the available options
        selected_namespace = common_obj.choose_namespace(v1, namespace_col, key= 'deployment')

        #* Select the 'Deployments' in the respective 'Namespace'
        selected_deployments = choose_deployment(a1, selected_namespace, deployment_col)

        #* 'Enable/ Disable' the Dropdown option based on 'selected_deployments'. If user haven't selected any deployment then they will not be able to 'Scale' the same OR vice versa
        operation_flag = True if len(selected_deployments) == 0 else False

        #* Choose Operations weather he/ she want to 'Scale Up/ Scale Down' the 'Deployments'
        selected_operations = operation_col.selectbox('Choose Deployment Operation 👇', ['Scale Up', 'Scale Down'], disabled= operation_flag)

        #* Choose the 'Number of Replicas' if you want to 'Scale Up'. default= '1' in case of 'Scale Up'. Else it will be '0' in case of 'Scale Down'
        if selected_operations == 'Scale Up' and len(selected_deployments) > 0:
            with st.expander("Want to Increase the Number of 'Replicas' 🤔 ?'"):
                replicas = st.number_input("Enter Number of Replicas", value = 1, key = 'numeric', min_value= 1, max_value= 10, label_visibility= "visible")
        else:
            replicas= 0

        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : deployment_page : Replicas : " + str(replicas))

        #? Made Column Partition to make a button at center location by accessing the '3rd Partition'
        _, _, button_col_partition_1, _, _ = st.columns(5)

        #* Scale the Deployment based on the Selection
        deployment_scaling_status= button_col_partition_1.button('Perform Deployment Scaling', on_click= deployment_scaling, args= (a1, replicas, selected_namespace, selected_deployments), disabled= operation_flag)

        #* If 'Deployment Scaled Successfully' then return 'Success' Message else return 'Error'
        if deployment_scaling_status:
            st.success('Deployment Changes Made Successfully')
            # st.balloons() #? Animation on 'Successful' Code Execution
        elif deployment_scaling_status is None:
            st.error('Issue Occurred while Scaling !!!')

        logging.info("streamlit : K8S Control Panel : scripts  deployment_page : deployment_page : Execution End")

    except Exception as exe:
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : deployment_page : Exception : {str(exe)}")
        logging.error(f"streamlit : K8S Control Panel : scripts  deployment_page : deployment_page : traceback : {traceback.format_exc()}")
        st.exception(exe)