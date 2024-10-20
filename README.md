Here’s the updated and visually engaging README with the changes you requested:

---

# 🌐 Intranet Monitoring System

## 📋 Overview
The **Intranet Monitoring System** is a secure, domain-based application designed to **monitor and collect critical device information** from users within an intranet. Seamlessly integrating into an existing web portal, it ensures all devices are compliant with internal security policies. Upon login, the system checks for data reception from the device. If no data is detected, it automatically installs the application on the user’s device, gathering and transmitting hardware and software information to the server securely.

> **Designed for government organizations** to protect sensitive internal devices and prevent external applications from accessing company data.

---

## 🚀 Key Features
- **Device Data Monitoring**: Verifies if device information is sent to the web portal and stores it in the database.
- **Automatic Installation**: If the application is missing, it installs automatically, ensuring **zero friction** for the user.
- **Data Collection**: Gathers important information:
  - Device Name, Make, Model, OS, OS Model
  - IP Address, MAC Address, and other network details
  - Installed Applications
  - Hardware Specifications (CPU, RAM, Disk Space)
- **Secure Data Transmission**: Sends data securely to the server via a **REST API**.
- **Startup Execution**: Configured to run at startup, ensuring regular data updates.
- **Security Compliance**: Blocks unauthorized external applications from accessing the system, reducing the risk of data breaches.

---

## 🖥️ Use Case
This monitoring system is built for **internal use by government organizations**. It empowers IT administrators to keep track of all devices within the intranet, ensuring compliance with security standards. By operating strictly within the internal network, it provides a controlled and secure environment for device data collection and management.

---

## 🔧 Installation

### Prerequisites:
- Device must be connected to the **domain network**.
- The **web portal** must be accessible.
- **Admin privileges** may be required for installation.

### Automatic Installation:
1. **Login** to the web portal.
2. The system checks for device data.
3. If no data is found, the app installs automatically.
4. The application starts collecting and sending device information.

### Manual Installation (Optional):
- Download the installer from the portal.
- Run the installer manually.
- The application will start transmitting device data immediately.

---

## 📊 Data Collection Process

1. **Login**: The system checks for device data during user login.
2. **Data Transmission**: Collects the following information:
   - **Device Information**: Device name, make, model, OS, OS model
   - **Network Information**: IP address, MAC address, etc.
   - **Installed Applications**: A list of all installed software
   - **Hardware Specifications**: Details such as CPU, RAM, and available disk space
3. **Database Storage**: All collected data is securely transmitted and stored in the central database.
4. **Data Security**: Ensures all transmissions are encrypted and limited to the intranet for enhanced security.

---

## ⚙️ Technologies Used
- **Backend**: ASP.NET WebForms
- **Client-side**: Python for cross-platform compatibility (Windows & Linux)
- **Database**: SQL Server for secure data storage
- **REST API**: Facilitates secure data transmission
- **Cross-Platform**: Works on Windows and Linux devices across the domain.

---

## 🔐 Security Considerations
- **Intranet-Only**: Communication is limited to the internal network.
- **No External Applications**: Prevents external software from compromising security.
- **Data Encryption**: All data transfers are encrypted for added security.

---

## 🔄 Deployment & Maintenance
- **Automatic Deployment**: Installs automatically via the web portal, requiring no user input.
- **Maintenance**: IT admins can manage updates and ensure the application evolves with security needs.

---

## ⚖️ License
This project is for **internal use only** by government organizations. It is not intended for public release or use outside internal operations.
