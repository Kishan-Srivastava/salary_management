"""Shared Streamlit styling."""

from __future__ import annotations

import streamlit as st


def inject_app_theme() -> None:
    """Global dashboard styles (call once from streamlit_app)."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', system-ui, sans-serif;
        }

        /* Sidebar polish */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        [data-testid="stSidebar"] .stCaption {
            color: #94a3b8 !important;
        }

        /* Main padding */
        .block-container {
            padding-top: 1.5rem;
            max-width: 1200px;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        }
        div[data-testid="stMetric"] label {
            color: #64748b !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_home_styles() -> None:
    """Home page hero, feature grid, and accents."""
    st.markdown(
        """
        <style>
        .home-hero {
            position: relative;
            padding: 2.5rem 2rem 2rem 2rem;
            border-radius: 20px;
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 45%, #7c3aed 100%);
            color: #f8fafc;
            overflow: hidden;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 50px -12px rgba(29, 78, 216, 0.45);
        }
        .home-hero::before {
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
            border-radius: 50%;
        }
        .home-hero::after {
            content: "";
            position: absolute;
            bottom: -30%;
            left: 5%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(124,58,237,0.4) 0%, transparent 70%);
            border-radius: 50%;
        }
        .home-hero h1 {
            font-size: 2.4rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.02em;
            position: relative;
            z-index: 1;
        }
        .home-hero p {
            font-size: 1.1rem;
            opacity: 0.92;
            margin: 0;
            max-width: 36rem;
            line-height: 1.5;
            position: relative;
            z-index: 1;
        }
        .home-badge {
            display: inline-block;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.25);
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
            backdrop-filter: blur(8px);
            position: relative;
            z-index: 1;
        }

        .feature-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem 1.35rem;
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        }
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(29, 78, 216, 0.12);
            border-color: #93c5fd;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.6rem;
        }
        .feature-card h3 {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0 0 0.4rem 0;
        }
        .feature-card p {
            color: #64748b;
            font-size: 0.9rem;
            margin: 0;
            line-height: 1.45;
        }

        .quick-tip {
            background: linear-gradient(90deg, #eff6ff 0%, #f5f3ff 100%);
            border-left: 4px solid #3b82f6;
            padding: 1rem 1.25rem;
            border-radius: 0 12px 12px 0;
            color: #334155;
            font-size: 0.95rem;
            margin-top: 1rem;
        }
        .api-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 0.4rem 0.9rem;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #475569;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }
        .status-dot.ok { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
        .status-dot.err { background: #ef4444; box-shadow: 0 0 8px #ef4444; }
        </style>
        """,
        unsafe_allow_html=True,
    )
