"""
Documentation Page Module for K8s Control Panel.

This module provides comprehensive documentation for the K8s Control Panel application,
including setup instructions, architecture overview, cloud provider configuration guides,
and security best practices.

Features:
    - Application overview and features
    - Architecture diagrams (centered)
    - Cloud provider-specific setup guides (AWS, GCP, Azure) - displayed side-by-side
    - OS-specific installation guides (Windows, macOS, Linux)
    - Security best practices
    - Troubleshooting guide
"""

from __future__ import annotations

import streamlit as st


def render_cloud_provider_section() -> None:
    """Render cloud provider configuration in side-by-side columns.

    Creates three columns for AWS EKS, GCP GKE, and Azure AKS configuration
    displayed side-by-side with SVG logos and clean styling.
    """
    st.markdown("### Cloud Provider Configuration")
    st.info("Select your cloud provider below for specific setup instructions:")
    
    # Create three columns for side-by-side display
    aws_col, gcp_col, azure_col = st.columns(3)
    
    with aws_col:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%); padding: 25px; border-radius: 12px; margin: 10px 0; border: 1px solid #b3d9ff; height: 100%;'>
            <div style='text-align: center; margin-bottom: 20px;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg' 
                     alt='AWS Logo' 
                     style='height: 60px; margin-bottom: 10px;'>
                <h4 style='color: #FF9900; font-size: 1.2em; margin: 10px 0;'>Amazon EKS</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
**Prerequisites:**
- AWS CLI installed
- IAM Authenticator
- EKS cluster created

**Generate Kubeconfig:**
```bash
aws eks update-kubeconfig \\
  --name <cluster_name> \\
  --region <region_name>
```

**Copy to Application:**
```bash
cp ~/.kube/config config/k8sconfig.txt
```
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with gcp_col:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e8f4fd 0%, #d4ebfa 100%); padding: 25px; border-radius: 12px; margin: 10px 0; border: 1px solid #a8d8f5; height: 100%;'>
            <div style='text-align: center; margin-bottom: 20px;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg' 
                     alt='GCP Logo' 
                     style='height: 60px; margin-bottom: 10px;'>
                <h4 style='color: #4285F4; font-size: 1.2em; margin: 10px 0;'>Google GKE</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
**Prerequisites:**
- Google Cloud SDK
- GKE cluster created
- kubectl installed

**Generate Kubeconfig:**
```bash
gcloud container clusters \\
  get-credentials <cluster_name> \\
  --zone <zone_name>
```

**Copy to Application:**
```bash
cp ~/.kube/config config/k8sconfig.txt
```
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with azure_col:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f4ff 0%, #e6ecff 100%); padding: 25px; border-radius: 12px; margin: 10px 0; border: 1px solid #c4d4ff; height: 100%;'>
            <div style='text-align: center; margin-bottom: 20px;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/a/a8/Microsoft_Azure_Logo.svg' 
                     alt='Azure Logo' 
                     style='height: 60px; margin-bottom: 10px;'>
                <h4 style='color: #0078D4; font-size: 1.2em; margin: 10px 0;'>Azure AKS</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
**Prerequisites:**
- Azure CLI installed
- AKS cluster created
- kubectl installed

**Generate Kubeconfig:**
```bash
az aks get-credentials \\
  --resource-group <rg_name> \\
  --name <cluster_name>
```

**Copy to Application:**
```bash
cp ~/.kube/config config/k8sconfig.txt
```
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_os_installation_tabs() -> None:
    """Render OS-specific installation instructions in tabs.

    Creates tabs for Windows, macOS, and Linux with specific installation commands
    for each operating system.
    """
    st.markdown("### Installation by Operating System")
    
    win_tab, mac_tab, linux_tab = st.tabs(["Windows", "macOS", "Linux"])
    
    with win_tab:
        st.markdown("""
#### Windows Installation Guide

**Step 1: Install Python**
```powershell
# Download from https://www.python.org/downloads/
# Or use winget
winget install Python.Python.3.12
```

**Step 2: Create Virtual Environment**
```powershell
python -m venv venv
venv\\Scripts\\activate
```

**Step 3: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 4: Install kubectl**
```powershell
choco install kubernetes-cli
# Or download from: https://kubernetes.io/docs/tasks/tools/
```

**Step 5: Run Application**
```powershell
python -m streamlit run main_application.py
```

**Note:** Windows users may need to run PowerShell as Administrator for some commands.
        """)
    
    with mac_tab:
        st.markdown("""
#### macOS Installation Guide

**Step 1: Install Python**
```bash
# Python 3.10+ is usually pre-installed
# Or install latest version
brew install python@3.12
```

**Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Install kubectl**
```bash
brew install kubectl
```

**Step 5: Run Application**
```bash
python -m streamlit run main_application.py
```

**Note:** macOS users may need to allow the app in System Preferences > Security & Privacy.
        """)
    
    with linux_tab:
        st.markdown("""
#### Linux Installation Guide

**Step 1: Install Python**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip

# RHEL/CentOS/Fedora
sudo dnf install python3 python3-venv python3-pip
```

**Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Install kubectl**
```bash
# Download latest
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Step 5: Run Application**
```bash
python -m streamlit run main_application.py
```

**Note:** Linux users may need to install additional dependencies based on their distribution.
        """)


