import time
import sys
import os
from datetime import datetime
import random
import json
import hashlib

# ==================== CONFIGURATION ====================
log_file = "animation_log.txt"
stats_file = "system_stats.json"
pattern_count = 0
cycle_count = 0
total_chars_generated = 0
start_time = datetime.now()

class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# ==================== FITUR 1: AI PATTERN PREDICTOR ====================
# Sistem yang "memprediksi" pattern berikutnya berdasarkan history
pattern_history = []

def predict_next_pattern():
    if len(pattern_history) < 3:
        return random.choice(['WAVE', 'PULSE', 'SPIRAL'])
    
    # Analisis pattern terakhir
    last_three = pattern_history[-3:]
    if last_three.count('WAVE') >= 2:
        return 'SPIRAL'
    elif last_three.count('SPIRAL') >= 2:
        return 'PULSE'
    else:
        return 'WAVE'

def generate_wave_pattern(i):
    chars = ['~', '≈', '∿']
    return chars[i % 3] * (i * i)

def generate_pulse_pattern(i):
    chars = ['●', '◉', '○']
    return f"{chars[i % 3]} " * (i * 2)

def generate_spiral_pattern(i):
    chars = ['◢', '◣', '◤', '◥']
    return chars[i % 4] * (i * 3)

# ==================== FITUR 2: REAL-TIME PERFORMANCE MONITOR ====================
# Monitor CPU usage pattern generation (simulasi)
class PerformanceMonitor:
    def __init__(self):
        self.load_history = []
        self.efficiency_score = 100.0
    
    def calculate_load(self):
        # Simulasi load berdasarkan pattern count
        base_load = (pattern_count % 100) / 2
        random_load = random.uniform(0, 20)
        current_load = min(base_load + random_load, 100)
        self.load_history.append(current_load)
        if len(self.load_history) > 10:
            self.load_history.pop(0)
        return current_load
    
    def get_avg_load(self):
        if not self.load_history:
            return 0
        return sum(self.load_history) / len(self.load_history)
    
    def get_health_status(self):
        avg = self.get_avg_load()
        if avg < 30:
            return f"{Colors.GREEN}OPTIMAL{Colors.RESET}", "●●●●●"
        elif avg < 60:
            return f"{Colors.YELLOW}GOOD{Colors.RESET}", "●●●●○"
        elif avg < 80:
            return f"{Colors.YELLOW}MODERATE{Colors.RESET}", "●●●○○"
        else:
            return f"{Colors.RED}HIGH{Colors.RESET}", "●●○○○"

monitor = PerformanceMonitor()

# ==================== FITUR 3: BLOCKCHAIN-STYLE PATTERN HASHING ====================
# Setiap pattern di-hash seperti blockchain untuk verifikasi integritas
pattern_chain = []

def hash_pattern(pattern_data, prev_hash):
    data_string = f"{pattern_data}{prev_hash}{datetime.now().isoformat()}"
    return hashlib.sha256(data_string.encode()).hexdigest()[:16]

def add_to_chain(pattern_type, length):
    prev_hash = pattern_chain[-1]['hash'] if pattern_chain else "0" * 16
    new_hash = hash_pattern(f"{pattern_type}{length}", prev_hash)
    
    pattern_chain.append({
        'index': len(pattern_chain),
        'pattern': pattern_type,
        'length': length,
        'hash': new_hash,
        'prev_hash': prev_hash,
        'timestamp': datetime.now().isoformat()
    })
    
    return new_hash

# ==================== BONUS FITUR: SMART SAVE SYSTEM ====================
def save_session_stats():
    runtime = (datetime.now() - start_time).total_seconds()
    stats = {
        'session_start': start_time.isoformat(),
        'session_end': datetime.now().isoformat(),
        'runtime_seconds': runtime,
        'total_cycles': cycle_count,
        'total_patterns': pattern_count,
        'total_chars': total_chars_generated,
        'avg_load': monitor.get_avg_load(),
        'chain_length': len(pattern_chain),
        'last_hash': pattern_chain[-1]['hash'] if pattern_chain else None
    }
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

