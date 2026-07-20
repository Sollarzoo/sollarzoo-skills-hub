# Blender MCP initialization and recovery

## Contents

1. Architecture
2. Preflight gate
3. Install Blender
4. Install the official Blender MCP Extension
5. Install the MCP server
6. Configure Codex
7. Verify the connection
8. Handle missing or broken MCP
9. Obtain a licensed model

Official Blender MCP guide: <https://www.blender.org/lab/mcp-server/>

Official model-search starting point supplied for this workflow: <https://sketchfab.com/3d-models>

## 1. Understand the two required components

Blender MCP is not only a Codex configuration and not only a Blender add-on. It requires both:

```text
Codex/MCP client
  ⇅ MCP over stdio
blender-mcp server process
  ⇅ local TCP socket
Blender MCP Extension
  ⇅ Blender Python API
open Blender scene
```

The MCP client normally launches the external `blender-mcp` process. The enabled Blender Extension opens a local bridge. The official extension defaults to `localhost:9876`.

No Blender, MCP, or API account is required for this local connection. Installation requires internet access. Do not ask the user for a password, token, or API key.

## 2. Use a read-only preflight gate

At the beginning of every Blender production task:

1. Locate Blender:

   ```bash
   command -v blender || ls -d /Applications/Blender.app
   ```

2. Read its version. The official MCP Extension version 1.0.0 declares Blender 5.1.0 as its minimum; verify the current official guide before installing on another machine.
3. Search for Blender MCP tools in the current client.
4. Call a read-only tool such as `get_blendfile_summary_path_info`.
5. Confirm:
   - the call succeeds;
   - a Blender process is open;
   - the returned file path is the intended `.blend`;
   - the file’s dirty/saved state is understood.
6. Detect the operating system and available local video encoder:
   - macOS: `xcrun`/Swift AVFoundation, then optional FFmpeg;
   - Windows: `ffmpeg` and `ffprobe`;
   - Linux: `ffmpeg` and `ffprobe`.

Only after all connection checks may the Skill modify the live scene. Video-encoder availability does not block scene work, but it must be resolved before final video encoding.

Do not infer connectivity from any one of these:

- Blender is installed;
- the extension appears installed;
- a `[mcp_servers.blender]` entry exists;
- Blender tools appear in a tool catalog.

The live read-only response is the gate.

## 3. Install Blender

If Blender is missing or too old:

1. explain the required version and download source;
2. ask the user to approve installation or install Blender themselves;
3. let the user complete any administrator or macOS security prompt;
4. reopen Blender and confirm its version.

Do not replace an existing production Blender version without approval. Multiple Blender versions can have separate extension and preference directories.

## 4. Install the official Blender MCP Extension

Use the official guide above. For the current official route:

1. Open Blender.
2. Open **Edit → Preferences → System → Network** and enable **Allow Online Access**.
3. Open **Preferences → Get Extensions**.
4. Add or enable the Blender Lab Extensions repository:

   ```text
   https://lab.blender.org/
   ```

5. Search for **MCP**, install it, and enable it.
6. Open the MCP add-on preferences.
7. Keep:
   - Host: `localhost`
   - Port: `9876`
   - Auto Start: enabled
8. Save Preferences.
9. Restart Blender if the extension does not become active immediately.

Alternatively, use the extension ZIP from the official Blender MCP release and choose **Install from Disk**. Do not download add-on ZIPs from an unverified mirror.

The user may need to operate the Blender Preferences UI or approve the installation. Codex may guide or use authorized computer control, but must explain what will be installed first.

### Bridge status

In the MCP extension preferences, check for:

- `Server is running`; or
- the **Start MCP Bridge Server** button.

If Auto Start is disabled, start the bridge manually every time Blender opens. Keep Blender running while Codex uses interactive tools.

## 5. Install the external MCP server

The official server installation source is:

```bash
pip install 'git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp'
```

Prefer an isolated environment:

### macOS/Linux

```bash
python3 -m venv ~/.local/share/blender-mcp/.venv
~/.local/share/blender-mcp/.venv/bin/python -m pip install \
  'git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp'
```

The executable will normally be:

