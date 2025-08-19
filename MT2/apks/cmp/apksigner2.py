#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import time
import json
import shutil
import zipfile
import hashlib
import logging
import argparse
import platform
import subprocess
import threading
import traceback
from typing import Optional, Dict, List, Tuple, Any, Union, NoReturn
from datetime import datetime
from pathlib import Path
import random
import string
import signal
import tempfile
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# 基础配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('apksigner.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 常量定义
VALID_COUNTRY_CODES = {
    'CN': 'China', 'US': 'United States', 'GB': 'United Kingdom',
    'DE': 'Germany', 'FR': 'France', 'JP': 'Japan', 'KR': 'South Korea',
    'IN': 'India', 'RU': 'Russia', 'BR': 'Brazil'
}

# 基础异常类
class SystemException(Exception):
    pass

class ValidationException(Exception):
    pass

class SecurityException(Exception):
    pass

class ProcessException(Exception):
    pass

# 数据类
@dataclass
class KeystoreConfig:
    path: str
    alias: str
    store_password: str
    key_password: str

# 配置类
class AppConfig:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.apk_signer")
        self.keystore_dir = os.path.join(self.config_dir, "keystores")
        self.config_file = os.path.join(self.config_dir, "keystore_config.json")

# UI基类
class UIBase(ABC):
    @abstractmethod
    def display_message(self, message: str, level: str) -> None:
        pass

    @abstractmethod
    def show_progress(self, current: int, total: int) -> None:
        pass

