# Suicide Prevention: A Therapy ChatBot
### Developed By: Deepalakshmi T

## Overview

Suicide Prevention: A Therapy ChatBot is an innovative therapy chatbot designed to provide immediate, empathetic support for individuals experiencing emotional distress or suicidal thoughts.

## Purpose

The chatbot serves as a first line of defense in suicide prevention, offering a safe space for users to express their feelings and receive guidance. Its primary goal is to reduce the risk of suicide by providing support and directing users to appropriate resources.

## Capabilities

- **Emotional Support**: Engages users in therapeutic conversations to explore their feelings and provide comfort.
- **Crisis Detection**: Utilizes advanced algorithms to detect signs of suicidal ideation and trigger alerts.
- **Immediate Assistance**: Offers strategies and techniques to help users cope with their immediate emotional state.
- **Resource Connection**: Guides users to professional help and emergency services when necessary.

## Impact

Suicide Prevention: A Therapy ChatBot aims to make mental health support more accessible and immediate, potentially saving lives by connecting users with the help they need when they need it most.

For more information on how Suicide Prevention: A Therapy ChatBot is transforming mental health support, please refer to the detailed sections within this README.

# Key Packages

1) langchain - Seems to be a custom or specialized library, given the multiple modules imported from it (like vectorstores, embeddings, llms, and chains).
2) chainlit - Chainlit is an open-source asynchronous Python framework that enables developers to build scalable Conversational AI or agentic applications quickly and efficiently.

# Setup

### Clone the repository

### Install required dependencies

pip install -r requirements.txt

### Start the ChatBot

python -m chainlit run model.py

# Requirements

To run this project, you will need the following packages:

Make sure to install these packages using `pip` before running the project.

# Workflow

This section outlines the workflow of our therapy chatbot, designed to provide support and prevent suicidal attempts. The workflow is divided into several key stages:

### User Interaction
- Users begin by interacting with the chatbot through a conversational interface.
- The chatbot utilizes natural language processing to understand and respond to user inputs.

![alt text](image.png)

### Assistance and Support
- The chatbot provides empathetic responses and engages users in therapeutic conversations.
- It offers guidance and support based on the user's expressed emotions and concerns.

![alt text](image-1.png)

### Alert Mechanism

- Upon detecting potential suicidal intent, the chatbot triggers an automated alert system.
- An email notification is sent to a designated organization for immediate human intervention.

<img width="771" alt="image" src="https://github.com/user-attachments/assets/7bd94fe6-9ef8-47cc-a836-616aa6d431cd" />


### Follow-Up

- The organization can then reach out to the user to provide further assistance and resources.
- The chatbot also provides information on how to access professional help and emergency services.

### Continuous Improvement

- User interactions are analyzed to improve the chatbot's responses and detection capabilities.
- Feedback loops are established to refine the system and enhance its effectiveness.

# Role of Vector Database

A **Vector Database** is a specialized database designed to store, manage, and index high-dimensional vector data efficiently. These vectors, also known as embeddings, are numerical representations of data objects that carry semantic information.

In our therapy chatbot, the vector database plays a crucial role in understanding and processing user inputs. By converting text into vector embeddings, the chatbot can analyze the conversation's context, detect crisis situations, and provide relevant and personalized support to the user.

The use of a vector database ensures that our chatbot responds with high accuracy and relevance, making it a vital component in our mission to offer timely assistance and prevent suicidal attempts.

This workflow ensures that users receive timely and appropriate support, while also facilitating human intervention when necessary.

Conclusion















