**[Client](https://github.com/LuigiARC/Persona5AP.Client/) [Apworld](https://github.com/LuigiARC/Archipelago-P5R/releases/) [Details](https://github.com/LuigiARC/Archipelago-P5R/tree/p5r/docs/en_Persona%205%20Royal.md) <u>[Setup](https://github.com/LuigiARC/Archipelago-P5R/tree/p5r/docs/setup_en.md)</u>**

# Persona 5 Royal Archipelago Setup Guide

Persona 5 AP is in alpha. Use a disposable save and keep a backup before playing.

## Required Software

- A supported **Steam PC installation of Persona 5 Royal**, with the English game resources.
- [Reloaded-II](https://github.com/Reloaded-Project/Reloaded-II/releases), used to launch the modded game.
- The **Persona 5 AP client**, downloaded as `Persona 5 AP.zip` from the [client releases](https://github.com/LuigiARC/Persona5AP.Client/releases).
- For generating or locally hosting a world: **Archipelago 0.6.8 or a compatible version**, available from the [Archipelago releases](https://github.com/ArchipelagoMW/Archipelago/releases), and `p5r.apworld` from the [Persona 5 Royal APWorld releases](https://github.com/LuigiARC/Archipelago-P5R/releases).

The person generating the multiworld must install the APWorld. Players joining an
already-generated room use the Reloaded-II client to connect to it.

## Installation Procedures

### Install the APWorld

If you are generating the multiworld:

1. Install Archipelago.
2. Download `p5r.apworld` from the APWorld releases linked above.
3. Open Archipelago Launcher, select **Install APWorld**, and choose `p5r.apworld`.
4. Restart the launcher after installation so it loads the world.

Use matching APWorld and client releases. The game name in the YAML and the client
is **Persona 5 Royal**.

### Install the Game Client

These steps use the Windows Reloaded-II interface. For Linux/Proton, follow
Reloaded-II's [Linux setup guide](https://reloaded-project.github.io/Reloaded-II/LinuxSetupGuide/) first.

1. Back up the Persona 5 Royal saves you intend to use.
2. Install Reloaded-II and add the game's `P5R.exe` as an application. See the
   [Reloaded-II quick start](https://reloaded-project.github.io/Reloaded-II/QuickStart/) if this is your first time using it.
3. Download `Persona 5 AP.zip` and drag the ZIP onto the Reloaded-II window to install it.
4. Select Persona 5 Royal in Reloaded-II and enable **Persona 5 AP** and its dependencies:
   - Persona Essentials (`p5rpc.modloader`)
   - CRI FileSystem V2 Hook (`crifs.v2.hook`)
   - SharedLib Hooks (`reloaded.sharedlib.hooks`)
   - BF File Emulator (`reloaded.universal.fileemulationframework.bf`)
5. Install and enable any additional dependencies requested by Reloaded-II.
6. Launch the game through Reloaded-II.

On launch, the client reads the necessary files from your installed game, applies
its patches and caches the results locally. Original CPK archives are opened
read-only. You do not need to extract CPKs, install Python, build the client, or
apply a separate per-player patch.

## Create a Config (.yaml) File

### What Is a Config File and Why Do I Need One?

Your YAML identifies your player slot and selects the options used when generating
your world. For an introduction, see the
[Archipelago setup guide](https://archipelago.gg/tutorial/Archipelago/setup/en).

### Where Do I Get an Options File?

After installing `p5r.apworld`, select **Generate Template Options** in Archipelago
Launcher. Find the Persona 5 Royal template in `Players/Templates` and copy it into
`Players` before editing it. You can also start from the supplied
[example YAML](../examples/P5R.yaml).

Set the top-level `name` to your desired slot name, up to 16 characters. This is the
name you enter in the client's Connection menu; it must match the generated slot.
Keep the `game` value and game-options section named `Persona 5 Royal`.

The defaults use Shido as the goal, 20 shop checks priced from 1,000 to 10,000 yen,
five chest checks per Mementos Path, and DeathLink enabled with 30% received damage.
See the [game details](en_Persona%205%20Royal.md) for the available checks and features.

### Verifying Your Config File

Generate a local test world using your installed APWorld. If generation reports an
option or YAML error, correct it before sending the file to your room organizer.
A web generator or validator also needs to support this APWorld to process it.

## Joining a Multiworld Game

### Generating and Hosting a Game

If another person is hosting, send them your YAML and obtain the room address,
port and password, if one is set. The organizer needs the matching `p5r.apworld`
installed when generating the multiworld.

To generate and host locally:

1. Put each player's YAML in Archipelago's `Players` folder. Each slot needs a unique name.
2. Select **Generate** in Archipelago Launcher.
3. Find the generated `AP_*.zip` in the `output` folder and extract it.
4. Select **Host** in Archipelago Launcher and open the generated `.archipelago` file.
5. Keep the server running while playing. If other players are connecting from
   another computer, follow the networking instructions in the general Archipelago setup guide.

Keep the generated world and server save so you can resume the same session.
The Persona 5 AP client is installed once and connects to the selected room; this
world does not produce a ROM or a per-player game patch to open.

### Connecting to a Server

1. Launch Persona 5 Royal through Reloaded-II with Persona 5 AP enabled.
2. Load your test save and wait until you can control Joker normally. The F9 menu
   should be available after the casino intro; loading screens, battles and events can block it.
3. Press **F9** and open **Connection**.
4. Enter the room's address and port, such as `archipelago.gg:12345`. Use
   `localhost:38281` only when the server is running on the same computer as the game.
5. Enter the slot name from your YAML and the room password, if required.
6. Select **Connect** and confirm that the connection status shows you are connected.
7. Use the Shop and Warps menus and begin collecting checks. Return to or reopen
   the hub as needed to reconcile received inventory, recruitment and level rewards.

The Mementos entrance ticket gates also provide access to the hub. Host and slot
settings are saved; passwords entered through the menu may need to be entered
again after restarting the game.

Completed checks are tracked for reconciliation after reconnecting or loading a
save. Keep the same generated world and use the same slot when resuming.

## Troubleshooting

- **F9 does not open:** confirm the mod and dependencies are enabled for `P5R.exe`,
  launch through Reloaded-II, load a save and try again during normal field control.
  Check the Reloaded log for startup errors if the menu remains unavailable.
- **The slot is not found:** check that the Connection slot name matches the YAML's
  `name`, and that you are connecting to the correct room and port.
- **The room rejects the game name or catalog data:** use matching APWorld and
  client releases. Seeds generated under an older game identifier need regeneration.
- **Game-file preparation fails:** check the Reloaded log for the affected file.
  The client requires unmodified original files from a supported game version.
- **A received item has not appeared yet:** return to or reopen the hub so pending
  grants can reconcile. If it still does not apply, check the connection status and Reloaded log.