# 增强版UI类
class EnterpriseUI(UIBase):
    COLORS = {
        'neon_green': '\033[38;5;46m',
        'neon_blue': '\033[38;5;51m',
        'neon_pink': '\033[38;5;198m',
        'neon_yellow': '\033[38;5;226m',
        'neon_purple': '\033[38;5;165m',
        'neon_red': '\033[38;5;196m',
        'dark_gray': '\033[38;5;240m',
        'bright_cyan': '\033[38;5;87m',
        'glitch_red': '\033[38;5;160m',
        'glitch_blue': '\033[38;5;33m',
        'reset': '\033[0m'
    }
    
    STYLES = {
        'bold': '\033[1m',
        'blink': '\033[5m',
        'dim': '\033[2m',
        'reverse': '\033[7m',
        'hidden': '\033[8m',
        'strike': '\033[9m'
    }

    def __init__(self):
        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines
        self.stop_animation = False
        self.scan_line_pos = 0
        self.glitch_chars = "▓▒░█▀▄▐▌▂▁▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓"
        self.noise_density = 0.1

    def create_noise(self, width: int) -> str:
        return ''.join(random.choice(self.glitch_chars) if random.random() < self.noise_density else ' ' 
                      for _ in range(width))

    def create_scan_line(self, width: int) -> str:
        return f"{self.COLORS['dark_gray']}{self.STYLES['dim']}{'█' * width}{self.COLORS['reset']}"

    def glitch_effect(self, text: str, intensity: float = 0.3) -> str:
        result = ''
        for char in text:
            if random.random() < intensity:
                color = self.COLORS['glitch_red'] if random.random() < 0.5 else self.COLORS['glitch_blue']
                result += f"{color}{random.choice(self.glitch_chars)}"
            else:
                result += char
        return result + self.COLORS['reset']

    def display_message(self, message: str, level: str = 'info') -> None:
        color = self.COLORS.get(f'neon_{level}', self.COLORS['neon_blue'])
        print(f"{color}[{level.upper()}] {message}{self.COLORS['reset']}")

    def show_progress(self, current: int, total: int) -> None:
        bar_length = 40
        filled_length = int(bar_length * current / total)
        
        bar = ''
        for i in range(bar_length):
            if i < filled_length:
                bar += '█' if random.random() > 0.1 else random.choice("▓▒░")
            else:
                bar += '▒' if random.random() > 0.05 else random.choice("░▒▓")
                    
        percentage = current / total * 100
        progress_text = f"{self.COLORS['neon_green']}Progress |{bar}| {percentage:.1f}%"
        scan_line = " " * (int(bar_length * current / total)) + "▀"
        progress_text += f"\n{self.COLORS['bright_cyan']}{scan_line}"
        
        print(f"\r{progress_text}{self.COLORS['reset']}", end='')
        if current == total:
            print()

    def cyber_print(self, text: str, effect: str = 'normal') -> None:
        width = self.width
        
        if effect == 'glitch':
            for _ in range(3):
                glitched_text = self.glitch_effect(text)
                noise_line = self.create_noise(width)
                scan_line = " " * self.scan_line_pos + "▀" + " " * (width - self.scan_line_pos - 1)
                
                print(f"\r{self.COLORS['dark_gray']}{noise_line}", end='')
                print(f"\r{self.COLORS['bright_cyan']}{scan_line}", end='')
                print(f"\r{glitched_text}", end='')
                
                self.scan_line_pos = (self.scan_line_pos + 5) % width
                time.sleep(0.1)
        
        print(f"\r{text}{self.COLORS['reset']}")

    def show_loading(self, text: str = "PROCESSING", duration: int = 3) -> None:
        frames = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
        glitch_frames = "▓▒░█▀▄"
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < duration:
            frame = frames[i % len(frames)]
            glitch = glitch_frames[i % len(glitch_frames)]
            noise = self.create_noise(5)
            
            animation = f"{self.COLORS['neon_blue']}{frame} "
            animation += f"{self.COLORS['glitch_red']}{glitch} "
            animation += f"{self.COLORS['dark_gray']}{noise} "
            animation += f"{self.COLORS['neon_green']}{text}"
            
            print(f"\r{animation}", end='')
            time.sleep(0.1)
            i += 1
        print(f"{self.COLORS['reset']}")

    def show_banner(self) -> None:
        banner_text = f"""
{self.COLORS['dark_gray']}▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
{self.COLORS['neon_blue']}██████╗ ██╗  ██╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗███████╗██████╗ 
{self.COLORS['glitch_blue']}██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║██╔════╝ ████╗  ██║██╔════╝██╔══██╗
{self.COLORS['neon_purple']}██████╔╝█████╔╝ ██████╔╝███████╗██║██║  ███╗██╔██╗ ██║█████╗  ██████╔╝
{self.COLORS['glitch_red']}██╔═══╝ ██╔═██╗ ██╔══██╗╚════██║██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
{self.COLORS['neon_red']}██║     ██║  ██╗██║  ██║███████║██║╚██████╔╝██║ ╚████║███████╗██║  ██║
{self.COLORS['dark_gray']}▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒{self.COLORS['reset']}
        """
        
        for line in banner_text.split('\n'):
            self.cyber_print(line, 'glitch')
            time.sleep(0.1)
        
        slogan = f"{self.COLORS['neon_green']}>> QUANTUM SECURITY PROTOCOL ACTIVATED <<"
        self.cyber_print(slogan, 'glitch')
        self.show_loading("INITIALIZING SYSTEM", 2)

