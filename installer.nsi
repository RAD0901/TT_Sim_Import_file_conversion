; SIM Management Installer Script
; Created by GitHub Copilot

!define APPNAME "SIM Card Management Portal"
!define COMPANYNAME "Amecor"
!define DESCRIPTION "Tool for SIM card data management"
!define VERSION "1.0.0"

!include "MUI2.nsh"
!include "LogicLib.nsh"

Name "${APPNAME}"
OutFile "SIM_Management_Setup.exe"
InstallDir "$PROGRAMFILES\${COMPANYNAME}\${APPNAME}"
InstallDirRegKey HKLM "Software\${COMPANYNAME}\${APPNAME}" "Install_Dir"
RequestExecutionLevel admin

; Modern UI
!define MUI_ABORTWARNING
!define MUI_ICON "tt_sim_import\assets\app_icon.ico"
!define MUI_UNICON "tt_sim_import\assets\app_icon.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath $INSTDIR
    
    ; Main executable file
    File "dist\SIM_Management.exe"
    
    ; Create Start Menu shortcut
    CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\SIM_Management.exe"
    
    ; Create Desktop shortcut
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\SIM_Management.exe"
    
    ; Write registry keys for uninstaller
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "NoRepair" 1
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "DisplayIcon" "$INSTDIR\SIM_Management.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}" "Publisher" "${COMPANYNAME}"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove application files
    Delete "$INSTDIR\SIM_Management.exe"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Remove Start Menu shortcuts
    Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${COMPANYNAME}"
    
    ; Remove Desktop shortcut
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME}_${APPNAME}"
    DeleteRegKey HKLM "Software\${COMPANYNAME}\${APPNAME}"
    
    ; Remove installation directory if empty
    RMDir "$INSTDIR"
SectionEnd
