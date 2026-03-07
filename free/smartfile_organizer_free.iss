; ==============================
; Smart File Organizer Installer
; The DevOps Rite
; ==============================

#define MyAppName "Smart File Organizer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "The DevOps Rite"
#define MyAppURL "https://github.com/TheDevOpsRite"
#define MyAppExeName "smart_file_organizer.exe"

[Setup]
AppId={{E4D8F7A1-8C9B-4A2F-9F21-DEVOPSRITE001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
OutputDir=Output
OutputBaseFilename=SmartFileOrganizerSetup_v{#MyAppVersion}
SetupIconFile=app.ico
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
SetupAppTitle=Smart File Organizer Setup
SetupWindowTitle=Smart File Organizer Installer
FinishedHeadingLabel=Installation Complete
FinishedLabel=Smart File Organizer has been successfully installed on your system.