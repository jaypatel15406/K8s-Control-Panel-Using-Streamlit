"""
Pod Operations Page Module for K8s Control Panel.

This module provides the user interface and backend logic for managing Kubernetes
pods through the Streamlit web interface. It enables users to perform pod operations
such as deletion and resource updates without using kubectl commands.

Features:
    - Namespace selection for pod targeting
    - Multi-pod selection within a namespace
    - Pod deletion operations
    - Resource update operations (memory and CPU - coming soon)
    - Real-time operation status feedback
    - Comprehensive error handling and logging
    - "Coming Soon" placeholder for future features

Architecture:
    The module follows a three-tier structure:
    1. UI Layer: Streamlit widgets for user interaction
    2. Business Logic: Pod operation execution
    3. Data Layer: Kubernetes Core V1 API interactions

Functions:
    choose_pod: Display pod selection dropdown
    perform_pod_operation: Execute pod operations (delete, update resources)
    pod_page: Main page orchestrator for pod operations

Note:
    - Pod deletion is immediately effective and irreversible
    - Resource update functionality is under development
    - All operations are logged for audit purposes
"""

from __future__ import annotations

import json
import logging
import traceback
from pathlib import Path
from typing import Any

import streamlit as st
from kubernetes.client import AppsV1Api, CoreV1Api
from PIL import Image
from streamlit.delta_generator import DeltaGenerator

# Import External Packages
from common.common_component import CommonComponent

# Initialization of 'Class Objects'
common_obj = CommonComponent()

# Initialization of all the Important Variables
config_path = "./config"
app_config_path = f"{config_path}/config.json"

# Unpack all the important variables from 'app_config_path' file
coming_soon_image_width: int = 520  # Default value
if Path(app_config_path).exists():
    with open(app_config_path, "r", encoding="utf-8") as app_conf_file:
        app_conf_json_str = app_conf_file.read()
        app_config_dict: dict[str, Any] = json.loads(app_conf_json_str)
        coming_soon_image_width = app_config_dict.get(
            "coming_soon_image_configurations", {}
        ).get("width", 520)


def choose_pod(
    v1: CoreV1Api | None, namespace: str, pod_col: DeltaGenerator, k8s_error: str
) -> list[str]:
    """Display pod selection dropdown for a given namespace.

    Retrieves all pods from the specified Kubernetes namespace and presents
    them in a multi-select dropdown for user selection.

    Args:
        v1: Kubernetes Core V1 API client instance for pod operations.
           If None (Kubernetes not configured), returns empty list.
        namespace: Kubernetes namespace name to list pods from.
        pod_col: Streamlit column container for the pod selector.
        k8s_error: Error message if Kubernetes is not configured.

    Returns:
        List of selected pod names. Returns empty list if no pods are
        selected, if no pods exist in the namespace, or if Kubernetes
        is not configured.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Execution Start"
        )

        # If Kubernetes is not configured, return empty list
        if v1 is None or k8s_error:
            pod_col.info("⚠️ Kubernetes not configured - no pods available")
            return []

        # List all the Pods
        available_pods = []
        try:
            pods = v1.list_namespaced_pod(namespace=namespace)
            for pod_name in pods.items:
                available_pods.append(pod_name.metadata.name)
        except Exception as e:
            logger.warning(f"Failed to list pods: {e}")
            pod_col.warning("Unable to fetch pods. Check Kubernetes connection.")
            return []

        # Select the Pod using 'Multi Select' functionality
        selected_pod = pod_col.multiselect(
            f"Choose Pod for the given 'Namespace: {namespace}' 👇", available_pods
        )

        logger.info(
            "streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Execution End"
        )
        return selected_pod

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : choose_pod : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : choose_pod : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)
        return []


def perform_pod_operation(
    a1: AppsV1Api,
    v1: CoreV1Api,
    selected_namespace: str,
    selected_pod: list[str],
    selected_pod_operations: str,
    pod_operation_status: bool = False,
) -> bool | None:
    """Execute pod operations on selected Kubernetes pods.

    Performs the specified operation (delete, update resources) on selected
    pods. Currently supports pod deletion; resource updates are under development.

    Args:
        a1: Kubernetes Apps V1 API client instance (reserved for future use).
        v1: Kubernetes Core V1 API client instance for pod operations.
        selected_namespace: Kubernetes namespace containing the pods.
        selected_pod: List of pod names to operate on.
        selected_pod_operations: Operation type to perform. Valid values:
                                - 'Delete Pod': Delete the selected pod(s)
                                - 'Update Memory and CPU': Update resources (coming soon)
        pod_operation_status: Initial status flag. Defaults to False.

    Returns:
        Operation status:
        - True: Operation completed successfully
        - None: Operation failed (error occurred)
        - False: No operation was performed (default)
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Execution Start"
        )

        logger.info(
            f"streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Chosen Operation : {str(selected_pod_operations)}"
        )

        if selected_pod_operations == "Delete Pod":
            logger.info(
                "streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Pod Deletion Started"
            )
            for pod_name in selected_pod:
                v1.delete_namespaced_pod(namespace=selected_namespace, name=pod_name)
                pod_operation_status = True
            logger.info(
                "streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Pod Deletion Completed"
            )

        logger.info(
            "streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Execution End"
        )
        return pod_operation_status

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : perform_pod_operation : traceback : {traceback.format_exc()}"
        )
        pod_operation_status = None
        return pod_operation_status