# ==================== UI FUNCTIONS ====================
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_dashboard():
    clear_terminal()
    runtime = (datetime.now() - start_time).total_seconds()
    current_load = monitor.calculate_load()
    status, health_bar = monitor.get_health_status()
    
    print(f"{Colors.BOLD}{Colors.CYAN}╔{'═' * 78}╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} {Colors.BOLD}ADVANCED PATTERN GENERATION SYSTEM v2.0{Colors.RESET}                              {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╠{'═' * 78}╣{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Runtime: {Colors.GREEN}{runtime:.1f}s{Colors.RESET} | Cycles: {Colors.YELLOW}{cycle_count}{Colors.RESET} | Patterns: {Colors.PURPLE}{pattern_count}{Colors.RESET} | Chars: {Colors.BLUE}{total_chars_generated}{Colors.RESET}     {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} System Load: {current_load:.1f}% | Status: {status} {health_bar}                    {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.RESET} Chain Length: {Colors.GREEN}{len(pattern_chain)}{Colors.RESET} blocks | Last Hash: {Colors.DIM}{pattern_chain[-1]['hash'] if pattern_chain else 'N/A':16}{Colors.RESET}  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 78}╝{Colors.RESET}\n")

# ==================== MAIN PROGRAM ====================
draw_dashboard()
print(f"{Colors.YELLOW}[INIT] Starting AI Pattern Generator...{Colors.RESET}")
time.sleep(1)
print(f"{Colors.GREEN}[READY] System online. Press Ctrl+C to stop{Colors.RESET}\n")
time.sleep(1)

try:
    while True:
        cycle_count += 1
        
        # Refresh dashboard setiap 3 cycles
        if cycle_count % 3 == 0:
            draw_dashboard()
        
        # AI memilih pattern type
        pattern_type = predict_next_pattern()
        pattern_history.append(pattern_type)
        
        print(f"\n{Colors.BOLD}[CYCLE {cycle_count:03d}] AI Selected: {Colors.CYAN}{pattern_type}{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
        
        # Generate patterns
        for i in range(1, 9):
            if pattern_type == 'WAVE':
                pattern = generate_wave_pattern(i)
                color = Colors.CYAN
            elif pattern_type == 'PULSE':
                pattern = generate_pulse_pattern(i)
                color = Colors.PURPLE
            else:
                pattern = generate_spiral_pattern(i)
                color = Colors.GREEN
            
            print(f"{color}{pattern}{Colors.RESET}")
            
            # Update blockchain
            pattern_hash = add_to_chain(pattern_type, len(pattern))
            pattern_count += 1
            total_chars_generated += len(pattern)
            
            # Speed berdasarkan system load
            load = monitor.calculate_load()
            sleep_time = 0.05 + (load / 1000)  # Load tinggi = lebih lambat
            time.sleep(sleep_time)
        
        # Decreasing phase
        for i in range(7, 1, -1):
            if pattern_type == 'WAVE':
                pattern = generate_wave_pattern(i)
                color = Colors.BLUE
            elif pattern_type == 'PULSE':
                pattern = generate_pulse_pattern(i)
                color = Colors.YELLOW
            else:
                pattern = generate_spiral_pattern(i)
                color = Colors.RED
            
            print(f"{color}{pattern}{Colors.RESET}")
            
            pattern_hash = add_to_chain(pattern_type, len(pattern))
            pattern_count += 1
            total_chars_generated += len(pattern)
            
            load = monitor.calculate_load()
            sleep_time = 0.05 + (load / 1000)
            time.sleep(sleep_time)
            
except KeyboardInterrupt:
    print(f"\n\n{Colors.BOLD}{Colors.RED}{'═' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}[SHUTDOWN] Saving session data...{Colors.RESET}")
    
    save_session_stats()
    
    runtime = (datetime.now() - start_time).total_seconds()
    print(f"{Colors.BOLD}{Colors.RED}{'═' * 80}{Colors.RESET}")
    print(f"{Colors.GREEN}Total Runtime:     {Colors.BOLD}{runtime:.2f}s{Colors.RESET}")
    print(f"{Colors.GREEN}Total Cycles:      {Colors.BOLD}{cycle_count}{Colors.RESET}")
    print(f"{Colors.GREEN}Total Patterns:    {Colors.BOLD}{pattern_count}{Colors.RESET}")
    print(f"{Colors.GREEN}Total Characters:  {Colors.BOLD}{total_chars_generated:,}{Colors.RESET}")
    print(f"{Colors.GREEN}Blockchain Length: {Colors.BOLD}{len(pattern_chain)} blocks{Colors.RESET}")
    print(f"{Colors.GREEN}Average Load:      {Colors.BOLD}{monitor.get_avg_load():.1f}%{Colors.RESET}")
    print(f"{Colors.GREEN}Stats Saved:       {Colors.BOLD}{stats_file}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}{'═' * 80}{Colors.RESET}\n")
    sys.exit()