class SecurityManager:
    def __init__(self):
        self.ui = EnterpriseUI()
        self._config = AppConfig()
        self._initialize_security()

    def _initialize_security(self) -> None:
        os.makedirs(self._config.keystore_dir, exist_ok=True)
        os.chmod(self._config.keystore_dir, 0o700)

    def validate_input(self, input_type: str, value: str) -> bool:
        if input_type == "keystore_name":
            if not re.match(r'^[a-zA-Z0-9_-]+$', value):
                raise ValidationException("Invalid keystore name format")
        elif input_type == "password":
            if len(value) < 8 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', value):
                raise ValidationException("Password does not meet security requirements")
        elif input_type == "country_code":
            if value not in VALID_COUNTRY_CODES:
                raise ValidationException(f"Invalid country code. Valid codes are: {', '.join(VALID_COUNTRY_CODES.keys())}")
        return True

    def verify_file_permissions(self, file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                current_perms = oct(os.stat(file_path).st_mode)[-3:]
                if current_perms != '600':
                    os.chmod(file_path, 0o600)
            return True
        except Exception as e:
            raise SecurityException(f"Permission verification failed: {str(e)}")

class ProcessManager:
    def __init__(self):
        self.ui = EnterpriseUI()
        self.security = SecurityManager()
        self._temp_dir = tempfile.mkdtemp()
        signal.signal(signal.SIGINT, self._cleanup)

    def _cleanup(self, signum=None, frame=None) -> None:
        if os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
        if signum:
            sys.exit(1)

    def execute_command(self, command: List[str], error_msg: str) -> subprocess.CompletedProcess:
        try:
            self.ui.show_loading(f"Executing: {command[0]}")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise ProcessException(f"{error_msg}: {result.stderr}")
            return result
        except Exception as e:
            raise ProcessException(f"Command execution failed: {str(e)}")

class KeystoreManager:
    def __init__(self):
        self.ui = EnterpriseUI()
        self.security = SecurityManager()
        self.process_manager = ProcessManager()
        self._config = AppConfig()
        self._load_configuration()

    def _load_configuration(self) -> None:
        try:
            if os.path.exists(self._config.config_file):
                with open(self._config.config_file, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
            else:
                self._settings = self._get_default_configuration()
                self._save_configuration()
        except Exception as e:
            raise SystemException(f"Configuration loading failed: {str(e)}")

    def _get_default_configuration(self) -> Dict:
        return {
            'default_keystore': {
                'path': os.path.join(self._config.keystore_dir, "debug.keystore"),
                'alias': "androiddebugkey",
                'store_password': "android",
                'key_password': "android"
            },
            'custom_keystores': {}
        }

    def _save_configuration(self) -> None:
        try:
            with open(self._config.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=4)
            self.security.verify_file_permissions(self._config.config_file)
        except Exception as e:
            raise SystemException(f"Configuration saving failed: {str(e)}")

    def ensure_default_keystore(self) -> None:
        default_keystore = os.path.join(self._config.keystore_dir, "debug.keystore")
        if not os.path.exists(default_keystore):
            try:
                self.ui.show_loading("Creating default keystore")
                
                cmd = [
                    "keytool", "-genkey", "-v",
                    "-keystore", default_keystore,
                    "-alias", "androiddebugkey",
                    "-keyalg", "RSA",
                    "-keysize", "2048",
                    "-validity", "10000",
                    "-storepass", "android",
                    "-keypass", "android",
                    "-dname", "CN=Android Debug,O=Android,C=US"
                ]
                
                self.process_manager.execute_command(cmd, "Default keystore creation failed")
                self.security.verify_file_permissions(default_keystore)
                
            except Exception as e:
                raise SecurityException(f"Failed to create default keystore: {str(e)}")

    def create_keystore(self, name: str, info: Dict) -> bool:
        try:
            self.security.validate_input("keystore_name", name)
            self.security.validate_input("password", info['store_password'])
            self.security.validate_input("password", info['key_password'])
            self.security.validate_input("country_code", info['c'])

            keystore_path = os.path.join(self._config.keystore_dir, f"{name}.keystore")
            
            if os.path.exists(keystore_path):
                raise ValidationException(f"Keystore '{name}' already exists")
                
            self.ui.show_loading("GENERATING SECURE KEYSTORE")
            
            cmd = [
                "keytool", "-genkey", "-v",
                "-keystore", keystore_path,
                "-alias", info['alias'],
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-storepass", info['store_password'],
                "-keypass", info['key_password'],
                "-dname", (f"CN={info.get('cn', 'Unknown')}, "
                          f"OU={info.get('ou', 'Unknown')}, "
                          f"O={info.get('o', 'Unknown')}, "
                          f"L={info.get('l', 'Unknown')}, "
                          f"ST={info.get('st', 'Unknown')}, "
                          f"C={info['c']}")
            ]
            
            self.process_manager.execute_command(cmd, "Keystore generation failed")
            self.security.verify_file_permissions(keystore_path)
            
            self._settings['custom_keystores'][name] = {
                'path': keystore_path,
                'alias': info['alias'],
                'store_password': info['store_password'],
                'key_password': info['key_password']
            }
            self._save_configuration()
            
            return True
            
        except Exception as e:
            if 'keystore_path' in locals() and os.path.exists(keystore_path):
                os.remove(keystore_path)
            raise SecurityException(f"Keystore creation failed: {str(e)}")

    def get_keystore_info(self, name: str) -> Optional[Dict]:
        try:
            if name == "default":
                return self._settings['default_keystore']
            return self._settings['custom_keystores'].get(name)
        except Exception as e:
            raise SecurityException(f"Failed to get keystore info: {str(e)}")

    def list_keystores(self) -> None:
        try:
            self.ui.cyber_print("\n=== KEYSTORES ===", "glitch")
            self.ui.cyber_print("\nDefault keystore:", "glitch")
            self.ui.cyber_print(json.dumps(self._settings['default_keystore'], indent=2))
            
            if self._settings['custom_keystores']:
                self.ui.cyber_print("\nCustom keystores:", "glitch")
                for name, info in self._settings['custom_keystores'].items():
                    self.ui.cyber_print(f"\n{name}:", "glitch")
                    self.ui.cyber_print(json.dumps(info, indent=2))
            else:
                self.ui.cyber_print("\nNo custom keystores found")
        except Exception as e:
            raise SecurityException(f"Failed to list keystores: {str(e)}")

class EnterpriseAPKSigner:
    def __init__(self):
        self.ui = EnterpriseUI()
        self.keystore_manager = KeystoreManager()
        self.process_manager = ProcessManager()
        self.security = SecurityManager()
        self._verify_environment()

    def _verify_environment(self) -> None:
        try:
            self.ui.show_loading("VERIFYING SYSTEM ENVIRONMENT")
            
            if not os.path.exists("/data/data/com.termux"):
                raise SystemException("This script must run in Termux environment!")
                
            required_tools = ['apksigner', 'zipalign', 'keytool']
            missing_tools = []
            for tool in required_tools:
                if shutil.which(tool) is None:
                    missing_tools.append(tool)
                    
            if missing_tools:
                raise SystemException(
                    f"Required tools not found: {', '.join(missing_tools)}\n"
                    "Please install missing tools using:\n"
                    "pkg install apksigner zipalign openjdk-17"
                )
                
            self.ui.show_loading("ENVIRONMENT VERIFICATION COMPLETE")
            
        except Exception as e:
            raise SystemException(f"Environment verification failed: {str(e)}")

    def optimize_apk(self, input_apk: str, output_apk: str) -> bool:
        try:
            self.ui.show_loading("OPTIMIZING APK")
            
            cmd = ["zipalign", "-v", "-p", "4", input_apk, output_apk]
            self.process_manager.execute_command(cmd, "APK optimization failed")
            
            return True
            
        except Exception as e:
            raise ProcessException(f"APK optimization failed: {str(e)}")

    def sign_apk(self, input_apk: str, output_apk: str, keystore_name: str = "default") -> bool:
        try:
            if not os.path.exists(input_apk):
                raise FileNotFoundError(f"Input APK not found: {input_apk}")
                
            keystore_info = self.keystore_manager.get_keystore_info(keystore_name)
            if not keystore_info:
                raise SecurityException(f"Keystore not found: {keystore_name}")
                
            keystore_path = os.path.expanduser(keystore_info['path'])
            if not os.path.exists(keystore_path):
                raise SecurityException(f"Keystore file not found: {keystore_path}")
                
            optimized_apk = os.path.join(self.process_manager._temp_dir, "optimized.apk")
            self.optimize_apk(input_apk, optimized_apk)
                
            self.ui.show_loading("SIGNING APK")
            
            sign_cmd = [
                "apksigner", "sign",
                "--ks", keystore_path,
                "--ks-key-alias", keystore_info['alias'],
                "--ks-pass", f"pass:{keystore_info['store_password']}",
                "--key-pass", f"pass:{keystore_info['key_password']}",
                "--out", output_apk,
                optimized_apk
            ]
            
            self.process_manager.execute_command(sign_cmd, "APK signing failed")
                
            self.ui.show_loading("VERIFYING SIGNATURE")
            verify_cmd = ["apksigner", "verify", "-v", output_apk]
            self.process_manager.execute_command(verify_cmd, "Signature verification failed")
                
            self.ui.cyber_print("\nAPK SIGNING COMPLETE", "glitch")
            self.ui.cyber_print(f"\nOutput file: {output_apk}")
            
            return True
            
        except Exception as e:
            logger.error(traceback.format_exc())
            raise ProcessException(f"APK signing process failed: {str(e)}")
            
        finally:
            self.process_manager._cleanup()

    def create_new_keystore(self) -> None:
        try:
            self.ui.cyber_print("\n=== CREATE KEYSTORE ===", "glitch")
            self.ui.cyber_print("\nAvailable country codes:", "glitch")
            for code, name in VALID_COUNTRY_CODES.items():
                self.ui.cyber_print(f"{code}: {name}")
            
            name = input("\nKeystore name: ").strip()
            info = {
                'alias': input("Key alias [key0]: ").strip() or "key0",
                'store_password': input("Keystore password (min 8 chars): ").strip(),
                'key_password': input("Key password (min 8 chars): ").strip(),
                'cn': input("Common Name (CN) [Unknown]: ").strip() or "Unknown",
                'ou': input("Organization Unit (OU) [Unknown]: ").strip() or "Unknown",
                'o': input("Organization (O) [Unknown]: ").strip() or "Unknown",
                'l': input("Location (L) [Unknown]: ").strip() or "Unknown",
                'st': input("State (ST) [Unknown]: ").strip() or "Unknown",
                'c': input("Country Code (e.g., CN) [CN]: ").strip().upper() or "CN"
            }
            
            self.keystore_manager.create_keystore(name, info)
            
        except KeyboardInterrupt:
            self.ui.cyber_print("\nKeystore creation cancelled", "glitch")
            raise
        except Exception as e:
            raise SecurityException(f"Keystore creation failed: {str(e)}")

def main() -> None:
    try:
        signer = EnterpriseAPKSigner()
        ui = EnterpriseUI()
        
        ui.show_banner()
        
        while True:
            ui.cyber_print("\n=== QUANTUM SECURITY INTERFACE ===", "glitch")
            menu = """
1. Sign APK
2. Create Keystore
3. List Keystores
0. Exit
            """
            ui.cyber_print(menu, "normal")
            
            try:
                choice = input("\nSelect option [0-3]: ").strip()
                
                if choice == "1":
                    ui.show_loading("INITIALIZING SIGNATURE PROCESS")
                    input_apk = input("\nInput APK path: ").strip()
                    output_apk = input("Output APK path (Enter for default): ").strip()
                    if not output_apk:
                        output_apk = input_apk.replace('.apk', '_signed.apk')
                    keystore_name = input("Keystore name (Enter for default): ").strip() or "default"
                    
                    # 显示进度
                    for i in range(101):
                        ui.show_progress(i, 100)
                        time.sleep(0.02)
                    
                    signer.sign_apk(input_apk, output_apk, keystore_name)
                    
                elif choice == "2":
                    signer.create_new_keystore()
                    
                elif choice == "3":
                    signer.keystore_manager.list_keystores()
                    
                elif choice == "0":
                    ui.show_loading("SHUTTING DOWN QUANTUM SECURITY PROTOCOL", 2)
                    ui.cyber_print("\nSYSTEM SHUTDOWN COMPLETE", "glitch")
                    break
                    
                else:
                    ui.cyber_print("\nINVALID OPTION SELECTED", "glitch")
                    
            except KeyboardInterrupt:
                ui.cyber_print("\nOPERATION CANCELLED BY USER", "glitch")
                continue
                
            except (ValidationException, SecurityException, ProcessException) as e:
                ui.cyber_print(f"\nERROR: {str(e)}", "glitch")
                logger.error(traceback.format_exc())
                continue
                
            except Exception as e:
                ui.cyber_print(f"\nUNEXPECTED ERROR: {str(e)}", "glitch")
                logger.error(traceback.format_exc())
                continue
                
    except KeyboardInterrupt:
        ui.cyber_print("\nEMERGENCY SHUTDOWN INITIATED", "glitch")
        ui.show_loading("PERFORMING EMERGENCY CLEANUP", 1)
        sys.exit(0)
        
    except Exception as e:
        logger.error(traceback.format_exc())
        print(f"\nCRITICAL SYSTEM ERROR: {str(e)}")
        sys.exit(1)
        
    finally:
        try:
            # 清理所有临时文件
            if hasattr(signer, 'process_manager'):
                signer.process_manager._cleanup()
        except:
            pass

if __name__ == "__main__":
    main()
