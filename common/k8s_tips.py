"""
Kubernetes Tips and Tricks Module for K8s Control Panel.

This module provides a collection of Kubernetes tips, tricks, and best practices
that are randomly displayed in the sidebar to help users learn Kubernetes.

Features:
    - Rotating tips on each page reload
    - Best practices for deployments, pods, and general K8s usage
    - Professional, concise tips with explanations
"""

from __future__ import annotations

import random

import streamlit as st

# Kubernetes Tips and Tricks Collection (20 tips with explanations)
K8S_TIPS = [
    # Core Philosophy
    (
        "Don't treat Kubernetes like Docker++",
        "If you're only running one container, Kubernetes is basically a very expensive docker run."
    ),
    (
        "kubectl describe is your therapist",
        "When something breaks, it calmly explains everything you did wrong."
    ),
    (
        "Use kubectl get pods -A first",
        "Before debugging anything, confirm the pod actually exists... many engineers skip this step."
    ),
    
    # Labels and Namespaces
    (
        "Labels are Kubernetes' love language",
        "Without good labels, selectors will ghost your pods."
    ),
    (
        "Namespaces = apartments for pods",
        "Everyone shares the same building (cluster), but at least the neighbors can't steal your configs."
    ),
    
    # Safety First
    (
        "Never debug production with kubectl delete",
        "Kubernetes will happily comply with your bad decisions."
    ),
    (
        "Use readiness probes",
        "Otherwise Kubernetes sends traffic to your app while it's still waking up like a Monday morning developer."
    ),
    (
        "Use resource limits wisely",
        "Too low → throttling; too high → one pod becomes the office food thief."
    ),
    
    # Configuration Management
    (
        "ConfigMaps for configs, Secrets for secrets",
        "If your passwords live in ConfigMaps, congratulations: your cluster runs on vibes."
    ),
    (
        "Pods are disposable, not pets",
        "If you're SSH-ing into pods to fix things, Kubernetes is quietly judging you."
    ),
    
    # Scaling and Reliability
    (
        "ReplicaSets are your safety net",
        "Kill a pod and Kubernetes spawns another like a hydra head."
    ),
    (
        "Use Horizontal Pod Autoscaler (HPA)",
        "Because manually scaling pods is basically cloud caveman behavior."
    ),
    
    # Debugging
    (
        "Always check kubectl logs before panicking",
        "80% of the time the app literally prints the problem."
    ),
    (
        "kubectl port-forward is the developer VPN",
        "Perfect for debugging without opening the cluster to the entire internet."
    ),
    (
        "CrashLoopBackOff means your app is practicing failure repeatedly",
        "Kubernetes keeps retrying, hoping you eventually fix the bug."
    ),
    
    # Best Practices
    (
        "Helm charts: copy-paste engineering, but organized",
        "It's YAML... but now with reusable chaos."
    ),
    (
        "Avoid giant YAML files",
        "If your manifest scrolls for miles, future-you will file a complaint."
    ),
    (
        "Keep kubectl explain in your toolbox",
        "It's like Kubernetes documentation... but actually useful."
    ),
    (
        "Use kubectl diff before applying changes",
        "Prevents the classic 'why did production explode?' moment."
    ),
    (
        "Remember: Kubernetes doesn't fix bad architecture",
        "It just distributes the bad architecture across many nodes."
    ),
]


def get_random_tip() -> tuple[str, str]:
    """Get a random Kubernetes tip from the collection.

    Returns:
        A tuple containing (tip_title, tip_explanation).
    """
    return random.choice(K8S_TIPS)


def render_tips_section() -> None:
    """Render the Quick Tips and Tricks section in sidebar.

    Displays a randomly selected Kubernetes tip with explanation each time
    the sidebar is loaded. Uses Streamlit's components for consistent styling.
    """
    tip_title, tip_explanation = get_random_tip()

    st.markdown("### 💡 Quick Tips & Tricks")
    
    # Display tip title in bold
    st.markdown(f"**{tip_title}**")
    
    # Display explanation in a subtle info box
    st.info(tip_explanation)

    st.caption(
        "Tip changes each time you open the sidebar"
    )
