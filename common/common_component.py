"""
Common Components Module for K8s Control Panel.

This module provides reusable UI components and utility functions used across
multiple pages in the K8s Control Panel application. It centralizes common
functionality to ensure consistency and reduce code duplication.

Features:
    - Namespace selection component (used by all operation pages)
    - Consistent error handling and logging
    - Streamlit widget standardization
    - Reusable UI patterns

Classes:
    CommonComponent: Container class for shared UI components and utilities.

Example:
    from common.common_component import CommonComponent
    
    common_obj = CommonComponent()
    namespace = common_obj.choose_namespace(v1_api, column, key="deployment")
"""

from __future__ import annotations

import logging
import traceback

import streamlit as st
from kubernetes.client import CoreV1Api
from streamlit.delta_generator import DeltaGenerator


class CommonComponent:
    """Reusable UI components for Kubernetes operations.

    This class provides common UI components used across different pages
    of the K8s Control Panel application. It centralizes functionality
    like namespace selection to ensure consistent behavior and appearance.

    Example:
        >>> common_obj = CommonComponent()
        >>> namespace = common_obj.choose_namespace(v1_api, col1, "deployment")
    """

    def choose_namespace(
        self,
        v1: CoreV1Api | None,
        namespace_col: DeltaGenerator,
        key: str,
        k8s_error: str = "",
    ) -> str:
        """Display namespace selection dropdown for Kubernetes cluster.

        Retrieves all available namespaces from the Kubernetes cluster and
        presents them in a dropdown selector. This is a common first step
        for most Kubernetes operations as it scopes subsequent actions to
        the selected namespace.

        Args:
            v1: Kubernetes Core V1 API client instance for namespace operations.
               If None (Kubernetes not configured), shows empty dropdown with warning.
            namespace_col: Streamlit column container for the namespace selector.
                          This determines where the dropdown appears in the UI layout.
            key: Unique Streamlit widget key for session state management.
                Common values:
                - 'pod': Used in Pod Operations page
                - 'deployment': Used in Deployment Operations page
            k8s_error: Error message if Kubernetes is not configured. Empty string
                      if Kubernetes is properly configured.

        Returns:
            Selected namespace name as a string. Returns empty string if Kubernetes
            is not configured or if namespace listing fails.

        Example:
            >>> from kubernetes import client, config
            >>> config.load_kube_config()
            >>> v1 = client.CoreV1Api()
            >>> common_obj = CommonComponent()
            >>> namespace = common_obj.choose_namespace(v1, st.columns(1)[0], "deployment")
        """
        try:
            logger = logging.getLogger(__name__)
            logger.info(
                "streamlit : K8S Control Panel : common : choose_namespace : Execution Start"
            )

            # If Kubernetes is not configured, show info message and return empty
            if v1 is None or k8s_error:
                namespace_col.info("⚠️ Kubernetes not configured - no namespaces available")
                logger.info(
                    "streamlit : K8S Control Panel : common : choose_namespace : Kubernetes not configured"
                )
                return ""

            # List all the Namespaces
            available_namespace = []
            try:
                namespace_list = v1.list_namespace()
                for namespace in namespace_list.items:
                    available_namespace.append(namespace.metadata.name)
            except Exception as e:
                logger.warning(f"Failed to list namespaces: {e}")
                namespace_col.warning("Unable to fetch namespaces. Check Kubernetes connection.")
                return ""

            # Give it into the dropdown
            selected_namespace = namespace_col.selectbox(
                "Choose Namespace 👇", available_namespace, key=key
            )

            logger.info(
                "streamlit : K8S Control Panel : common : choose_namespace : Execution End"
            )
            return selected_namespace

        except Exception as exe:
            logger = logging.getLogger(__name__)
            logger.error(
                f"streamlit : K8S Control Panel : common : choose_namespace : Exception : {str(exe)}"
            )
            logger.error(
                f"streamlit : K8S Control Panel : common : choose_namespace : traceback : {traceback.format_exc()}"
            )
            st.exception(exe)
            return ""
