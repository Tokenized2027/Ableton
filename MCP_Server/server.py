# ableton_mcp_server.py
from mcp.server.fastmcp import FastMCP, Context
import socket
import json
import logging
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AbletonMCPServer")

@dataclass
class AbletonConnection:
    host: str
    port: int
    sock: socket.socket = None
    
    def connect(self) -> bool:
        """Connect to the Ableton Remote Script socket server"""
        if self.sock:
            return True
            
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            logger.info(f"Connected to Ableton at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ableton: {str(e)}")
            self.sock = None
            return False
    
    def disconnect(self):
        """Disconnect from the Ableton Remote Script"""
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                logger.error(f"Error disconnecting from Ableton: {str(e)}")
            finally:
                self.sock = None

    def receive_full_response(self, sock, buffer_size=8192):
        """Receive the complete response, potentially in multiple chunks"""
        chunks = []
        sock.settimeout(15.0)  # Increased timeout for operations that might take longer
        
        try:
            while True:
                try:
                    chunk = sock.recv(buffer_size)
                    if not chunk:
                        if not chunks:
                            raise Exception("Connection closed before receiving any data")
                        break
                    
                    chunks.append(chunk)
                    
                    # Check if we've received a complete JSON object
                    try:
                        data = b''.join(chunks)
                        json.loads(data.decode('utf-8'))
                        logger.info(f"Received complete response ({len(data)} bytes)")
                        return data
                    except json.JSONDecodeError:
                        # Incomplete JSON, continue receiving
                        continue
                except socket.timeout:
                    logger.warning("Socket timeout during chunked receive")
                    break
                except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                    logger.error(f"Socket connection error during receive: {str(e)}")
                    raise
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
            
        # If we get here, we either timed out or broke out of the loop
        if chunks:
            data = b''.join(chunks)
            logger.info(f"Returning data after receive completion ({len(data)} bytes)")
            try:
                json.loads(data.decode('utf-8'))
                return data
            except json.JSONDecodeError:
                raise Exception("Incomplete JSON response received")
        else:
            raise Exception("No data received")

    def send_command(self, command_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to Ableton and return the response"""
        if not self.sock and not self.connect():
            raise ConnectionError("Not connected to Ableton")
        
        command = {
            "type": command_type,
            "params": params or {}
        }
        
        # Check if this is a state-modifying command
        is_modifying_command = command_type in [
            "create_midi_track", "create_audio_track", "set_track_name",
            "create_clip", "add_notes_to_clip", "set_clip_name",
            "set_tempo", "fire_clip", "stop_clip", "set_device_parameter",
            "start_playback", "stop_playback", "load_instrument_or_effect"
        ]
        
        try:
            logger.info(f"Sending command: {command_type} with params: {params}")
            
            # Send the command
            self.sock.sendall(json.dumps(command).encode('utf-8'))
            logger.info(f"Command sent, waiting for response...")
            
            # For state-modifying commands, add a small delay to give Ableton time to process
            if is_modifying_command:
                import time
                time.sleep(0.1)  # 100ms delay
            
            # Set timeout based on command type
            timeout = 15.0 if is_modifying_command else 10.0
            self.sock.settimeout(timeout)
            
            # Receive the response
            response_data = self.receive_full_response(self.sock)
            logger.info(f"Received {len(response_data)} bytes of data")
            
            # Parse the response
            response = json.loads(response_data.decode('utf-8'))
            logger.info(f"Response parsed, status: {response.get('status', 'unknown')}")
            
            if response.get("status") == "error":
                logger.error(f"Ableton error: {response.get('message')}")
                raise Exception(response.get("message", "Unknown error from Ableton"))
            
            # For state-modifying commands, add another small delay after receiving response
            if is_modifying_command:
                import time
                time.sleep(0.1)  # 100ms delay
            
            return response.get("result", {})
        except socket.timeout:
            logger.error("Socket timeout while waiting for response from Ableton")
            self.sock = None
            raise Exception("Timeout waiting for Ableton response")
        except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
            logger.error(f"Socket connection error: {str(e)}")
            self.sock = None
            raise Exception(f"Connection to Ableton lost: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Ableton: {str(e)}")
            if 'response_data' in locals() and response_data:
                logger.error(f"Raw response (first 200 bytes): {response_data[:200]}")
            self.sock = None
            raise Exception(f"Invalid response from Ableton: {str(e)}")
        except Exception as e:
            logger.error(f"Error communicating with Ableton: {str(e)}")
            self.sock = None
            raise Exception(f"Communication error with Ableton: {str(e)}")

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("AbletonMCP server starting up")
        
        try:
            ableton = get_ableton_connection()
            logger.info("Successfully connected to Ableton on startup")
        except Exception as e:
            logger.warning(f"Could not connect to Ableton on startup: {str(e)}")
            logger.warning("Make sure the Ableton Remote Script is running")
        
        yield {}
    finally:
        global _ableton_connection
        if _ableton_connection:
            logger.info("Disconnecting from Ableton on shutdown")
            _ableton_connection.disconnect()
            _ableton_connection = None
        logger.info("AbletonMCP server shut down")

# Create the MCP server with lifespan support
mcp = FastMCP(
    "AbletonMCP",
    lifespan=server_lifespan
)

# Global connection for resources
_ableton_connection = None

def get_ableton_connection():
    """Get or create a persistent Ableton connection"""
    global _ableton_connection
    
    if _ableton_connection is not None:
        try:
            # Test the connection with a simple ping
            # We'll try to send an empty message, which should fail if the connection is dead
            # but won't affect Ableton if it's alive
            _ableton_connection.sock.settimeout(1.0)
            _ableton_connection.sock.sendall(b'')
            return _ableton_connection
        except Exception as e:
            logger.warning(f"Existing connection is no longer valid: {str(e)}")
            try:
                _ableton_connection.disconnect()
            except:
                pass
            _ableton_connection = None
    
    # Connection doesn't exist or is invalid, create a new one
    if _ableton_connection is None:
        # Try to connect up to 3 times with a short delay between attempts
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"Connecting to Ableton (attempt {attempt}/{max_attempts})...")
                _ableton_connection = AbletonConnection(host="localhost", port=9877)
                if _ableton_connection.connect():
                    logger.info("Created new persistent connection to Ableton")
                    
                    # Validate connection with a simple command
                    try:
                        # Get session info as a test
                        _ableton_connection.send_command("get_session_info")
                        logger.info("Connection validated successfully")
                        return _ableton_connection
                    except Exception as e:
                        logger.error(f"Connection validation failed: {str(e)}")
                        _ableton_connection.disconnect()
                        _ableton_connection = None
                        # Continue to next attempt
                else:
                    _ableton_connection = None
            except Exception as e:
                logger.error(f"Connection attempt {attempt} failed: {str(e)}")
                if _ableton_connection:
                    _ableton_connection.disconnect()
                    _ableton_connection = None
            
            # Wait before trying again, but only if we have more attempts left
            if attempt < max_attempts:
                import time
                time.sleep(1.0)
        
        # If we get here, all connection attempts failed
        if _ableton_connection is None:
            logger.error("Failed to connect to Ableton after multiple attempts")
            raise Exception("Could not connect to Ableton. Make sure the Remote Script is running.")
    
    return _ableton_connection


# Core Tool endpoints

@mcp.tool()
def get_session_info(ctx: Context) -> str:
    """Get detailed information about the current Ableton session"""
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_session_info")
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting session info from Ableton: {str(e)}")
        return f"Error getting session info: {str(e)}"

@mcp.tool()
def get_track_info(ctx: Context, track_index: int) -> str:
    """
    Get detailed information about a specific track in Ableton.
    
    Parameters:
    - track_index: The index of the track to get information about
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_track_info", {"track_index": track_index})
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting track info from Ableton: {str(e)}")
        return f"Error getting track info: {str(e)}"

@mcp.tool()
def create_midi_track(ctx: Context, index: int = -1) -> str:
    """
    Create a new MIDI track in the Ableton session.
    
    Parameters:
    - index: The index to insert the track at (-1 = end of list)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("create_midi_track", {"index": index})
        return f"Created new MIDI track: {result.get('name', 'unknown')}"
    except Exception as e:
        logger.error(f"Error creating MIDI track: {str(e)}")
        return f"Error creating MIDI track: {str(e)}"


@mcp.tool()
def set_track_name(ctx: Context, track_index: int, name: str) -> str:
    """
    Set the name of a track.
    
    Parameters:
    - track_index: The index of the track to rename
    - name: The new name for the track
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("set_track_name", {"track_index": track_index, "name": name})
        return f"Renamed track to: {result.get('name', name)}"
    except Exception as e:
        logger.error(f"Error setting track name: {str(e)}")
        return f"Error setting track name: {str(e)}"

@mcp.tool()
def create_clip(ctx: Context, track_index: int, clip_index: int, length: float = 4.0) -> str:
    """
    Create a new MIDI clip in the specified track and clip slot.
    
    Parameters:
    - track_index: The index of the track to create the clip in
    - clip_index: The index of the clip slot to create the clip in
    - length: The length of the clip in beats (default: 4.0)
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("create_clip", {
            "track_index": track_index, 
            "clip_index": clip_index, 
            "length": length
        })
        return f"Created new clip at track {track_index}, slot {clip_index} with length {length} beats"
    except Exception as e:
        logger.error(f"Error creating clip: {str(e)}")
        return f"Error creating clip: {str(e)}"

@mcp.tool()
def add_notes_to_clip(
    ctx: Context, 
    track_index: int, 
    clip_index: int, 
    notes: List[Dict[str, Union[int, float, bool]]]
) -> str:
    """
    Add MIDI notes to a clip.
    
    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    - notes: List of note dictionaries, each with pitch, start_time, duration, velocity, and mute
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("add_notes_to_clip", {
            "track_index": track_index,
            "clip_index": clip_index,
            "notes": notes
        })
        return f"Added {len(notes)} notes to clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.error(f"Error adding notes to clip: {str(e)}")
        return f"Error adding notes to clip: {str(e)}"

@mcp.tool()
def set_clip_name(ctx: Context, track_index: int, clip_index: int, name: str) -> str:
    """
    Set the name of a clip.
    
    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    - name: The new name for the clip
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("set_clip_name", {
            "track_index": track_index,
            "clip_index": clip_index,
            "name": name
        })
        return f"Renamed clip at track {track_index}, slot {clip_index} to '{name}'"
    except Exception as e:
        logger.error(f"Error setting clip name: {str(e)}")
        return f"Error setting clip name: {str(e)}"

@mcp.tool()
def set_tempo(ctx: Context, tempo: float) -> str:
    """
    Set the tempo of the Ableton session.
    
    Parameters:
    - tempo: The new tempo in BPM
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("set_tempo", {"tempo": tempo})
        return f"Set tempo to {tempo} BPM"
    except Exception as e:
        logger.error(f"Error setting tempo: {str(e)}")
        return f"Error setting tempo: {str(e)}"


@mcp.tool()
def load_instrument_or_effect(ctx: Context, track_index: int, uri: str) -> str:
    """
    Load an instrument or effect onto a track using its URI.
    
    Parameters:
    - track_index: The index of the track to load the instrument on
    - uri: The URI of the instrument or effect to load (e.g., 'query:Synths#Instrument%20Rack:Bass:FileId_5116')
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("load_browser_item", {
            "track_index": track_index,
            "item_uri": uri
        })
        
        # Check if the instrument was loaded successfully
        if result.get("loaded", False):
            new_devices = result.get("new_devices", [])
            if new_devices:
                return f"Loaded instrument with URI '{uri}' on track {track_index}. New devices: {', '.join(new_devices)}"
            else:
                devices = result.get("devices_after", [])
                return f"Loaded instrument with URI '{uri}' on track {track_index}. Devices on track: {', '.join(devices)}"
        else:
            return f"Failed to load instrument with URI '{uri}'"
    except Exception as e:
        logger.error(f"Error loading instrument by URI: {str(e)}")
        return f"Error loading instrument by URI: {str(e)}"

@mcp.tool()
def fire_clip(ctx: Context, track_index: int, clip_index: int) -> str:
    """
    Start playing a clip.
    
    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("fire_clip", {
            "track_index": track_index,
            "clip_index": clip_index
        })
        return f"Started playing clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.error(f"Error firing clip: {str(e)}")
        return f"Error firing clip: {str(e)}"

@mcp.tool()
def stop_clip(ctx: Context, track_index: int, clip_index: int) -> str:
    """
    Stop playing a clip.
    
    Parameters:
    - track_index: The index of the track containing the clip
    - clip_index: The index of the clip slot containing the clip
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("stop_clip", {
            "track_index": track_index,
            "clip_index": clip_index
        })
        return f"Stopped clip at track {track_index}, slot {clip_index}"
    except Exception as e:
        logger.error(f"Error stopping clip: {str(e)}")
        return f"Error stopping clip: {str(e)}"

@mcp.tool()
def start_playback(ctx: Context) -> str:
    """Start playing the Ableton session."""
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("start_playback")
        return "Started playback"
    except Exception as e:
        logger.error(f"Error starting playback: {str(e)}")
        return f"Error starting playback: {str(e)}"

@mcp.tool()
def stop_playback(ctx: Context) -> str:
    """Stop playing the Ableton session."""
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("stop_playback")
        return "Stopped playback"
    except Exception as e:
        logger.error(f"Error stopping playback: {str(e)}")
        return f"Error stopping playback: {str(e)}"

@mcp.tool()
def get_browser_tree(ctx: Context, category_type: str = "all") -> str:
    """
    Get a hierarchical tree of browser categories from Ableton.
    
    Parameters:
    - category_type: Type of categories to get ('all', 'instruments', 'sounds', 'drums', 'audio_effects', 'midi_effects')
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_browser_tree", {
            "category_type": category_type
        })
        
        # Check if we got any categories
        if "available_categories" in result and len(result.get("categories", [])) == 0:
            available_cats = result.get("available_categories", [])
            return (f"No categories found for '{category_type}'. "
                   f"Available browser categories: {', '.join(available_cats)}")
        
        # Format the tree in a more readable way
        total_folders = result.get("total_folders", 0)
        formatted_output = f"Browser tree for '{category_type}' (showing {total_folders} folders):\n\n"
        
        def format_tree(item, indent=0):
            output = ""
            if item:
                prefix = "  " * indent
                name = item.get("name", "Unknown")
                path = item.get("path", "")
                has_more = item.get("has_more", False)
                
                # Add this item
                output += f"{prefix}• {name}"
                if path:
                    output += f" (path: {path})"
                if has_more:
                    output += " [...]"
                output += "\n"
                
                # Add children
                for child in item.get("children", []):
                    output += format_tree(child, indent + 1)
            return output
        
        # Format each category
        for category in result.get("categories", []):
            formatted_output += format_tree(category)
            formatted_output += "\n"
        
        return formatted_output
    except Exception as e:
        error_msg = str(e)
        if "Browser is not available" in error_msg:
            logger.error(f"Browser is not available in Ableton: {error_msg}")
            return f"Error: The Ableton browser is not available. Make sure Ableton Live is fully loaded and try again."
        elif "Could not access Live application" in error_msg:
            logger.error(f"Could not access Live application: {error_msg}")
            return f"Error: Could not access the Ableton Live application. Make sure Ableton Live is running and the Remote Script is loaded."
        else:
            logger.error(f"Error getting browser tree: {error_msg}")
            return f"Error getting browser tree: {error_msg}"

