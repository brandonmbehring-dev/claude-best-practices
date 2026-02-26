"""Install the WarmTol Pygments style for minted code highlighting."""
from setuptools import setup

setup(
    name="warmtol-pygments",
    version="1.0.0",
    description="Warm Tol Hybrid Pygments style for Claude Best Practices guide",
    py_modules=["warmtol"],
    entry_points={
        "pygments.styles": [
            "warmtol = warmtol:WarmTolStyle",
        ],
    },
    install_requires=["Pygments"],
)
