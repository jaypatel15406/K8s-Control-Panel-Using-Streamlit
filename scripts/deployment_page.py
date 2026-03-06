"""
Deployment Operations Page Module for K8s Control Panel.

This module provides the user interface and backend logic for managing Kubernetes
deployments through the Streamlit web interface. It enables users to perform
deployment scaling operations without using kubectl commands.

Features:
    - Namespace selection for deployment targeting
    - Multi-deployment selection within a namespace
    - Scale up operations (increase replica count)
    - Scale down operations (decrease replica count to zero)
    - Real-time operation status feedback
    - Comprehensive error handling and logging
"""

from __future__ import annotations

import logging
import traceback

import streamlit as st
from kubernetes.client import AppsV1Api, CoreV1Api
from streamlit.delta_generator import DeltaGenerator

# Import External Packages
from common.common_component import CommonComponent

# Initialization of 'Class Objects'
common_obj = CommonComponent()


def choose_deployment(
    a1: AppsV1Api | None, namespace: str, deployment_col: DeltaGenerator, k8s_error: str
) -> list[str]:
    """Display deployment selection dropdown for a given namespace.

    Retrieves all deployments from the specified Kubernetes namespace and
    presents them in a multi-select dropdown for user selection.

    Args:
        a1: Kubernetes Apps V1 API client instance for deployment operations.
           If None (Kubernetes not configured), returns empty list.
        namespace: Kubernetes namespace name to list deployments from.
        deployment_col: Streamlit column container for the deployment selector.
        k8s_error: Error message if Kubernetes is not configured.

    Returns:
        List of selected deployment names. Returns empty list if no deployments
        are selected, if no deployments exist in the namespace, or if Kubernetes
        is not configured.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : choose_deployment : Execution Start"
        )

        # If Kubernetes is not configured, return empty list
        if a1 is None or k8s_error:
            deployment_col.info("Kubernetes not configured - no deployments available")
            return []

        # List all the Deployments in its respective 'namespace'
        available_deps = []
        try:
            deployment_list = a1.list_namespaced_deployment(namespace=namespace)
            for dep in deployment_list.items:
                available_deps.append(dep.metadata.name)
        except Exception as e:
            logger.warning(f"Failed to list deployments: {e}")
            deployment_col.warning("Unable to fetch deployments. Check Kubernetes connection.")
            return []

        # Select the deployments using 'Multiselect' functionality
        selected_deployments = deployment_col.multiselect(
            f"Choose Deployment/s for the given 'Namespace: {namespace}' 👇",
            available_deps,
        )

        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : choose_deployment : Execution End"
        )
        return selected_deployments

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : choose_deployment : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : choose_deployment : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)
        return []


def deployment_scaling(
    a1: AppsV1Api,
    replicas: int,
    selected_namespace: str,
    selected_deployments: list[str],
    deployment_scaling_status: bool = False,
) -> bool | None:
    """Scale Kubernetes deployments to specified replica count.

    Performs scaling operations on selected deployments by patching their
    replica count. Supports both scale up (positive replica count) and
    scale down (zero replicas) operations.

    Args:
        a1: Kubernetes Apps V1 API client instance.
        replicas: Target number of replicas for the deployment(s).
                 Use 0 for scale down, positive integer for scale up.
        selected_namespace: Kubernetes namespace containing the deployments.
        selected_deployments: List of deployment names to scale.
        deployment_scaling_status: Initial status flag. Defaults to False.

    Returns:
        Scaling operation status:
        - True: All deployments scaled successfully
        - None: Scaling operation failed (error occurred)
        - False: No deployments were scaled (default, should not occur)
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : deployment_scaling : Execution Start"
        )

        # Perform 'Deployment Scaling' based on the number of 'replicas'
        for deployment_name in selected_deployments:
            deployment = a1.read_namespaced_deployment(
                name=deployment_name, namespace=selected_namespace
            )
            deployment.spec.replicas = replicas
            a1.patch_namespaced_deployment(
                name=deployment_name, namespace=selected_namespace, body=deployment
            )
            deployment_scaling_status = True

        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : deployment_scaling : Execution End"
        )
        return deployment_scaling_status

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : deployment_scaling : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : deployment_scaling : traceback : {traceback.format_exc()}"
        )
        deployment_scaling_status = None
        return deployment_scaling_status


def deployment_page(
    v1: CoreV1Api | None, a1: AppsV1Api | None, k8s_error: str = ""
) -> None:
    """Display and manage the Deployment Operations page interface.

    Main entry point for deployment management functionality. Renders the
    complete UI for namespace selection, deployment selection, operation
    type selection, and replica count configuration. Executes scaling
    operations based on user input.

    Args:
        v1: Kubernetes Core V1 API client instance (used for namespace listing).
        a1: Kubernetes Apps V1 API client instance (used for deployment operations).
        k8s_error: Error message if Kubernetes configuration failed, empty string otherwise.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : deployment_page : Execution Start"
        )

        # Show warning if Kubernetes is not configured
        if k8s_error:
            st.warning(f"Kubeconfig Error: {k8s_error}")

        # Page title
        st.markdown("### Deployment Operations")
        st.markdown("Scale your Kubernetes deployments up or down with ease.")

        st.divider()

        # Initialization of 'Column Partition' for selecting 'Namespace' and 'Deployment'
        namespace_col, deployment_col, operation_col = st.columns(3)

        # Select 'Namespace' from all the available options
        selected_namespace = common_obj.choose_namespace(
            v1, namespace_col, key="deployment", k8s_error=k8s_error
        )

        # Select the 'Deployments' in the respective 'Namespace'
        selected_deployments = choose_deployment(
            a1, selected_namespace, deployment_col, k8s_error
        )

        # Enable/Disable the Dropdown option based on 'selected_deployments'
        operation_flag = True if len(selected_deployments) == 0 else False

        # Choose Operations
        selected_operations = operation_col.selectbox(
            "Choose Deployment Operation",
            ["Scale Up", "Scale Down"],
            disabled=operation_flag,
        )

        # Choose the 'Number of Replicas' if you want to 'Scale Up'
        if selected_operations == "Scale Up" and len(selected_deployments) > 0:
            with st.expander("Increase the Number of Replicas"):
                replicas = st.number_input(
                    "Enter Number of Replicas",
                    value=1,
                    key="deployment_replicas",
                    min_value=1,
                    max_value=10,
                    label_visibility="visible",
                )
        else:
            replicas = 0

        logger.info(
            f"streamlit : K8S Control Panel : scripts : deployment_page : deployment_page : Replicas : {str(replicas)}"
        )

        # Made Column Partition to make a button at center location
        _, _, button_col_partition_1, _, _ = st.columns(5)

        # Scale the Deployment based on the Selection
        deployment_scaling_status = button_col_partition_1.button(
            "Perform Deployment Scaling",
            on_click=deployment_scaling,
            args=(a1, replicas, selected_namespace, selected_deployments),
            disabled=operation_flag,
            type="primary",
        )

        # If 'Deployment Scaled Successfully' then return 'Success' Message else return 'Error'
        if deployment_scaling_status:
            st.success("Deployment Changes Made Successfully")
        elif deployment_scaling_status is None:
            st.error("Issue Occurred while Scaling")

        logger.info(
            "streamlit : K8S Control Panel : scripts : deployment_page : deployment_page : Execution End"
        )

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : deployment_page : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : deployment_page : deployment_page : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)
