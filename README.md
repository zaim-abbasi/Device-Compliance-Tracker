# Intranet Monitoring System

## Overview
The **Intranet Monitoring System** is a secure, domain-based application designed to monitor and collect device information from users within an intranet. It integrates seamlessly into an existing web portal, ensuring that all devices on the network are compliant with internal security policies. The system verifies if data is being received from each device upon user login. If no data is detected, the system triggers an automatic installation of the application on the user's device, which then gathers and transmits essential hardware and software information to the server.

This project is specifically developed for government organizations to maintain the security of internal devices, preventing external applications from potentially stealing sensitive company information.

## Key Features
- **Device Data Monitoring**: The application checks if device information is being sent to the web portal upon user login. If data exists, it is stored in the database.
- **Automatic Installation**: If the application is not detected on the user's device, it will automatically install, minimizing user interaction and ensuring deployment across the domain.
- **Data Collection**: Once installed, the application collects critical data, including:
  - Device Name
  - MAC Address
  - Installed Applications
  - Hardware Specifications (e.g., CPU, RAM, Disk space)
- **Data Transmission**: The collected data is securely sent to the web portal via a REST API, where it is stored in a secure database for further analysis.
- **Startup Execution**: The application is configured to run at startup, ensuring that device information is regularly updated and transmitted to the server.
- **Security Compliance**: The system ensures that no external applications are installed or running on the devices, reducing the risk of data theft or leaks.

## Use Case
This monitoring system is tailored for internal use by government organizations, allowing IT administrators to monitor the devices within their intranet. The system helps ensure that all devices meet security requirements, with no external software threatening data integrity. By operating strictly within the internal network, the system provides a controlled and secure environment for data collection and storage.

## Installation

### Prerequisites
- The user’s device must be connected to the domain network.
- The web portal must be accessible from the device.
- Administrator privileges may be required to install the application on user devices (handled automatically through the installation process).

### Automatic Installation
- **Step 1**: Upon user login to the web portal, the system checks if device data is being received.
- **Step 2**: If no data is detected, the application will be automatically installed on the user's device.
- **Step 3**: The installation process runs silently, with minimal user interaction.
- **Step 4**: Once installed, the application begins collecting and transmitting device information to the web portal.

### Manual Installation (Optional)
In case of automatic installation failures or network issues:
1. Download the installation package from the web portal.
2. Run the installer manually on the device.
3. The application will start immediately upon installation and transmit device data to the server.

## Data Collection Process

1. **Login to Portal**: Each time a user logs into the web portal, the system verifies if the user’s device is sending data.
   - If device data is detected, it is checked against the existing records in the database.
   - If no data exists, the new data is stored in the database.

2. **Data Transmission**: If the application is installed on the device, it collects the following information:
   - **Device Name**: The name assigned to the device.
   - **MAC Address**: The device’s unique hardware identifier.
   - **Installed Applications**: A list of applications currently installed on the device.
   - **Hardware Specifications**: Detailed information about the device’s hardware, including CPU, RAM, and available disk space.

3. **Database Storage**: All collected data is securely transmitted via the REST API to the web portal and stored in a central database. The portal checks if this data already exists, preventing duplicates.

4. **Data Security**: This system is built with a focus on internal security, ensuring no external application or malicious software can access or steal sensitive information from the devices.

## Technologies Used

- **Backend**: ASP.NET WebForms for handling user authentication and web portal interaction.
- **Client-side Application**: Python, designed for cross-platform support on both Windows and Linux environments.
- **Database**: SQL Server for secure storage of collected device data.
- **REST API**: Used to transmit device data from the client application to the web portal.
- **Cross-Platform Support**: The client application is designed to run on both Windows and Linux devices, ensuring compatibility with a wide range of user devices within the domain.

## Security Considerations
This system is designed with security in mind:
- **Intranet-only operation**: The application communicates exclusively within the internal network (intranet), preventing exposure to the external internet.
- **No external applications**: Ensures that only the authorized monitoring application is installed, reducing the risk of unauthorized data leaks.
- **Data encryption**: All data transmitted between the client devices and the server is encrypted to prevent unauthorized access.

## Deployment and Maintenance

1. **Deployment**: The client application is deployed automatically via the web portal and runs silently in the background. This ensures minimal disruption to the user experience.
2. **Maintenance**: Regular updates to the client application and the web portal can be managed by the IT department to adapt to evolving security needs.

## License
This project is designed for **internal use only** within government organizations. It is not intended for public release or use by external entities.

