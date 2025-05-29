# SIM Card Management Portal - Distribution Guide

This guide explains how to distribute the SIM Card Management Portal application to end users.

## Option 1: Simple Executable Distribution

The simplest way to distribute the application is to share the standalone executable:

1. Navigate to the `dist` folder
2. Share the entire `SIM_Management.exe` file with users
3. Users can simply double-click the file to run the application

## Option 2: Creating an Installer (Recommended)

For a more professional distribution experience, you can create an installer:

1. Download and install NSIS (Nullsoft Scriptable Install System) from: https://nsis.sourceforge.io/Download
2. Right-click on the `installer.nsi` file and select "Compile NSIS Script"
3. This will create the `SIM_Management_Setup.exe` installer in the same directory
4. Share the installer with users
5. Users can run the installer to properly install the application with Start Menu shortcuts and uninstall support

## Installation Requirements

Users' computers should meet the following requirements:

- Windows 7 or higher
- At least 200MB of free disk space
- Administrator rights (if using the installer)

## Support

For any issues or support requests, please contact support@amecor.com