@mcp.tool()
def get_browser_items_at_path(ctx: Context, path: str) -> str:
    """
    Get browser items at a specific path in Ableton's browser.
    
    Parameters:
    - path: Path in the format "category/folder/subfolder"
            where category is one of the available browser categories in Ableton
    """
    try:
        ableton = get_ableton_connection()
        result = ableton.send_command("get_browser_items_at_path", {
            "path": path
        })
        
        # Check if there was an error with available categories
        if "error" in result and "available_categories" in result:
            error = result.get("error", "")
            available_cats = result.get("available_categories", [])
            return (f"Error: {error}\n"
                   f"Available browser categories: {', '.join(available_cats)}")
        
        return json.dumps(result, indent=2)
    except Exception as e:
        error_msg = str(e)
        if "Browser is not available" in error_msg:
            logger.error(f"Browser is not available in Ableton: {error_msg}")
            return f"Error: The Ableton browser is not available. Make sure Ableton Live is fully loaded and try again."
        elif "Could not access Live application" in error_msg:
            logger.error(f"Could not access Live application: {error_msg}")
            return f"Error: Could not access the Ableton Live application. Make sure Ableton Live is running and the Remote Script is loaded."
        elif "Unknown or unavailable category" in error_msg:
            logger.error(f"Invalid browser category: {error_msg}")
            return f"Error: {error_msg}. Please check the available categories using get_browser_tree."
        elif "Path part" in error_msg and "not found" in error_msg:
            logger.error(f"Path not found: {error_msg}")
            return f"Error: {error_msg}. Please check the path and try again."
        else:
            logger.error(f"Error getting browser items at path: {error_msg}")
            return f"Error getting browser items at path: {error_msg}"

