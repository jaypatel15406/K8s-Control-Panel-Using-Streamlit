"""
Common Footer Component for K8s Control Panel.

This module provides a reusable footer component that displays social media links
and copyright information across all pages of the application.

Features:
    - Dynamic current year display
    - Social media badges (GitHub, LinkedIn, Twitter, Instagram, Email)
    - Consistent styling across all pages
    - Gradient background design
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st


def get_current_year() -> int:
    """Get the current year for copyright display.

    Returns:
        Current year as integer.
    """
    return datetime.now().year


def render_footer() -> None:
    """Render the full application footer with social media links and copyright.

    Displays a styled footer containing:
    - Social media badges (GitHub, LinkedIn, Twitter, Instagram, Email)
    - Copyright message with current year
    - License information

    Use this on ALL pages for consistent footer display.
    """
    current_year = get_current_year()

    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin-top: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    '>
        <h4 style='color: white; margin-bottom: 15px; font-size: 1.1em;'>Connect & Contribute</h4>
        <div style='margin: 15px 0;'>
            <a href='https://github.com/jaypatel15406' 
               target='_blank' 
               style='text-decoration: none; display: inline-block; margin: 5px;'>
                <img src='https://img.shields.io/badge/GitHub-jaypatel15406-181717?style=for-the-badge&logo=github&logoColor=white' 
                     alt='GitHub' 
                     style='height: 32px;'>
            </a>
            <a href='https://www.linkedin.com/in/jaypatel15406' 
               target='_blank' 
               style='text-decoration: none; display: inline-block; margin: 5px;'>
                <img src='https://img.shields.io/badge/LinkedIn-jaypatel15406-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white' 
                     alt='LinkedIn' 
                     style='height: 32px;'>
            </a>
            <a href='https://twitter.com/jaypatel15406' 
               target='_blank' 
               style='text-decoration: none; display: inline-block; margin: 5px;'>
                <img src='https://img.shields.io/badge/Twitter-jaypatel15406-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white' 
                     alt='Twitter' 
                     style='height: 32px;'>
            </a>
            <a href='https://instagram.com/jaypatel15406' 
               target='_blank' 
               style='text-decoration: none; display: inline-block; margin: 5px;'>
                <img src='https://img.shields.io/badge/Instagram-jaypatel15406-E4405F?style=for-the-badge&logo=instagram&logoColor=white' 
                     alt='Instagram' 
                     style='height: 32px;'>
            </a>
            <a href='mailto:jaypatel15406@gmail.com' 
               target='_blank' 
               style='text-decoration: none; display: inline-block; margin: 5px;'>
                <img src='https://img.shields.io/badge/Email-jaypatel15406@gmail.com-D44638?style=for-the-badge&logo=gmail&logoColor=white' 
                     alt='Email' 
                     style='height: 32px;'>
            </a>
        </div>
        <hr style='border-color: rgba(255,255,255,0.3); margin: 15px 0;'>
        <p style='color: rgba(255,255,255,0.9); font-size: 0.9em; margin: 8px 0;'>
            &copy; {current_year} K8s Control Panel. Built with ❤️ using Streamlit & Kubernetes
        </p>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.85em; margin: 5px 0;'>
            Licensed under MIT License
        </p>
    </div>
    """, unsafe_allow_html=True)
