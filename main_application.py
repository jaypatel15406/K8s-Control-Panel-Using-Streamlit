"""
K8s Control Panel - Main Application Module.

This module serves as the entry point for the K8s Control Panel Streamlit application.
It provides a web-based interface for managing Kubernetes deployments and pods without
requiring direct kubectl command usage.

The application handles:
    - User authentication via streamlit-authenticator
    - Kubernetes cluster connection via kubeconfig
    - Deployment operations (scaling up/down)
    - Pod operations (deletion, resource updates)
    - Session state management
    - Logging and error handling

Architecture:
    The application follows a modular structure with separate pages for different
    Kubernetes operations. Authentication is handled before granting access to
    cluster management features.

Example:
    To run the application:
    $ python -m streamlit run main_application.py

Note:
    Ensure all configuration files are properly set up before running:
    - config/config.json: Application settings
    - config/credential.yaml: User authentication credentials
    - config/k8sconfig.txt: Kubernetes cluster configuration
"""

from __future__ import annotations

import json
import logging
import os
import traceback
from typing import Any

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from kubernetes import client, config
from kubernetes.config import ConfigException
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader

# Import scripted modules
from scripts.deployment_page import deployment_page
from scripts.pod_page import pod_page
from scripts.documentation_page import render_documentation_page

# Import common components
from common.logging_config import setup_logging
from common.footer_component import render_footer
from common.k8s_tips import render_tips_section

# Set Page width to 'Wide'
st.set_page_config(
    layout="wide",
    menu_items={},
    page_icon="media/K8s_Control_Panel_Favicon.svg",
    initial_sidebar_state="expanded"
)

# Hide 'Streamlit' Watermark
with open("template/watermark_removal/watermark_removal_script.html", "r") as (
    watermark_removal_file
):
    hide_st_style = watermark_removal_file.read()
st.markdown(hide_st_style, unsafe_allow_html=True)

# Initialization of all the Important Variables
config_path = "./config"
app_config_path = f"{config_path}/config.json"
credential_config_path = f"{config_path}/credential.yaml"
kube_config_path = f"{config_path}/k8sconfig.txt"


def load_configuration() -> dict[str, Any] | None:
    """Load and validate application configuration from JSON file.

    Returns:
        Dictionary containing application configuration settings, or None if
        configuration cannot be loaded.
    """
    try:
        if not os.path.exists(app_config_path):
            return None

        with open(app_config_path, "r", encoding="utf-8") as app_conf_file:
            app_conf_json_str = app_conf_file.read()
            app_config_dict = json.loads(app_conf_json_str)
        return app_config_dict
    except (json.JSONDecodeError, Exception):
        return None


def load_kubernetes_clients() -> tuple[client.CoreV1Api | None, client.AppsV1Api | None, str]:
    """Load and initialize Kubernetes API clients.

    Loads the kubeconfig file and creates API client instances for Core V1
    (pods, namespaces, services) and Apps V1 (deployments, statefulsets).

    Returns:
        Tuple containing (CoreV1Api client, AppsV1Api client, error_message):
        - On success: (CoreV1Api instance, AppsV1Api instance, "")
        - On failure: (None, None, "error description")
    """
    try:
        if not os.path.exists(kube_config_path):
            return None, None, "Kubeconfig file not found"

        config.load_kube_config(kube_config_path)
        v1 = client.CoreV1Api()
        a1 = client.AppsV1Api()
        return v1, a1, ""
    except ConfigException as e:
        return None, None, f"Invalid kubeconfig: {str(e)}"
    except Exception as e:
        return None, None, f"Error loading Kubernetes config: {str(e)}"


def load_credentials() -> dict[str, Any] | None:
    """Load user credentials from YAML file.

    Returns:
        Dictionary containing user credentials, or None if loading fails.
    """
    try:
        if not os.path.exists(credential_config_path):
            return None

        with open(credential_config_path) as credential_conf_file:
            credential_config_dict = yaml.load(credential_conf_file, Loader=SafeLoader)
        return credential_config_dict
    except Exception:
        return None


def render_login_page(authenticator: stauth.Authenticate) -> None:
    """Render centered login page for first-time users.

    Displays a clean, centered login form with application branding.
    Only shown when user is not authenticated.

    Args:
        authenticator: Streamlit authenticator instance.
    """
    # Application title with emoji
    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0.5rem;'>K8s Control Panel 🕵️‍♀️</h1>",
        unsafe_allow_html=True,
    )

    # Subtitle with white color for better contrast on dark backgrounds
    st.markdown(
        "<p style='text-align: center; color: #4a5568; font-size: 1.1em; margin-bottom: 0.5rem; font-weight: 500;'>Manage your Kubernetes cluster with ease</p>",
        unsafe_allow_html=True,
    )

    # Create centered columns for login widget
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Render login widget
        authenticator.login(location="main")

        # Check authentication status
        auth_status = st.session_state.get("authentication_status")
        if auth_status is False:
            st.error("Username/Password is Incorrect")
        elif auth_status is None:
            st.info("🔐 Please enter your credentials to access the control panel")