@mcp.tool()
def load_drum_kit(ctx: Context, track_index: int, rack_uri: str, kit_path: str) -> str:
    """
    Load a drum rack and then load a specific drum kit into it.
    
    Parameters:
    - track_index: The index of the track to load on
    - rack_uri: The URI of the drum rack to load (e.g., 'Drums/Drum Rack')
    - kit_path: Path to the drum kit inside the browser (e.g., 'drums/acoustic/kit1')
    """
    try:
        ableton = get_ableton_connection()
        
        # Step 1: Load the drum rack
        result = ableton.send_command("load_browser_item", {
            "track_index": track_index,
            "item_uri": rack_uri
        })
        
        if not result.get("loaded", False):
            return f"Failed to load drum rack with URI '{rack_uri}'"
        
        # Step 2: Get the drum kit items at the specified path
        kit_result = ableton.send_command("get_browser_items_at_path", {
            "path": kit_path
        })
        
        if "error" in kit_result:
            return f"Loaded drum rack but failed to find drum kit: {kit_result.get('error')}"
        
        # Step 3: Find a loadable drum kit
        kit_items = kit_result.get("items", [])
        loadable_kits = [item for item in kit_items if item.get("is_loadable", False)]
        
        if not loadable_kits:
            return f"Loaded drum rack but no loadable drum kits found at '{kit_path}'"
        
        # Step 4: Load the first loadable kit
        kit_uri = loadable_kits[0].get("uri")
        load_result = ableton.send_command("load_browser_item", {
            "track_index": track_index,
            "item_uri": kit_uri
        })
        
        return f"Loaded drum rack and kit '{loadable_kits[0].get('name')}' on track {track_index}"
    except Exception as e:
        logger.error(f"Error loading drum kit: {str(e)}")
        return f"Error loading drum kit: {str(e)}"