```text
~/.local/share/blender-mcp/.venv/bin/blender-mcp
```

### Windows

Create a virtual environment and use its `Scripts\blender-mcp.exe`. Use an absolute path in the client configuration.

Installation changes the machine and downloads code. Ask for approval when required by the host. No login is needed for the official public repository.

### Source-checkout alternative

When using a reviewed local source checkout with `uv`:

```toml
[mcp_servers.blender]
command = "/absolute/path/to/uv"
args = ["--directory", "/absolute/path/to/blender_mcp/mcp", "run", "blender-mcp"]
```

Use absolute paths. Do not assume `/opt/homebrew/bin/uv` exists on every Mac.

## 6. Configure Codex

Add the server to `${CODEX_HOME:-~/.codex}/config.toml`:

```toml
[mcp_servers.blender]
command = "/absolute/path/to/blender-mcp"
```

For a virtual environment on macOS, this may be:

```toml
[mcp_servers.blender]
command = "/Users/NAME/.local/share/blender-mcp/.venv/bin/blender-mcp"
```

Do not overwrite unrelated MCP configuration. Inspect the existing file first, create a backup, and add only the missing server block. If a Blender block already exists, verify it instead of creating a duplicate.

After changing the configuration:

1. restart Codex/ChatGPT Desktop or open a new task so tools are rediscovered;
2. open Blender;
3. wait for the MCP bridge Auto Start delay;
4. run the read-only preflight again.

## 7. Verify end to end

The verification sequence is:

1. Blender open;
2. intended `.blend` open;
3. MCP Extension enabled;
4. bridge reports running on `localhost:9876`;
5. Codex MCP server configuration points to a valid executable;
6. Codex restarted after configuration;
7. a read-only Blender summary call succeeds;
8. returned path matches the intended file.

Then tell the user:

> Blender MCP 已连通，当前连接到 `<blend-path>`。我会先只读分析场景，确认后再修改。

Do not test the connection by adding, deleting, or moving an object.

## 8. Handle missing or broken MCP

Classify the failure before asking the user for help.

| Failure | Evidence | Action |
|---|---|---|
| Blender missing | no executable/application | ask user to install/approve Blender |
| Blender too old | version below extension minimum | propose upgrade; do not overwrite silently |
| Server not configured | no MCP block/tool | install server and add client config with approval |
| Extension missing | server exists but socket refuses connection | guide installation in Blender |
| Bridge stopped | extension enabled, status stopped | user clicks Start or enables Auto Start |
| Online Access off | extension shows startup error | user enables Allow Online Access |
| Port mismatch | server and extension use different ports | align both to `localhost:9876` or one approved port |
| Client stale | config correct but tools absent | restart Codex/open a new task |
| Wrong `.blend` | live call returns another path | user opens intended file; retest |
| MCP temporarily unavailable | quota/tool outage | prepare script/specification; resume live work later |

### Fallback boundary

Without a live MCP connection:

- continue reading the creative script and local assets;
- write or refine the shot specification;
- prepare a Blender Python script for later execution;
- use Blender background CLI only for safe, file-based inspection/rendering when available;
- explain that interactive viewport rendering and live scene changes are not verified.

Do not claim the `.blend` was changed. Do not use generic desktop automation to perform a long sequence of hidden scene edits unless the user explicitly chooses that fallback and the result can be verified.

## 9. Obtain a licensed model

When no suitable model is provided, use the user-approved source:

<https://sketchfab.com/3d-models>

Before downloading:

1. identify whether an exact named device or a generic device is acceptable;
2. filter for downloadable models;
3. open the individual model page;
4. verify its license, creator, permitted use, attribution, and redistribution limits;
5. ask the user to log in or purchase the asset if required;
6. never request the Sketchfab password in chat;
7. save the source URL, creator, license, and attribution text in the project manifest.

Prefer:

- `.glb/.gltf` for PBR material portability;
- `.fbx` when the supplied pipeline requires it;
- `.obj` only when simpler geometry and separate textures are acceptable.

After download, inspect polygon count, visible detail, UVs, texture completeness, normals, scale, and license file before importing. Do not rip, scrape, or bypass download restrictions on a non-downloadable model.