def render_main_interface(v1: client.CoreV1Api | None, a1: client.AppsV1Api | None, k8s_error: str) -> None:
    """Display the main application interface after successful authentication.

    Renders the main page with navigation tabs for Deployment Operations and
    Pod Operations. Shows configuration warnings if Kubernetes is not configured.

    Args:
        v1: Kubernetes Core V1 API client instance.
        a1: Kubernetes Apps V1 API client instance.
        k8s_error: Error message if Kubernetes configuration failed, empty string otherwise.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("streamlit : K8S Control Panel : main_page : Execution Start")

        # Sidebar with user info and navigation
        with st.sidebar:
            # User profile section with emoji
            st.markdown("### 👤 User Profile")
            user_name = st.session_state.get("name", "User")
            user_email = st.session_state.get("username", "")
            st.write(f"**Name:** {user_name}")
            st.write(f"**Email:** {user_email}")
            st.divider()

            # Logout button
            st.markdown("### 🔒 Session")
            if st.button("Logout", use_container_width=True, type="secondary"):
                # Clear authentication session state
                st.session_state.authentication_status = False
                st.session_state.name = None
                st.session_state.username = None
                st.rerun()

            st.divider()

            # Quick Tips & Tricks (random on each reload)
            render_tips_section()

        # Show Kubernetes configuration warning if needed
        if k8s_error:
            st.warning(f"Kubeconfig Error: {k8s_error}")
            st.info(
                "Please configure your Kubernetes cluster by adding the kubeconfig file to "
                f"`{kube_config_path}`. Until then, dropdown menus will be empty."
            )

        # Application title with centered alignment and emoji
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 2rem;'>K8s Control Panel Dashboard 🕵️‍♀️</h1>",
            unsafe_allow_html=True,
        )

        # Navigation menu for different operation tabs
        selected_tab = option_menu(
            None,
            ["Deployment Operations", "Pod Operations", "Documentation"],
            icons=["hdd-stack", "window-stack", "book"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )

        # Display appropriate page based on selection
        if selected_tab == "Deployment Operations":
            deployment_page(
                v1=v1,
                a1=a1,
                k8s_error=k8s_error,
            )
        elif selected_tab == "Pod Operations":
            pod_page(
                v1=v1,
                a1=a1,
                k8s_error=k8s_error,
            )
        elif selected_tab == "Documentation":
            render_documentation_page()

        # Render footer on ALL pages
        render_footer()

        logger.info("streamlit : K8S Control Panel : main_page : Execution End")

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : main_page : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : main_page : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)


def main() -> None:
    """Main entry point for the K8s Control Panel application.

    Orchestrates the complete application flow:
    1. Load configuration and initialize logging
    2. Initialize Kubernetes clients
    3. Load credentials and authenticate user
    4. Render login page OR main interface based on auth status
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("streamlit : K8S Control Panel : main : Execution Start")

        # Initialize logging
        setup_logging(level="INFO", log_file="logs/app.log")

        # Load Kubernetes clients
        v1, a1, k8s_error = load_kubernetes_clients()
        if k8s_error:
            logger.warning(f"Kubernetes configuration failed: {k8s_error}")
        else:
            logger.info("Kubernetes clients loaded successfully")

        # Load credentials for authentication
        credential_config_dict = load_credentials()

        # Check if we can proceed with authentication
        if credential_config_dict is None:
            st.error(
                f"Credential file not found at `{credential_config_path}`. "
                "Please configure user authentication first."
            )
            st.info(
                "See README.md section 'Step 3: Set Up User Authentication' for instructions."
            )
            logger.info("streamlit : K8S Control Panel : main : Execution End")
            return

        # Instantiate authenticator (streamlit-authenticator >= 0.4.0)
        authenticator = stauth.Authenticate(
            credential_config_dict["credentials"],
            credential_config_dict["cookie"]["name"],
            credential_config_dict["cookie"]["key"],
            credential_config_dict["cookie"]["expiry_days"],
        )

        # Check if user is already authenticated
        auth_status = st.session_state.get("authentication_status")

        if auth_status:
            # User is authenticated - show main interface ONLY
            render_main_interface(v1=v1, a1=a1, k8s_error=k8s_error)
        else:
            # User not authenticated - show ONLY login page
            render_login_page(authenticator)

        logger.info("streamlit : K8S Control Panel : main : Execution End")

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(f"streamlit : K8S Control Panel : main : Exception : {str(exe)}")
        logger.error(
            f"streamlit : K8S Control Panel : main : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)


if __name__ == "__main__":
    main()