def render_architecture_section() -> None:
    """Render architecture section with centered diagram.

    Displays a text-based architecture diagram that is properly centered
    and formatted for readability.
    """
    st.markdown("### Architecture")
    
    # Center the architecture title and diagram using columns
    _, center_col, _ = st.columns([0.25, 0.5, 0.25])
    with center_col:
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <h4 style='color: #4a5568; margin-bottom: 15px;'>System Architecture Overview</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
The K8s Control Panel follows a layered architecture:

```
┌─────────────────────────────────────────────────┐
│              User Browser Layer                 │
│         (Streamlit Web Interface)               │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│           Application Layer                     │
│  ┌──────────┬──────────────┬──────────────┐    │
│  │Authentication│   UI     │  Navigation  │    │
│  │   Module   │ Components │    System    │    │
│  └──────────┴──────────────┴──────────────┘    │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│         Business Logic Layer                    │
│  ┌──────────────────┬──────────────────────┐   │
│  │  Deployment      │     Pod Operations   │   │
│  │  Operations      │                      │   │
│  └──────────────────┴──────────────────────┘   │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│         Infrastructure Layer                    │
│  ┌──────────────────┬──────────────────────┐   │
│  │  Kubernetes      │   Kubernetes Cluster │   │
│  │  Python Client   │   (Your Cluster)     │   │
│  └──────────────────┴──────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Architecture Flow:**

1. **User** accesses the web interface via browser
2. **Authentication Module** validates credentials
3. **UI Components** render the dashboard
4. **Business Logic** processes user operations
5. **Kubernetes Client** communicates with your cluster
6. **Cluster** executes the requested operations

> **Note:** For visual architecture diagrams, please refer to the 
> [README.md](https://github.com/jaypatel15406/K8s-Control-Panel-Using-Streamlit/blob/main/README.md)
> file in the repository.
    """)


def render_troubleshooting_section() -> None:
    """Render troubleshooting section with clean formatting.

    Displays common issues and solutions in a clean, readable format
    using Streamlit's native components instead of raw HTML.
    """
    st.markdown("### Troubleshooting")
    
    st.markdown("""
Below are common issues and their solutions:
    """)
    
    # Issue 1
    with st.expander("**Application Shows 'Credential file not found'**"):
        st.markdown("""
**Problem:** Error message about missing credential file

**Solution:**
1. Ensure `config/credential.yaml` exists
2. Verify the file is properly formatted YAML
3. Check file permissions

```bash
# Verify file exists
ls -la config/credential.yaml

# Test YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/credential.yaml'))"
```
        """)
    
    # Issue 2
    with st.expander("**'Kubeconfig file not found' Warning**"):
        st.markdown("""
**Problem:** Warning about missing kubeconfig

**Solution:**
1. Copy your kubeconfig to the application
2. Verify the file is named correctly

```bash
# Copy kubeconfig
cp ~/.kube/config config/k8sconfig.txt

# Verify
ls -la config/k8sconfig.txt
```
        """)
    
    # Issue 3
    with st.expander("**Login Widget Not Appearing**"):
        st.markdown("""
**Problem:** Login form doesn't show up

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete / Cmd+Shift+Delete)
2. Refresh the page (F5 / Cmd+R)
3. Try incognito/private browsing mode
4. Check browser console for errors (F12)
        """)
    
    # Issue 4
    with st.expander("**'Invalid kubeconfig' Error**"):
        st.markdown("""
**Problem:** Error about invalid kubeconfig file

**Solution:**
1. Test kubeconfig with kubectl
2. Regenerate if necessary

```bash
# Test kubeconfig
kubectl --kubeconfig=config/k8sconfig.txt get namespaces

# If this fails, regenerate using your cloud provider CLI
# AWS: aws eks update-kubeconfig --name <cluster> --region <region>
# GCP: gcloud container clusters get-credentials <cluster> --zone <zone>
# Azure: az aks get-credentials --resource-group <rg> --name <cluster>
```
        """)
    
    # Issue 5
    with st.expander("**Dropdown Shows No Namespaces**"):
        st.markdown("""
**Problem:** Namespace dropdown is empty

**Solution:**
1. Verify cluster connection
2. Check RBAC permissions
3. Ensure correct context is set

```bash
# Check cluster connection
kubectl cluster-info

# Check current context
kubectl config current-context

# List available contexts
kubectl config get-contexts

