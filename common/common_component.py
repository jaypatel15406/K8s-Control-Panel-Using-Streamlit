'''
/* CHANGE HISTORY

--- CREATED BY ------ CREATION DATE ------ VERSION ------ PURPOSE --------------------------------------------------------
    Jay Patel         21-APR-2023          1.0            Initial Version of K8S Control Panel's "Common Component Files"

*/
'''
#* Import all the Important Modules
import logging
import traceback

#* Import all the Important Modules using 'Aliases'
import streamlit as st

class CommonComponent:
    def choose_namespace(self, v1, namespace_col, key):
        '''
            Description:
            -------------
                This Function is used to Choose the Namespace from the given 'K8s Cluster'
            
            Parameters:
            -------------
                - v1 (`obj`)            : K8s Core V1 API
                - namespace_col (`obj`) : Namespace Column Partition for the 'Namespace' Selection Dropdown
                - kwy (`string`)        : Key for the identification of 'Selectbox' is using which key. 
                                            for e.g.: key= 'pod' in case of 'Pod Page', key= 'deployment' in case of 'Deployment Page', etc.
                
            Returns: 
            -------------
                - selected_namespace (`string`): Chosen Namespace
        '''
        try:
            logging.info("streamlit : K8S Control Panel : common : choose_namespace : Execution Start")

            #* List all the Namespace
            available_namespace, namespace_list = [], v1.list_namespace()
            for namespace in namespace_list.items: available_namespace.append(namespace.metadata.name)

            #* Give it into the dropdown
            selected_namespace = namespace_col.selectbox('Choose Namespace 👇', available_namespace, key= key)

            logging.info("streamlit : K8S Control Panel : common : choose_namespace : Execution End")
            return selected_namespace

        except Exception as exe:
            logging.error(f"streamlit : K8S Control Panel : common : choose_namespace : Exception : {str(exe)}")
            logging.error(f"streamlit : K8S Control Panel : common : choose_namespace : traceback : {traceback.format_exc()}")
            st.exception(exe)