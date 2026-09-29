; Inno Setup script for Jazira Download Manager (JDM)
; Build:  ISCC.exe /DMyAppVersion=1.0.0 installer\jdm.iss

#ifndef MyAppVersion
  #define MyAppVersion "1.1.0"
#endif
#define MyAppName "Jazira Download Manager"
#define MyAppExe "JDM.exe"

[Setup]
AppId={{6C2B7E51-4A1D-4E8B-9C3F-2D7A51B0E9A4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Ali Alsaffar
DefaultDirName={autopf}\JDM
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=Output
OutputBaseFilename=JDM-Setup-{#MyAppVersion}
SetupIconFile=..\assets\jdm.ico
UninstallDisplayIcon={app}\{#MyAppExe}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startup";     Description: "Start JDM with Windows (in the tray)"; GroupDescription: "Options:"

[Files]
Source: "..\dist\JDM\*";     DestDir: "{app}";           Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\extension\*";    DestDir: "{app}\extension"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}";              Filename: "{app}\{#MyAppExe}"
Name: "{group}\Browser Extension Folder";  Filename: "{app}\extension"
Name: "{group}\Uninstall {#MyAppName}";    Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}";        Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}";        Filename: "{app}\{#MyAppExe}"; Parameters: "--minimized"; Tasks: startup

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\extension"; Description: "Open the browser extension folder (for Chrome / Edge)"; Flags: postinstall shellexec skipifsilent unchecked