def pod_page(v1: CoreV1Api | None, a1: AppsV1Api | None, k8s_error: str = "") -> None:
    """Display and manage the Pod Operations page interface.

    Main entry point for pod management functionality. Renders the complete
    UI for namespace selection, pod selection, operation type selection, and
    executes pod operations based on user input.

    The page workflow:
        1. Select namespace from available cluster namespaces
        2. Choose one or more pods from the selected namespace
        3. Select operation type (varies based on pod count)
        4. Execute operation
        5. Display success/error feedback or "Coming Soon" placeholder

    Operation availability:
        - Single pod selected: Delete Pod, Update Memory and CPU
        - Multiple pods selected: Delete Pod only

    Args:
        v1: Kubernetes Core V1 API client instance for pod operations.
        a1: Kubernetes Apps V1 API client instance (reserved for future use).
        k8s_error: Error message if Kubernetes configuration failed, empty string otherwise.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(
            "streamlit : K8S Control Panel : scripts : pod_page : Execution Start"
        )

        # Show warning if Kubernetes is not configured
        if k8s_error:
            st.warning(f"⚠️ {k8s_error}")

        # Initialization of 'Column Partition' for selecting 'Namespace' and 'Pod'
        namespace_col, pod_col, operation_col = st.columns(3)

        # Select 'Namespace' from all the available options
        selected_namespace = common_obj.choose_namespace(
            v1, namespace_col, key="pod", k8s_error=k8s_error
        )

        # Select the 'Pod' in the respective 'Namespace'
        selected_pod = choose_pod(v1, selected_namespace, pod_col, k8s_error)

        # Enable/Disable the Dropdown option based on 'selected_pod'
        # If user hasn't selected any pod then they will not be able to perform operations
        operation_flag = True if len(selected_pod) == 0 else False

        # Choose Operation based on the 'Number of Pods' Selected
        operation_lst = (
            ["Delete Pod", "Update Memory and CPU"]
            if len(selected_pod) == 1
            else ["Delete Pod"]
        )

        # Choose Operations whether he/she want to perform any of the given operations
        selected_pod_operations = operation_col.selectbox(
            "Choose Pod Operation 👇", operation_lst, disabled=operation_flag
        )

        # Made Column Partition to make a button at center location
        _, _, button_col_partition_1, _, _ = st.columns(5)

        # 'Coming Soon ...' Redirection for Update Memory and CPU feature
        if selected_pod_operations == "Update Memory and CPU":
            logger.info(
                "streamlit : K8S Control Panel : scripts : pod_page : pod_page : Inside Update Memory and CPU Section ..."
            )
            # Open 'Coming Soon' Image
            image_path = "media/Coming_Soon_Image.png"
            if Path(image_path).exists():
                image = Image.open(image_path)

                # Assign 'Center' column to the above uploaded image
                _, center_col, _ = st.columns(3)
                center_col.image(
                    image,
                    caption="Hold on tight, I am working on this 😮",
                    width=coming_soon_image_width,
                )
            else:
                st.info("🚧 Feature under development - Coming Soon!")

        else:
            # Perform Pod Operation based on the Selection
            pod_operation_status = button_col_partition_1.button(
                "Perform Pod Operation",
                on_click=perform_pod_operation,
                args=(
                    a1,
                    v1,
                    selected_namespace,
                    selected_pod,
                    selected_pod_operations,
                ),
                disabled=operation_flag,
            )

            # If 'Pod Operated Successfully' then return 'Success' Message else return 'Error'
            if pod_operation_status:
                st.success("Pod Changes Made Successfully")
            elif pod_operation_status is None:
                st.error("Issue Occurred while Operating Pod")

        logger.info("streamlit : K8S Control Panel : scripts : pod_page : Execution End")

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : scripts : pod_page : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)
