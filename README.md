# GCloud Xano Optimization for Hermione - App Enos  

## Overview  

This repository contains a set of Google Cloud Functions designed to optimize the data flows of a **Xano** backend for the **Bubble** app **Enos**, part of project **Hermione**. These functions handle various automation tasks such as data transformation, stock updates, and validation processes.  

## Structure  

- **gcloud-json-to-csv**: Converts JSON data from Xano into CSV format for better compatibility with other systems.  
- **gcloud-lambda-articles**: Processes and optimizes article-related data before being consumed by the Bubble app.  
- **gcloud-lambda-tarifs**: Manages pricing updates and ensures synchronization between Xano and Bubble.  
- **gcloud-maj-stock**: Updates stock levels in real-time based on incoming data from Xano.  
- **gcloud-checkcsv**: Validates CSV files before importing them into the system to prevent inconsistencies.  

## Prerequisites  

- Google Cloud SDK installed  
- Node.js or Python (depending on the function requirements)  
- Xano API access  
- Bubble API keys (if required for direct communication)  

## Deployment  

1. Authenticate with Google Cloud:  
   ```sh
   gcloud auth login
   gcloud config set project [PROJECT_ID]
   ```