# ============================================================================
# Flyin' Colors Custom Commands Extension
# ============================================================================

from flyin_colors.template_commands import create_flyin_colors_session as _fc_create_session
from flyin_colors.template_commands import create_nitzhonot_bass_template as _fc_create_nitzhonot_bass_template
from flyin_colors.midi_generation import generate_rolling_bass as _fc_generate_rolling_bass
from flyin_colors.midi_generation import generate_goa_arp as _fc_generate_goa_arp
from flyin_colors.midi_generation import generate_buildup_riser as _fc_generate_buildup_riser
from flyin_colors.session_commands import (
    set_section_markers as _fc_set_section_markers,
    export_session_state as _fc_export_session_state,
    import_continuation_brief as _fc_import_continuation_brief
)
from flyin_colors.narrative_commands import (
    apply_narrative_arc as _fc_apply_narrative_arc,
    transition_between_sections as _fc_transition_between_sections
)
from flyin_colors.mix_commands import (
    apply_frequency_ownership as _fc_apply_frequency_ownership,
    check_frequency_conflicts as _fc_check_frequency_conflicts
)

@mcp.tool()
def create_flyin_colors_session(
    ctx: Context,
    bpm: int = 148,
    key: str = "Dm",
    track_name: str = "FC_Track_01",
    section_type: str = "full"
) -> str:
    """
    Create a complete Flyin' Colors session template with standard track layout.

    This command creates a full Ableton session with:
    - 11 tracks (full mode) or fewer (minimal/jam modes)
    - 4 return tracks (reverb short/long, delay, distortion)
    - Session tempo set to specified BPM
    - Locator at bar 1 with track metadata

    Parameters:
    - bpm: Tempo in BPM (default: 148, Flyin' Colors standard)
    - key: Musical key for the track (default: "Dm")
    - track_name: Name for this production (default: "FC_Track_01")
    - section_type: Track template type - "full" (all 11 tracks),
                    "minimal" (kick+bass+lead), or "jam" (bass+drums)

    Track Layout (full mode):
    1. FC_Kick (MIDI)
    2. FC_Hats (MIDI)
    3. FC_Perc (MIDI)
    4. FC_Sub (MIDI - sub bass)
    5. FC_RollingBass (MIDI - signature rolling bass)
    6. FC_Lead (MIDI)
    7. FC_Pad (MIDI)
    8. FC_Arp (MIDI)
    9. FC_FX (Audio - for risers, impacts)
    10. FC_Vocal (Audio - for Hebrew samples, vocal textures)
    11. FC_Reference (Audio - muted, for A/B comparison)

    Return Tracks:
    A. FC_Reverb_Short (0.8s decay)
    B. FC_Reverb_Long (3.5s decay)
    C. FC_Delay (ping-pong, 1/8 note)
    D. FC_Distortion (saturator, medium drive)

    Example:
    create_flyin_colors_session(bpm=148, key="Dm", track_name="FC_HorrorToTriumph_01")
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_create_session(
            ableton_connection=ableton,
            bpm=bpm,
            key=key,
            track_name=track_name,
            section_type=section_type
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error creating Flyin' Colors session: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error creating Flyin' Colors session: {str(e)}"
        }, indent=2)

@mcp.tool()
def generate_rolling_bass(
    ctx: Context,
    track_index: int,
    clip_slot: int = 0,
    key: str = "D",
    octave: int = 2,
    scale: str = "natural_minor",
    bars: int = 4,
    pattern_type: str = "rolling_16th",
    velocity_pattern: List[int] = None,
    chord_progression: List[str] = None,
    bars_per_chord: int = 1,
    filter_hint: str = "medium"
) -> str:
    """
    Generate a rolling bass MIDI clip - the signature Flyin' Colors sound.

    Creates a MIDI clip with rolling 16th-note bass patterns that define
    the Flyin' Colors aesthetic. Supports multiple rhythm patterns and
    automatic chord progression mapping.

    Parameters:
    - track_index: Which track to place clip on (use track 4 for FC_RollingBass)
    - clip_slot: Scene/clip slot index (default: 0)
    - key: Root note - "C", "D", "E", etc. (default: "D")
    - octave: MIDI octave - 2 = bass range (D2 = MIDI 38) (default: 2)
    - scale: Scale type (default: "natural_minor")
             Options: "natural_minor", "harmonic_minor", "phrygian_dominant", "chromatic"
    - bars: Clip length in bars (default: 4)
    - pattern_type: Rhythm pattern (default: "rolling_16th")
                   Options: "rolling_16th" (mechanical, relentless),
                           "pulsing_8th" (pumping Nitzhonot),
                           "syncopated" (groovy, off-beats),
                           "gallop" (nu-metal 16-16-8th)
    - velocity_pattern: Repeating velocity cycle (default: [100, 85, 95, 80])
    - chord_progression: Roman numerals (default: ["i"])
                        Examples: ["i", "bVI", "bVII", "i"], ["i", "iv", "v", "i"]
    - bars_per_chord: Bars before chord changes (default: 1)
    - filter_hint: Metadata for filter position - "closed" (600Hz),
                   "medium" (900Hz), "open" (1200Hz) (default: "medium")

    Pattern Types:
    - rolling_16th: Every 16th note, single root - mechanical, Horror phase
    - pulsing_8th: Every 8th, root+octave alternating - Nitzhonot energy, Defiance
    - syncopated: 16ths with off-beat accents - groovy, Transitions
    - gallop: 16-16-8th repeating - aggressive nu-metal, Horror→Defiance

    Example:
    generate_rolling_bass(
        track_index=4,
        key="D",
        bars=4,
        pattern_type="rolling_16th",
        chord_progression=["i", "bVI", "bVII", "i"]
    )

    Creates: 64-note rolling bass pattern in Dm over 4 bars
    """
    try:
        ableton = get_ableton_connection()

        # Convert velocity_pattern and chord_progression to lists if needed
        if velocity_pattern is None:
            velocity_pattern = [100, 85, 95, 80]
        if chord_progression is None:
            chord_progression = ["i"]

        result = _fc_generate_rolling_bass(
            ableton_connection=ableton,
            track_index=track_index,
            clip_slot=clip_slot,
            key=key,
            octave=octave,
            scale=scale,
            bars=bars,
            pattern_type=pattern_type,
            velocity_pattern=velocity_pattern,
            chord_progression=chord_progression,
            bars_per_chord=bars_per_chord,
            filter_hint=filter_hint
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error generating rolling bass: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error generating rolling bass: {str(e)}"
        }, indent=2)

@mcp.tool()
def generate_goa_arp(
    ctx: Context,
    track_index: int,
    clip_slot: int = 0,
    key: str = "D",
    octave_start: int = 3,
    octave_range: int = 2,
    scale: str = "natural_minor",
    bars: int = 4,
    rate: str = "16th",
    direction: str = "up",
    chord_tones: List[str] = None,
    velocity_range: List[int] = None,
    velocity_shape: str = "saw_up",
    note_length_pct: int = 80
) -> str:
    """
    Generate arpeggiated MIDI pattern in Filteria/Pleiadians style.

    Creates classic Goa Trance arpeggios with configurable rate, direction,
    and velocity shaping. Perfect for psychedelic melodic lines that span
    multiple octaves.

    Parameters:
    - track_index: Which track to place clip on (use track 7 for FC_Arp)
    - clip_slot: Scene/clip slot index (default: 0)
    - key: Root note - "C", "D", "E", etc. (default: "D")
    - octave_start: Starting octave (default: 3)
    - octave_range: Octaves to span, 1-3 (default: 2)
    - scale: Scale type (default: "natural_minor")
             Options: "natural_minor", "harmonic_minor", "phrygian_dominant", "chromatic"
    - bars: Clip length in bars (default: 4)
    - rate: Note rate (default: "16th")
            Options: "8th", "16th", "32nd", "16th_triplet"
    - direction: Arp direction (default: "up")
                Options: "up" (classic uplifting),
                        "down" (melancholic),
                        "up_down" (Filteria-style flowing),
                        "random_seed" (psychedelic)
    - chord_tones: Scale degrees to use (default: ["1", "3", "5"])
                  Options: "1"=root, "3"=third, "5"=fifth, "7"=seventh
    - velocity_range: [min, max] velocity (default: [70, 110])
    - velocity_shape: Velocity pattern (default: "saw_up")
                     Options: "saw_up", "saw_down", "flat", "random"
    - note_length_pct: Note length % - 100=legato, 50=staccato (default: 80)

    Direction Patterns:
    - up: 1-3-5-1'-3'-5' - Classic Goa, uplifting
    - down: 5'-3'-1'-5-3-1 - Descending, melancholic
    - up_down: 1-3-5-1'-5-3-1 - Filteria-style flowing
    - random_seed: Seeded random - Psychedelic

    Example:
    generate_goa_arp(
        track_index=7,
        key="D",
        octave_start=3,
        octave_range=2,
        rate="16th",
        direction="up_down",
        chord_tones=["1", "3", "5", "7"]
    )

    Creates: Classic Filteria-style arpeggio spanning D3-D5
    """
    try:
        ableton = get_ableton_connection()

        # Convert chord_tones and velocity_range to lists if needed
        if chord_tones is None:
            chord_tones = ["1", "3", "5"]
        if velocity_range is None:
            velocity_range = [70, 110]

        result = _fc_generate_goa_arp(
            ableton_connection=ableton,
            track_index=track_index,
            clip_slot=clip_slot,
            key=key,
            octave_start=octave_start,
            octave_range=octave_range,
            scale=scale,
            bars=bars,
            rate=rate,
            direction=direction,
            chord_tones=chord_tones,
            velocity_range=velocity_range,
            velocity_shape=velocity_shape,
            note_length_pct=note_length_pct
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error generating Goa arp: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error generating Goa arp: {str(e)}"
        }, indent=2)

@mcp.tool()
def apply_narrative_arc(
    ctx: Context,
    phase: str,
    bar_start: int,
    bar_end: int,
    intensity: float = 0.7
) -> str:
    """
    Adjust track parameters to match emotional phase. Narrative arc becomes automation.

    This command sets device parameters and track volumes to reflect the
    narrative phase. Maps emotional states to concrete mixing/synthesis parameters.

    Parameters:
    - phase: Emotional phase (required)
             Options: "horror", "defiance", "triumph", "transition"
    - bar_start: First bar to apply settings (required)
    - bar_end: Last bar to apply settings (required)
    - intensity: Emotional intensity, 0.0=subtle, 1.0=extreme (default: 0.7)

    Phase Definitions:

    Horror:
    - Bass filter cutoff: 600-800 Hz (dark, constrained)
    - Reverb send (long): Low 0.1 (dry, claustrophobic)
    - Distortion send: High 0.5-0.7 (aggressive texture)
    - Pad volume: -6 dB (sparse, cold)
    - Lead: Muted (absent hope)

    Defiance:
    - Bass filter cutoff: 900-1200 Hz (full range, aggressive)
    - Reverb send (long): Medium 0.25 (building space)
    - Distortion send: Medium 0.3 (controlled aggression)
    - Pad volume: -3 dB (supportive)
    - Lead volume: 0 dB (assertive)

    Triumph:
    - Bass filter cutoff: 800-1000 Hz (gentler)
    - Reverb send (long): High 0.5 (lush, spacious)
    - Distortion send: Low 0.1 (clean, clear)
    - Pad volume: 0 dB (rich harmonic bed)
    - Lead volume: +1 dB (soaring melody)

    Transition:
    - Interpolated values between phases

    Example:
    apply_narrative_arc(
        phase="horror",
        bar_start=1,
        bar_end=64,
        intensity=0.8
    )

    Applies Horror phase settings across bars 1-64 at 80% intensity
    """
    try:
        ableton = get_ableton_connection()

        result = _fc_apply_narrative_arc(
            ableton_connection=ableton,
            phase=phase,
            bar_start=bar_start,
            bar_end=bar_end,
            intensity=intensity
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error applying narrative arc: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error applying narrative arc: {str(e)}"
        }, indent=2)

@mcp.tool()
def apply_frequency_ownership(
    ctx: Context,
    strict_mode: bool = True,
    apply_to_tracks: str = "all"
) -> str:
    """
    Apply frequency ownership chart to all tracks using EQ Eight.

    Automatically configures high-pass and low-pass filters on all Flyin' Colors
    tracks according to the FREQUENCY_RANGE_OWNERSHIP.md chart. Prevents frequency
    conflicts and ensures clean mix separation.

    Parameters:
    - strict_mode: Filter steepness (default: True)
                  True = 24dB/oct (hard cuts, strict separation)
                  False = 12dB/oct (gentle slopes, softer separation)
    - apply_to_tracks: Which tracks to process (default: "all")
                      "all" = Apply to all FC tracks, add/modify EQ as needed
                      "empty_only" = Only apply to tracks without existing EQ Eight

    Frequency Ownership Applied:
    - FC_Sub: 20-80 Hz (sub bass only)
    - FC_RollingBass: 80-200 Hz (core bass energy)
    - FC_Kick: 40-8000 Hz (overlaps with sub intentionally)
    - FC_Pad: 300-8000 Hz (carved out of bass)
    - FC_Lead: 800 Hz+ (high-mid focus)
    - FC_Arp: 1000 Hz+ (top-end energy)
    - FC_Hats: 3000 Hz+ (high-end percussion)
    - FC_Perc: 200 Hz+ (mid-range percussion)

    Returns:
    - Status with tracks_processed, eq_added, eq_modified counts

    Example:
    apply_frequency_ownership(strict_mode=True, apply_to_tracks="all")
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_apply_frequency_ownership(
            ableton_connection=ableton,
            strict_mode=strict_mode,
            apply_to_tracks=apply_to_tracks
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error applying frequency ownership: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error applying frequency ownership: {str(e)}"
        }, indent=2)