# Switch context if needed
kubectl config use-context <context-name>
```
        """)
    
    # Issue 6
    with st.expander("**Application Won't Start**"):
        st.markdown("""
**Problem:** Application fails to start

**Solution:**
1. Check Python version (3.10 - 3.13 required)
2. Verify all dependencies are installed
3. Check logs for errors

```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check logs
cat logs/app.log
```
        """)
    
    st.info("""
**Still having issues?**

- Check the application logs: `tail -f logs/app.log`
- Search for errors: `grep "ERROR" logs/app.log`
- Open an issue on GitHub with error details
    """)


def render_documentation_page() -> None:
    """Render the complete documentation page.

    Displays comprehensive documentation including:
    - Application overview
    - Architecture information
    - Cloud provider configuration (side-by-side)
    - OS-specific installation guides
    - Security guidelines
    - Troubleshooting tips
    """

    # Page title - matching style with Pod/Deployment operations pages
    st.markdown("### Documentation")
    st.markdown("Complete setup guide and reference documentation")

    st.divider()

    # Overview Section
    st.markdown("### Overview")

    st.markdown("""
**K8s Control Panel** is a Streamlit-based web interface for managing Kubernetes deployments and pods
without requiring direct `kubectl` command usage. It provides an intuitive graphical interface for
common Kubernetes operations.

**Key Features:**

| Feature | Description |
|---------|-------------|
| User Authentication | Secure login with bcrypt password hashing |
| Deployment Scaling | Scale deployments up or down with a click |
| Pod Management | Delete pods and manage resources |
| Namespace Selection | Easy namespace switching |
| Comprehensive Logging | Full audit trail of all operations |
| Graceful Degradation | UI loads even without Kubernetes configuration |
    """)

    st.divider()

    # Architecture Section
    render_architecture_section()

    st.divider()

    # Prerequisites Section
    st.markdown("### Prerequisites")

    st.markdown("""
**System Requirements:**

| Component | Version | Description |
|-----------|---------|-------------|
| Python | 3.10 - 3.13 | Required runtime environment |
| pip | 22.0+ | Python package installer |
| Kubernetes Cluster | 1.28+ | Target cluster for operations |
| kubectl | 1.28+ | For kubeconfig generation |
| Git | 2.30+ | For cloning the repository |

**Required Python Packages:**

```bash
streamlit>=1.42.0,<2.0.0
kubernetes>=31.0.0,<32.0.0
streamlit-authenticator>=0.4.0,<1.0.0
streamlit-option-menu>=0.3.13,<1.0.0
PyYAML>=6.0.2,<7.0.0
Pillow>=11.0.0,<12.0.0
```
    """)

    st.divider()

    # Installation Section
    st.markdown("### Installation")

    st.markdown("""
**Quick Start:**

```bash
# Clone the repository
git clone https://github.com/jaypatel15406/K8s-Control-Panel-Using-Streamlit.git
cd K8s-Control-Panel-Using-Streamlit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\\Scripts\\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

For OS-specific instructions, see the tabs below.
    """)

    # OS-specific installation tabs
    render_os_installation_tabs()

    st.divider()

    # Cloud Configuration Section
    render_cloud_provider_section()

    st.divider()

    # User Authentication Section
    st.markdown("### User Authentication Setup")

    st.markdown("""
**Step 1: Configure Initial Password**

Edit `config/config.json`:

```json
{
    "decrypted_password_jay_user": "your_secure_password",
    "password_hashing_flag": "True"
}
```

**Step 2: Generate Hashed Password**

Run the application:

```bash
python -m streamlit run main_application.py
```

The terminal will display a hashed password.

**Step 3: Update Credentials File**

Edit `config/credential.yaml` and paste the hashed password.

**Step 4: Disable Password Hashing**

Edit `config/config.json`:

```json
{
    "password_hashing_flag": "False"
}
```

**Step 5: Restart Application**

```bash
python -m streamlit run main_application.py
```
    """)

    st.divider()

    # Security Section
    st.markdown("### Security Best Practices")

    st.markdown("""
**Kubeconfig Security:**

- **Never commit** `k8sconfig.txt` to version control
- Use service accounts with **minimal RBAC permissions**
- **Rotate credentials** regularly
- Store kubeconfig in **encrypted storage** for production

**Password Security:**

- Use **strong, unique passwords** (minimum 12 characters)
- Enable `password_hashing_flag` **only during initial setup**
- Change passwords **periodically**
- Never share plain-text passwords

**Network Security:**

- Run application **behind firewall** for production use
- Use **HTTPS** in production
- Restrict access to **trusted IPs**
- Monitor access logs regularly

**Recommended RBAC Configuration:**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: k8s-control-panel
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: k8s-control-panel-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods", "namespaces"]
  verbs: ["get", "list", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: k8s-control-panel-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: k8s-control-panel
roleRef:
  kind: Role
  name: k8s-control-panel-role
  apiGroup: rbac.authorization.k8s.io
```
    """)

    st.divider()

    # Troubleshooting Section
    render_troubleshooting_section()
