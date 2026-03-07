; ==============================
; Smart File Organizer PRO Installer
; The DevOps Rite
; ==============================

#define MyAppName "Smart File Organizer Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "The DevOps Rite"
#define MyAppURL "https://github.com/TheDevOpsRite"
#define MyAppExeName "smart_file_organizer_pro.exe"

[Setup]
AppId={{B7F0A9C2-6D51-4D5E-9A1B-DEVOPSRITEPRO001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\installer_assets\LICENSE.txt
OutputDir=Output
OutputBaseFilename=SmartFileOrganizerProSetup_v{#MyAppVersion}
SetupIconFile=..\installer_assets\app.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional options:"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Messages]
SetupAppTitle=Smart File Organizer Pro Setup
SetupWindowTitle=Smart File Organizer Pro Installer
FinishedHeadingLabel=Installation Complete
FinishedLabel=Smart File Organizer Pro has been successfully installed on your system.