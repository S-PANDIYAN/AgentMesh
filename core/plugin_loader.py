"""
Plugin Loader for AgentMesh Framework.
Automatically discovers and loads agent plugins.
"""

import importlib
import importlib.util
from pathlib import Path
from typing import List, Dict, Any
import sys


class PluginLoader:
    """
    Discovers and loads agent plugins from plugins/ directory.
    Enables dynamic agent registration without hardcoding.
    """
    
    def __init__(self, plugin_dir: str = "plugins"):
        """
        Initialize plugin loader.
        
        Args:
            plugin_dir: Directory containing plugin files
        """
        self.plugin_dir = Path(plugin_dir)
        self.loaded_plugins: Dict[str, Any] = {}
    
    def discover_plugins(self) -> List[str]:
        """
        Discover all Python files in plugins directory.
        
        Returns:
            List of plugin module names
        """
        if not self.plugin_dir.exists():
            return []
        
        plugins = []
        for file_path in self.plugin_dir.glob("*_agent.py"):
            if file_path.stem != "__init__":
                plugins.append(file_path.stem)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """
        Load a single plugin module.
        
        Args:
            plugin_name: Name of plugin module (without .py)
            
        Returns:
            Dictionary with plugin metadata and factory function
        """
        try:
            # Import the plugin module
            module_path = f"plugins.{plugin_name}"
            module = importlib.import_module(module_path)
            
            # Extract plugin metadata
            metadata = {
                'name': getattr(module, 'PLUGIN_NAME', plugin_name),
                'version': getattr(module, 'PLUGIN_VERSION', '1.0.0'),
                'capabilities': getattr(module, 'PLUGIN_CAPABILITIES', []),
                'factory': getattr(module, 'create_agent', None),
                'module': module
            }
            
            self.loaded_plugins[plugin_name] = metadata
            return metadata
            
        except Exception as e:
            print(f"Warning: Failed to load plugin '{plugin_name}': {e}")
            return None
    
    def load_all_plugins(self) -> Dict[str, Dict[str, Any]]:
        """
        Discover and load all available plugins.
        
        Returns:
            Dictionary of loaded plugins
        """
        plugins = self.discover_plugins()
        
        for plugin_name in plugins:
            self.load_plugin(plugin_name)
        
        return self.loaded_plugins
    
    def create_agent_instance(self, plugin_name: str, *args, **kwargs) -> Any:
        """
        Create an agent instance from a loaded plugin.
        
        Args:
            plugin_name: Name of the plugin
            *args, **kwargs: Arguments to pass to factory function
            
        Returns:
            Agent instance
        """
        if plugin_name not in self.loaded_plugins:
            raise ValueError(f"Plugin '{plugin_name}' not loaded")
        
        metadata = self.loaded_plugins[plugin_name]
        factory = metadata.get('factory')
        
        if not factory:
            raise ValueError(f"Plugin '{plugin_name}' has no create_agent factory function")
        
        return factory(*args, **kwargs)
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """Get metadata about a loaded plugin."""
        return self.loaded_plugins.get(plugin_name)
    
    def get_all_capabilities(self) -> Dict[str, List[str]]:
        """
        Get capabilities of all loaded plugins.
        
        Returns:
            Dictionary mapping plugin names to capability lists
        """
        return {
            name: metadata['capabilities']
            for name, metadata in self.loaded_plugins.items()
        }
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Hot-reload a specific plugin without restarting the framework.
        
        Args:
            plugin_name: Name of plugin to reload
            
        Returns:
            True if reload successful, False otherwise
        """
        import importlib
        
        try:
            # Remove from cache if exists
            if plugin_name in self.loaded_plugins:
                module_name = f"plugins.{plugin_name}"
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
            
            # Reload the plugin
            self.load_plugin(plugin_name)
            return True
            
        except Exception as e:
            print(f"Error reloading plugin {plugin_name}: {e}")
            return False
    
    def reload_all_plugins(self) -> Dict[str, bool]:
        """
        Hot-reload all plugins without restarting the framework.
        
        Returns:
            Dictionary mapping plugin names to reload success status
        """
        results = {}
        for plugin_name in list(self.loaded_plugins.keys()):
            results[plugin_name] = self.reload_plugin(plugin_name)
        return results
    
    def watch_plugins(self, callback=None) -> None:
        """
        Watch plugin directory for changes and auto-reload.
        
        Args:
            callback: Optional function to call after reload (receives plugin_name, success)
        """
        import time
        from pathlib import Path
        
        file_mtimes = {}
        
        while True:
            try:
                for file_path in self.plugin_dir.glob("*_agent.py"):
                    current_mtime = file_path.stat().st_mtime
                    plugin_name = file_path.stem
                    
                    if plugin_name in file_mtimes:
                        if current_mtime > file_mtimes[plugin_name]:
                            print(f"🔄 Detected change in {plugin_name}, reloading...")
                            success = self.reload_plugin(plugin_name)
                            if callback:
                                callback(plugin_name, success)
                    
                    file_mtimes[plugin_name] = current_mtime
                
                time.sleep(2)  # Check every 2 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopped watching plugins")
                break
            except Exception as e:
                print(f"Error watching plugins: {e}")
                time.sleep(2)
