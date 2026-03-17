import sys
from pathlib import Path
from typing import Optional
import importlib.util

from config import SCHEMA_DIR, FORKS


class ForkManager:
    """Manages fork-specific schema operations"""
    
    def __init__(self, fork_name: str = 'mihon'):
        self.fork_name = fork_name
        self.schema_path = SCHEMA_DIR / f"schema_{fork_name}.proto"
        self.module_name = f"schema_{fork_name}_pb2"
        
    def import_schema(self):
        """Import the schema module for the current fork"""
        module_path = SCHEMA_DIR / f"{self.module_name}.py"
        
        if not module_path.exists():
            self.generate_schema()
            
        spec = importlib.util.spec_from_file_location(self.module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module.Backup
        
    def generate_schema(self):
        """Generate schema for the current fork"""
        from tachibk_legacy import proto_gen
        proto_gen(str(self.schema_path), self.fork_name)
        
        # Compile proto
        import subprocess
        try:
            subprocess.run([
                'protoc',
                f'--proto_path={SCHEMA_DIR}',
                f'--python_out={SCHEMA_DIR}',
                f'--pyi_out={SCHEMA_DIR}',
                str(self.schema_path)
            ], check=True)
        except FileNotFoundError:
            print("❌ protoc not found. Please install Protocol Buffers compiler")
            sys.exit(1)
            
    def get_backup_class(self):
        """Get the Backup class for the current fork"""
        Backup = self.import_schema()
        return Backup