@mcp.tool()
def check_frequency_conflicts(
    ctx: Context,
    report_mode: str = "summary"
) -> str:
    """
    Analyze all tracks for frequency ownership violations.

    Scans all Flyin' Colors tracks and detects violations of the frequency
    ownership chart. Reports conflicts like pads in bass territory, missing
    EQs on critical tracks, or incorrect filter settings.

    Parameters:
    - report_mode: Level of detail in report (default: "summary")
                  "summary" = Conflict counts by severity (high/medium/low)
                  "detailed" = Full list of conflicts with recommendations

    Detected Conflicts:
    1. Pads/Leads below 300 Hz (mudding bass territory)
    2. Missing EQ Eight on frequency-critical tracks
    3. Sub/Kick not correctly sharing 40-80 Hz range
    4. Tracks violating their assigned frequency ownership

    Returns:
    - Conflict analysis with recommendations for fixing violations

    Example (summary mode):
    {
      "status": "success",
      "conflict_count": 2,
      "summary": {
        "high_severity": 1,
        "medium_severity": 1,
        "low_severity": 0
      }
    }

    Example (detailed mode):
    {
      "status": "success",
      "conflicts": [
        {
          "track_1": "FC_Pad",
          "track_2": "FC_RollingBass",
          "conflict_range": "Below 300 Hz",
          "severity": "high",
          "recommendation": "High-pass FC_Pad to 300 Hz minimum"
        }
      ]
    }
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_check_frequency_conflicts(
            ableton_connection=ableton,
            report_mode=report_mode
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error checking frequency conflicts: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error checking frequency conflicts: {str(e)}"
        }, indent=2)

@mcp.tool()
def import_continuation_brief(
    ctx: Context,
    brief_path: str,
    restore_mode: str = "markers_only"
) -> str:
    """
    Restore session context from continuation brief JSON.

    This command is the reverse of export_session_state. It reads a previously
    exported session state JSON file and restores session context into Ableton.

    Parameters:
    - brief_path: Path to JSON brief file (e.g., "C:\\Users\\Avi\\Desktop\\GoAI\\session-states\\session_state_20260214.json")
    - restore_mode: Restoration level (default: "markers_only")
                   "markers_only" = Set tempo, create locators, set key signature
                   "full" = Also create tracks, load instruments, set send levels

    Restore Modes:
    - markers_only: Restores tempo, locators/markers, and key signature only.
                   Use this when you want to preserve your existing tracks but
                   restore the narrative structure and session metadata.

    - full: Restores everything including tracks, instruments, devices, and routing.
           Use this when starting from a blank session and want to recreate
           the entire production setup from the continuation brief.

    Example:
    import_continuation_brief(
        brief_path="C:\\Users\\Avi\\Desktop\\GoAI\\session-states\\session_state_20260214.json",
        restore_mode="markers_only"
    )

    Returns JSON with:
    - tempo_set: BPM value that was restored
    - markers_created: Number of locators created
    - tracks_created: Number of tracks created (0 in markers_only mode)
    - warnings: Array of any issues encountered during restoration
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_import_continuation_brief(
            ableton_connection=ableton,
            brief_path=brief_path,
            restore_mode=restore_mode
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error importing continuation brief: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error importing continuation brief: {str(e)}"
        }, indent=2)

