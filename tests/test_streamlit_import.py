"""Step 11 — verify Streamlit app imports."""


def test_streamlit_modules_import() -> None:
    import streamlit_app  # noqa: F401
    import ui.common  # noqa: F401
