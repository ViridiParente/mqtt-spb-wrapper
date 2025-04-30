from setuptools import setup, find_packages

setup(
    name="mqtt_spb_wrapper",
    version="2.0.3",
    description="MQTT Sparkplug B v1.0 Wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Javier FG",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "paho-mqtt==1.6.1",
        "protobuf==3.20.3",
    ],
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=["sparkplug", "mqtt", "ecliplse", "tahu", "iiot", "iot"],
    url="https://github.com/javier-fg/mqtt-spb-wrapper",
)