@mcp.tool()
def transition_between_sections(
    ctx: Context,
    bar_position: int,
    type: str,
    duration_bars: int = 2
) -> str:
    """
    Insert pre-built transition patterns between sections.

    Creates automation and/or audio clips for smooth transitions between
    musical sections. Essential for narrative arc transitions (Horror→Defiance→Triumph).

    Parameters:
    - bar_position: Bar position where transition occurs (target/impact point)
    - type: Transition type (required)
           "filter_sweep" = Master filter cutoff descends 8kHz → 200Hz
           "impact_hit" = Places impact sample with reverb automation spike
           "reverse_cymbal" = Places reverse cymbal clip leading into bar_position
           "silence_drop" = Volume drops to -inf 1 beat before, snaps back at bar_position
    - duration_bars: Length of transition in bars (default: 2, range: 1-16)

    Transition Types Explained:
    - filter_sweep: Classic trance breakdown transition. Master filter cutoff
                   sweeps down from 8kHz to 200Hz over duration_bars, creating
                   a darkening/closing effect. Perfect for Horror phase transitions.

    - impact_hit: Places an impact/hit sample on the FC_FX track with reverb
                 send automation spike at the exact bar_position. Creates dramatic
                 punctuation for drop entrances and section changes.

    - reverse_cymbal: Places a reverse cymbal clip that builds into bar_position.
                     The cymbal starts 1-2 bars before (based on duration_bars) and
                     crescendos into the target bar. Classic buildup element.

    - silence_drop: Creates a "silence before the drop" effect. Volume automation
                   drops to -inf dB on the 4th beat of the bar before bar_position,
                   then snaps back to 0 dB exactly at bar_position. Maximum tension.

    Example:
    transition_between_sections(
        bar_position=64,
        type="filter_sweep",
        duration_bars=2
    )

    Creates: 2-bar filter sweep ending at bar 64

    Note: Some transitions require automation API support. The command will
    create placeholder clips and log the intended automation parameters until
    full automation support is available in the base MCP server.
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_transition_between_sections(
            ableton_connection=ableton,
            bar_position=bar_position,
            type=type,
            duration_bars=duration_bars
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error creating transition: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error creating transition: {str(e)}"
        }, indent=2)

@mcp.tool()
def generate_buildup_riser(
    ctx: Context,
    track_index: int,
    start_bar: int,
    length_bars: int = 16,
    pitch_rise_semitones: int = 24,
    filter_sweep: bool = True,
    intensity: float = 0.7
) -> str:
    """
    Generate automated pitch rise + filter sweep for buildups.

    Creates a MIDI clip with a sustained note plus automation for pitch bend,
    filter cutoff, and volume. Perfect for creating tension before drops.

    Parameters:
    - track_index: Target track (usually FC_FX track)
    - start_bar: Where riser begins
    - length_bars: Riser length in bars (default: 16)
    - pitch_rise_semitones: Pitch rise amount in semitones (default: 24, 2 octaves)
    - filter_sweep: Add filter cutoff automation (default: True)
    - intensity: 0.0 = subtle, 1.0 = extreme (default: 0.7)

    Creates:
    - MIDI clip with single held note (C2)
    - Pitch bend automation (0 → pitch_rise_semitones)
    - Filter cutoff automation (200Hz → 8kHz) if enabled
    - Volume automation (fade in, exponential curve)

    Returns:
    - Status with clip_created, automation_envelopes count, pitch_rise, bars

    Example:
    generate_buildup_riser(track_index=8, start_bar=17, length_bars=16, intensity=0.8)

    Creates: 16-bar riser at bar 17 with 24-semitone pitch rise and filter sweep
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_generate_buildup_riser(
            ableton_connection=ableton,
            track_index=track_index,
            start_bar=start_bar,
            length_bars=length_bars,
            pitch_rise_semitones=pitch_rise_semitones,
            filter_sweep=filter_sweep,
            intensity=intensity
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error generating buildup riser: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error generating buildup riser: {str(e)}"
        }, indent=2)

