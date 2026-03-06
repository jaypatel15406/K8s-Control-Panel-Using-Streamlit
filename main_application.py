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

# Import common components
from common.logging_config import setup_logging

# Set Page width to 'Wide'
st.set_page_config(layout="wide", menu_items={}, page_icon="media/K8s Control Panel.png")

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

    Reads the application configuration file and returns it as a dictionary.
    Returns None if configuration file is missing or invalid.

    Returns:
        Dictionary containing application configuration settings, or None if
        configuration cannot be loaded.
    """
    try:
        if not os.path.exists(app_config_path):
            logger = logging.getLogger(__name__)
            logger.warning(f"Configuration file not found: {app_config_path}")
            return None

        with open(app_config_path, "r", encoding="utf-8") as app_conf_file:
            app_conf_json_str = app_conf_file.read()
            app_config_dict = json.loads(app_conf_json_str)
        return app_config_dict
    except json.JSONDecodeError as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Invalid JSON in config file: {e}")
        return None
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading configuration: {e}")
        return None


def initialize_logging(app_config_dict: dict[str, Any] | None) -> None:
    """Initialize logging configuration from application settings.

    Sets up logging based on the logging_configurations section in config.json.
    Uses default settings if configuration is missing or None.

    Args:
        app_config_dict: Application configuration dictionary containing
                        logging_configurations section, or None.
    """
    if app_config_dict is None:
        setup_logging(level="INFO", log_file="logs/app.log")
        return

    logging_config = app_config_dict.get("logging_configurations", {})
    setup_logging(
        level=logging_config.get("level", "INFO"),
        log_file=logging_config.get("file", "logs/app.log"),
        max_bytes=logging_config.get("max_bytes", 5 * 1024 * 1024),
        backup_count=logging_config.get("backup_count", 3),
        log_format=logging_config.get("format"),
    )


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
            return None, None, f"Kubeconfig file not found: {kube_config_path}"

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
            logger = logging.getLogger(__name__)
            logger.warning(f"Credential file not found: {credential_config_path}")
            return None

        with open(credential_config_path) as credential_conf_file:
            credential_config_dict = yaml.load(credential_conf_file, Loader=SafeLoader)
        return credential_config_dict
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading credentials: {e}")
        return None


def user_login(authenticator: stauth.Authenticate) -> tuple[str | None, bool | None, str | None]:
    """Authenticate user before allowing Kubernetes cluster operations.

    Handles user authentication using streamlit-authenticator.

    Args:
        authenticator: Streamlit authenticator instance configured with
                      user credentials.

    Returns:
        Tuple containing (name, authentication_status, username):
        - name: User's display name if authenticated, None otherwise
        - authentication_status: True (success), False (failed), None (not attempted)
        - username: Authenticated username if successful, None otherwise
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("streamlit : K8S Control Panel : user_login : Execution Start")

        # Authenticate User using keyword argument for location (streamlit-authenticator >= 0.4.0)
        authenticator.login(location="main")

        # Get authentication status from session state
        name = st.session_state.get("name")
        authentication_status = st.session_state.get("authentication_status")
        username = st.session_state.get("username")

        logger.info(f"streamlit : K8S Control Panel : user_login : name : {name}")
        logger.info(
            f"streamlit : K8S Control Panel : user_login : authentication_status : {authentication_status}"
        )
        logger.info(f"streamlit : K8S Control Panel : username : {username}")
        logger.info("streamlit : K8S Control Panel : user_login : Execution End")

        return name, authentication_status, username

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(
            f"streamlit : K8S Control Panel : user_login : Exception : {str(exe)}"
        )
        logger.error(
            f"streamlit : K8S Control Panel : user_login : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)
        return None, None, None


def main_page(v1: client.CoreV1Api | None, a1: client.AppsV1Api | None, k8s_error: str) -> None:
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

        # Show warning if Kubernetes is not configured
        if k8s_error:
            st.warning(f"⚠️ {k8s_error}")
            st.info(
                "Please configure your Kubernetes cluster by adding the kubeconfig file to "
                f"`{kube_config_path}`. Until then, dropdown menus will be empty."
            )

        # Navigation menu for different operation tabs
        selected_tab = option_menu(
            None,
            ["Deployment Operations", "Pod Operations"],
            icons=["hdd-stack", "window-stack"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )

        # Open Pages based on the 'on-click' method
        if selected_tab == "Deployment Operations":
            deployment_page(v1=v1, a1=a1, k8s_error=k8s_error)
        if selected_tab == "Pod Operations":
            pod_page(v1=v1, a1=a1, k8s_error=k8s_error)

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

    Orchestrates the application flow:
    1. Load configuration and initialize logging
    2. Load Kubernetes API clients (with graceful error handling)
    3. Load credentials and authenticate user
    4. Display main interface or authentication prompts

    The function handles three authentication states:
    - Successful login: Proceed to main page
    - Failed login: Display error message
    - No attempt: Display login prompt
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info("streamlit : K8S Control Panel : main : Execution Start")

        # Load configuration and initialize logging
        app_config_dict = load_configuration()
        initialize_logging(app_config_dict)
        logger.info("Configuration loaded successfully")

        # Load Kubernetes clients (may fail gracefully)
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

        # Instantiate authenticator (updated for streamlit-authenticator >= 0.4.0)
        # Note: preauthorized parameter moved to register_user() in v0.4.0
        authenticator = stauth.Authenticate(
            credential_config_dict["credentials"],
            credential_config_dict["cookie"]["name"],
            credential_config_dict["cookie"]["key"],
            credential_config_dict["cookie"]["expiry_days"],
        )

        # Authenticate user
        name, authentication_status, username = user_login(authenticator)

        if authentication_status:
            main_page(v1=v1, a1=a1, k8s_error=k8s_error)
        elif authentication_status is False:
            st.error("Username/Password is Incorrect")
        elif authentication_status is None:
            st.warning("Please enter your 'Username' and 'Password'")

        logger.info("streamlit : K8S Control Panel : main : Execution End")

    except Exception as exe:
        logger = logging.getLogger(__name__)
        logger.error(f"streamlit : K8S Control Panel : main : Exception : {str(exe)}")
        logger.error(
            f"streamlit : K8S Control Panel : main : traceback : {traceback.format_exc()}"
        )
        st.exception(exe)


if __name__ == "__main__":
    # Title of the Application
    st.markdown(
        "<h1 style='text-align: center;'>Welcome to K8s Control Panel 🕵️‍♀️</h1>",
        unsafe_allow_html=True,
    )
    main()