@mcp.tool()
def create_nitzhonot_bass_template(
    ctx: Context,
    key: str = "Dm",
    scale: str = "harmonic_minor",
    group_name: str = "Bass Group"
) -> str:
    """
    Create pre-routed rolling bass + sub bass track pair with sidechain.

    Creates a Nitzhonot-style bass setup with two complementary bass tracks:
    - Rolling Bass: Mid-bass energy (80-200 Hz) with Serum/Operator
    - Sub Bass: Pure sub-bass (20-80 Hz) with sine wave

    Both tracks are pre-configured with EQ Eight and Compressor with sidechain
    routing to the kick drum (manual sidechain configuration required).

    Parameters:
    - key: Musical key (e.g., "Dm", "Am")
    - scale: Scale type (default: "harmonic_minor")
    - group_name: Track group name (default: "Bass Group")

    Creates:
    ```
    Bass Group (track group)
    ├── FC_RollingBass
    │   ├── Serum (or Operator fallback)
    │   ├── EQ Eight (HP @ 80Hz, LP @ 200Hz)
    │   └── Compressor (sidechain to kick)
    └── FC_SubBass
        ├── Operator (sine wave)
        ├── EQ Eight (HP @ 20Hz, LP @ 80Hz)
        └── Compressor (sidechain to kick, faster attack)
    ```

    Returns:
    - Status with group_created, tracks_in_group, sidechain_configured, warnings

    Example:
    create_nitzhonot_bass_template(key="Dm", scale="harmonic_minor")

    Creates: 2-track bass group ready for Nitzhonot production
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_create_nitzhonot_bass_template(
            ableton_connection=ableton,
            key=key,
            scale=scale,
            group_name=group_name
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error creating Nitzhonot bass template: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error creating Nitzhonot bass template: {str(e)}"
        }, indent=2)

@mcp.tool()
def set_section_markers(
    ctx: Context,
    markers: List[Dict[str, Any]] = None,
    preset: str = None,
    total_bars: int = None,
    drop_count: int = None,
    clear_existing: bool = False
) -> str:
    """
    Create Ableton locators (arrangement markers) from narrative arc.

    This command bridges narrative workflow to Ableton timeline by creating
    color-coded locators that mark key sections of your track's emotional journey.

    Parameters:
    - markers: Array of marker objects with bar, label, color, phase
               Each marker: {"bar": int, "label": str, "color": str, "phase": str}
               Colors: "red", "orange", "yellow", "green", "blue", "purple", "gray"
               Phases: "horror", "defiance", "triumph", "transition"
    - preset: Preset template name (overrides markers if provided)
              Options: "standard_three_act", "two_drop", "extended_breakdown", "fast_capture"
    - total_bars: Total track length in bars (used with presets to scale markers)
    - drop_count: Number of drops (metadata, not used for scaling currently)
    - clear_existing: Remove all existing locators first (default: false)

    Preset Templates:
    - standard_three_act: Horror→Defiance→Triumph with 3 drops (10 markers)
    - two_drop: Shorter track, 2 drops (7 markers)
    - extended_breakdown: Long emotional breakdown between drops (11 markers)
    - fast_capture: Minimal - just intro/main/outro (3 markers)

    Example with custom markers:
    set_section_markers(
        markers=[
            {"bar": 1, "label": "INTRO - Dread", "color": "red", "phase": "horror"},
            {"bar": 33, "label": "DROP 1 - Horror", "color": "red", "phase": "horror"},
            {"bar": 97, "label": "DROP 2 - Defiance", "color": "orange", "phase": "defiance"}
        ]
    )

    Example with preset:
    set_section_markers(
        preset="standard_three_act",
        total_bars=208,
        clear_existing=true
    )

    Returns:
    JSON with markers_created count, phase breakdown, and total_bars
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_set_section_markers(
            ableton_connection=ableton,
            markers=markers,
            preset=preset,
            total_bars=total_bars,
            drop_count=drop_count,
            clear_existing=clear_existing
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error setting section markers: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error setting section markers: {str(e)}"
        }, indent=2)

@mcp.tool()
def export_session_state(
    ctx: Context,
    output_format: str = "both",
    output_path: str = None,
    include_midi_summary: bool = True,
    include_automation_summary: bool = True
) -> str:
    """
    Export current Ableton session as JSON + markdown for continuation briefs.

    This command reads the current session state and generates files that map
    to CONTINUATION_BRIEF_TEMPLATE, allowing you to resume work later with
    full context about what's been placed and what's still needed.

    Parameters:
    - output_format: File format to generate (default: "both")
                     Options: "json", "markdown", "both"
    - output_path: Directory to save files (default: current directory)
    - include_midi_summary: Summarize MIDI clip contents (default: true)
    - include_automation_summary: List automated parameters (default: true)

    Output Files:
    1. session_state_[timestamp].json - Full structured data
       Contains: BPM, time signature, all tracks, clips, devices, MIDI note counts

    2. session_state_[timestamp].md - Human-readable markdown
       Contains: Track table with MIDI/device/automation status, completion percentage

    Markdown Format:
    | Track | Has MIDI? | Devices? | Automation? | Status |
    |-------|-----------|----------|-------------|--------|
    | FC_Kick | ✅ (16 notes) | ✅ Drum Rack | ❌ | Looping |
    | FC_RollingBass | ✅ (64 notes) | ✅ Serum | ✅ Filter | Looping |

    Completion Estimate:
    - Tracks with content: 2/11 (18%)
    - Tracks with automation: 1/11 (9%)

    Example:
    export_session_state(
        output_format="both",
        output_path="C:\\Users\\Avi\\Desktop\\GoAI\\session-states\\",
        include_midi_summary=true
    )

    Returns:
    JSON with file paths and summary statistics
    """
    try:
        ableton = get_ableton_connection()
        result = _fc_export_session_state(
            ableton_connection=ableton,
            output_format=output_format,
            output_path=output_path,
            include_midi_summary=include_midi_summary,
            include_automation_summary=include_automation_summary
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error exporting session state: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Error exporting session state: {str(e)}"
        }, indent=2)

# ============================================================================
# End Flyin' Colors Extension
# ============================================================================

# Main execution
def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()
